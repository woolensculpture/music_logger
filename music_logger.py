from json import dumps, loads

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from track import Track, db

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret?"
socketio = SocketIO(app)


@app.route('/')
def Page():
    return render_template("index.html")


@socketio.on('connect')
def startup():
    tracks = Track.query.order_by(Track.time).limit(20).all()
    emit('addTrack', loads(tracks), json=True)


@socketio.on('addTrack')
def addTrack(track):
    aTrack = loads(track)
    dbTrack = Track(aTrack['artist'], aTrack['title'], aTrack['group'],
                    aTrack['time'], aTrack['request'], aTrack['requester'])
    db.session.add(dbTrack)
    db.session.commit()
    emit('addTrack', track, json=True, broadcast=True)


@socketio.on('updateTrack')
def updateTrack(track):
    dictTrack = loads(track)
    trackToUpdate = Track.query.get(dictTrack['id'])
    for column in dictTrack:
        setattr(trackToUpdate, column, dictTrack[column])
    db.session.commit()
    emit('updateTrack', track, json=True, broadcast=True)


@socketio.on('removeTrack')
def removeTrack(trackId):
    track = Track.query.get(trackId)
    db.session.delete(track)
    db.session.commit()
    emit('removeTrack', trackId, broadcast=True)


@socketio.on('query')
def searchTrack(start=None, end=None, title=None, artist=None, rangeStart=0, rangeEnd=20):
    results = Track.query
    if start is not None:
        results = results.filter_by(Track.time >= start)
    if end is not None:
        results = results.filter_by(Track.time <= end)
    if artist is not None:
        results = results.filter(Track.artist.like(artist))
    if title is not None:
        results = results.filter(Track.title.like(artist))
    emit('results', dumps(results.limit(20).all()), json=True)


if __name__ == '__main__':
    socketio.run(app)
    app.run()


# watch over the database and push updates when rvdl or another source updates and it does not go through the server.
# note: this might not be a good idea if the application ever has to scale since constantly checking for updates to rows
# is taxing on databases, especially mysql. If performance is bad you will have to have this server listen to rvdl's
# command output over udp instead of querying the database directly for changes. This will increase performance in all
# accept a few edge cases. However whatever you do, DO NOT OPEN UP A TRANSACTION FOR EVERY REQUEST. This leads to
# a security and memory leak issue this application was designed to fix compared to the php version.
def dbOverwatch():
    # TODO: have threaded function that connects to database
    # query: SELECT * FROM Tracks JOIN Groups ON Tracks.group_id=Groups.id WHERE Tracks.Created_at >= time OR Tracks.Updated_at >= time;
    # repeat this query every few seconds or every minute depending if seconds are stored. If not will have to keep a local copy cached to
    # make sure duplicates are not sent.
    return
