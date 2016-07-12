from json import dumps, loads

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from track import Track, db

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret?"
socketio = SocketIO(app)


@app.route('/')
@app.route('/details')
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
    emit('removeTrack', trackId, broadcast=True)


@socketio.on('search')
def searchTrack(start=None, end=None, title=None, artist=None):
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