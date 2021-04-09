import hashlib
import os
from app import db

hobbies = db.Table('hobbies',
                   db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id')),
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')))
events = db.Table('events',
                  db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')))
tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('event_id', db.Integer, db.ForeignKey('event.id')))


class User(db.Model):
    """App user, which used to create database table.

    Attributes:
        id: person identifier
        role: person status
        name: full name
        email: email address
        birthday: birthday date. Format: Y-m-d
        occupation: user occupation
        gender: 'male' or 'female'
        about: description of this user
        dateLockOut: date of lock out user ('Razban'). Format - UNIX
        hobbies: list of user hobbies
        events: list of events user participating in
        passhash: hash of the password
        avatar: link to database
    """
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum('admin',
                             'moderator',
                             'user',
                             name='role'), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    pass_hash = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    bdate = db.Column(db.Date)
    about = db.Column(db.Text)
    gender = db.Column(db.Enum('male', 'female', name='gender'))
    created_events = db.relationship('Event', backref='creator')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    achievements = db.relationship('Achievement',
                                   backref='user',
                                   lazy='dynamic')
    dateLockOut = db.Column(db.Date)
    avatar = db.Column(db.Text, nullable=False)

    # friends = db.relationship('User', lazy='dynamic')

    def __init__(self, name, email, password, role='user',
                 about='', avatar='default.png'):
        self.name = name
        self.set_email(email)
        self.set_password(password)
        self.role = role
        self.about = about
        self.avatar = avatar

    def set_email(self, value):
        self.email = value.lower()

    def set_password(self, value):
        self.pass_hash = User.hash_password(value)

    def create_event(self, event):
        event.people += self
        self.created_events.append(event)

    def comment(self, comment, event_id):
        comment.event_id = event_id
        self.comments.append(comment)

    @staticmethod
    def hash_password(password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_avatar_from_views(self):
        return os.path.join('static', 'avatar', self.avatar)

    def get_bdate(self):
        date = list(str(self.bdate).split('-'))
        return "{}.{}.{}".format(date[2], date[1], date[0])

    def __repr__(self):
        return '<User {}: name: \'{}\', ' \
               'email: \'{}\', ' \
               'role: \'{}\'>'.format(self.id,
                                      self.name,
                                      self.email,
                                      self.role)


class Hobby(db.Model):
    """Hobby of some users.

    Attributes:
        id: hobbies identifier
        name: short name
        description: detailed description
        people: list of people with this hobbies
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    people = db.relationship('User', secondary=hobbies,
                             backref=db.backref('hobbies', lazy='dynamic'))


class Event(db.Model):
    """Event on the map.

    Attributes:
        id: event identifier
        lat: latitude
        lng: longtitude
        name: short name
        description: detailed description
        date: date of event
        creator_id: DB id of the creator
        creator: creator of this event
        people: list of people participating in this event
        tags: list of tags of this event
        comments: list of comments
    """
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    coords = property()
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    date_time = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people = db.relationship('User', secondary=events,
                             backref=db.backref('events', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('events', lazy='dynamic'))
    comments = db.relationship('Comment', backref='event', lazy='dynamic')

    @coords.setter
    def coords(self, coords):
        self.lat, self.lng = coords

    @coords.getter
    def coords(self):
        return self.lat, self.lng

    def __init__(self, creator_id, name, date_time, coords, desc=''):
        self.creator_id = creator_id
        self.people.append(User.query.get(creator_id))
        self.coords = coords
        self.name = name
        self.date_time = int(date_time)
        self.description = desc

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_comment(self, comment):
        self.comments.append(comment)

    def add_user(self, user):
        self.people.append(user)

    def __repr__(self):
        return '<Event id: {id}, ' \
               'name: {name}, ' \
               'date: {date_time}, ' \
               'description: {desc}>'.format(id=self.id,
                                             name=self.name,
                                             date_time=self.date_time,
                                             desc=self.description)


class Tag(db.Model):
    """Tag for event. Just text string"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag name: {}>'.format(self.name)


class Invitation(db.Model):
    """Invitations

    Attributes:
        event_id: event identifier
        description: detailed description
    """
    event_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)


class Achievement(db.Model):
    """Achievements of users

    Attributes:
        id: achievement identifier
        type: type of achievement
        n: amount of elementary actions enough to get achievement

        Types of achievements:
            distance: total distance traversed by user
            taken_events: total number of completed events
            friends_number: number of user friends
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('distance', 'taken_events', 'friends_number',
                             name='ach_type'))
    n = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Route(db.Model):
    """Route of bike path/event/user

    Attributes:
        id: route identifier
        name: short name
        description: detailed description
        cover_photo: cover photo of Route
        route_time: full time of route
        distance: full distance of route, format - km
        coating: type of coating. Params: asphalt, ground, bike lane
        api_access_token_url: api_access_token_url to kml file

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    cover_photo = db.Column(db.Text)
    route_time = db.Column(db.Time)
    distance = db.Column(db.Float)
    coating = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    points = db.relationship('Point', backref='route', lazy='dynamic')
    url = db.Column(db.Text)

    def __init__(self, creator_id, name, desc=''):
        self.creator_id = creator_id
        self.name = name
        self.description = desc

    def set_points(self, points):
        self.points = points


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    cover_photo = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    coords = property()
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))

    @coords.setter
    def coords(self, coords):
        self.lat, self.lng = coords

    @coords.getter
    def coords(self):
        return self.lat, self.lng

    def __init__(self, coords, route_id):
        self.coords = coords
        self.route_id = route_id


class Structure(db.Model):
    """Structure"""
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.Enum('tire', 'rent', 'workshop',
                             'emergency room', name='type'),
                     nullable=False)


class Comment(db.Model):
    """Comments to events

    Attributes:
        id: comment identifier
        content: content of the comment
        time: creation date of the comment
        user: user who wrote the comment
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __init__(self, user_id, body, time):
        self.user_id = user_id
        self.body = body
        self.time = time

    def __repr__(self):
        return '<Comment id: {id}, ' \
               'user_id: {user_id}, ' \
               'event_id: {event_id}, time: {time}, body: {body}>'.format(
            id=self.id,
            user_id=self.user_id,
            event_id=self.event_id,
            time=self.time,
            body=self.body)


class Quest(db.Model):
    """Quest

    Attributes:
        id: quest identifier
        type: type of quest
        time: date of quest. Format - unix
        distance: all distance of quest in meters
        start_lat: start point. Latitude
        start_lng: start point. Longitude
        end_lat: end point. Latitude
        end_lng: end point. Longitude
        description: detailed description
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text)
    time = db.Column(db.DateTime)
    distance = db.Column(db.Float)
    start_lat = db.Column(db.Float, nullable=False)
    start_lng = db.Column(db.Float, nullable=False)
    end_lat = db.Column(db.Float, nullable=False)
    end_lng = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
