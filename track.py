from music_logger import db


class Track(db.Model):
    id = db.Column(db.Integer(11), primary_key=True, autoincrement=True, nullable=False, unique=True)
    artist = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(255), nullable=True)
    time = db.Column(db.DateTime, nullable=True)
    rivendell = db.Column(db.Boolean, nullable=True)
    group_id = db.Column(db.Integer(11), db.ForeignKey('groups.id'), nullable=True)
    group = db.relationship('groups')
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    request = db.Column(db.Boolean, nullable=True)
    requester = db.Column(db.String(255), nullable=True)

    def __init__(self, tid, artist, title, rivendell, group_id, created_at, updated_at,
                 time, request=False, requester=None):
        self.id = tid
        self.artist = artist
        self.title = title
        self.rivendell = rivendell
        self.group_id = group_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.time = time
        self.request = request
        self.requester = requester

    def __repr__(self):
        return '<Track:artist %r, title %r, time %r>' % self.artist, self.title, self.created_at


class Group(db.Model):
    id = db.Column(db.Integer(11), primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, tid, name, created_at, updated_at):
        self.id = tid
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Group: %r>' % self.name
