import threading
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from datetime import datetime
from json import dumps, loads
from time import sleep

from flask import Flask, Response, render_template

from config import Development
from models import Track, db

app = Flask(__name__)
app.config.from_object(Development)  # change loaded config name to change attributes
db.init_app(app)

subscriptions = []

# Note: While developing many changes to this file required the project to be reloaded to take effect

# code originally from http://flask.pocoo.org/snippets/116/
class ServerSentEvent(object):
    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data: "data",
            self.event: "event",
            self.id: "id"
        }

    def __str__(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) for k, v in self.desc_map.items() if k]
        return "\n".join(lines) + "\n\n"


# Client code consumes like this.
@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)


@app.route("/publish")
def publish():
    # Dummy data - pick up from request for real data
    def notify():
        msg = str(datetime.time())
        for sub in subscriptions:
            sub.put(msg)
    gevent.spawn(notify)
    return "OK"


@app.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield str(ev)
        except GeneratorExit:  # Or maybe use flask signals
            subscriptions.remove(q)
    return Response(gen(), mimetype="text/event-stream")


# TODO decide whether to use polyfill for browsers with SSE (IE and Edge) options are:
# https://github.com/remy/polyfills/blob/master/EventSource.js
# https://github.com/rwaldron/jquery.eventsource
@app.route('/')
def page():
    return render_template("index.html")


@app.route('/latest.json')
def latest():
    """
    For legacy programs
    Creates the latest.json file
    :return:
    """
    return tracks_to_json(Track.query.order_by(Track.created_at).first())


@app.route('/details', methods=['GET'])
@app.route('/details/', methods=['GET'])
@app.route('/details/<int:page>', methods=['GET'])
def details(page=1):
    """
    Shows the in-station extra information
    :param page:
    :return: Starting page
    """
    tracks = models.Track.query.order_by(desc(Track.created_at)).paginate(page, itemsPerPage, False)
    # Formatting time for display
    for track in tracks.items:
        track.created_at = track.created_at.strftime("%x %I:%M %p")
    return render_template('index.html', tracks=tracks, detailed=True)


# TODO Refactor for SSE pushing
@app.route('/controls/addTrack')
def add_track(track):
    a_track = loads(track)
    db_track = Track(a_track['artist'], a_track['title'], a_track['group'],
                     a_track['time'], a_track['request'], a_track['requester'])
    db.session.add(db_track)
    db.session.commit()
    emit('addTracks', track, json=True, broadcast=True)


# TODO refactor for SSE pushing
@app.route('/controls/updateTrack')
def update_track(track):
    dict_track = loads(track)
    track_to_update = Track.query.get(dict_track['id'])
    for column in dict_track:
        setattr(track_to_update, column, dict_track[column])
    db.session.commit()


# TODO refactor for SSE pushing
@app.route('/controls/removeTrack')
def remove_track(track_id):
    track = Track.query.get(track_id)
    db.session.delete(track)
    db.session.commit()


# TODO refactor for SSE pushing
@app.route('/search')
def search_track(start=None, end=None, title=None, artist=None):
    results = Track.query
    if start is not None:
        results = results.filter_by(Track.time >= start)
    if end is not None:
        results = results.filter_by(Track.time <= end)
    if artist is not None:
        results = results.filter(Track.artist.like(artist))
    if title is not None:
        results = results.filter(Track.title.like(artist))


# watch over the database and push updates when rvdl or another source updates and it does not go through the server.
# note: this might not be a good idea if the application ever has to scale since constantly checking for updates to rows
# is taxing on databases, especially mysql. If performance is bad you will have to have this server listen to rvdl's
# command output over udp instead of querying the database directly for changes. This will increase performance in all
# accept a few edge cases. However whatever you do, DO NOT OPEN UP A TRANSACTION FOR EVERY REQUEST. This leads to
# a security and memory leak issue this application was designed to fix compared to the php version.

# TODO create exception and modify to use SSE
def db_overwatch():
    # TODO: have threaded function that connects to database, make updated tracks
    # query: SELECT * FROM Tracks JOIN Groups ON Tracks.group_id=Groups.id WHERE Tracks.created_at >= time;
    # repeat this query every few seconds, .
    # If not will have to keep a local copy cached to make sure duplicates are not sent.
    time = datetime.now()
    old_tracks = Track.query(Track.created_at >= time).all()
    while True:
        new_tracks = Track.query(Track.created_at >= time).all()  # get all newly created tracks since last check
        new_tracks = [track for track in new_tracks if track not in old_tracks]  # filter out already emitted tracks
        old_tracks = new_tracks + [track for track in old_tracks if track.created_at >= time]
        sleep(3)
    return db_overwatch()


def tracks_to_json(query):
    """
    Function for converting tracks to json and prettifying the
    json while debugging, switch to compact for deployment
    :param query:
    :return:
    """
    obj = []
    if isinstance(query, list):
        for track in query:
            obj.append({'id': track.id, 'artist': track.artist, 'title': track.title,
                        'time': track.created_at.strftime("%x %I:%M %p"), 'requester': track.requester,
                        'group': track.group.name})
    else:
        obj.append({'id': query.id, 'artist': query.artist, 'title': query.title,
                    'time': query.created_at.strftime("%x %I:%M %p"), 'requester': query.requester,
                    'group': query.group.name})
    if app.testing:
        return dumps(obj, sort_keys=True, indent=4)
    else:
        return dumps(obj, separators=(',', ':'))


if __name__ == '__main__':
    server = WSGIServer(("127.0.0.1", 5000), app)
    server.serve_forever()
    threading.Thread(db_overwatch())
