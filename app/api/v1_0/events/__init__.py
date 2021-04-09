from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from app import (models, db)
from app.api.v1_0 import check_fields

access_fields = {'id',
                 'name', 'description',
                 'date_time', 'coords',
                 'creator_id', 'people'}


def parse(o, fields):
    dct = {}
    for f in fields:
        if f == 'people':
            dct[f] = [u.id for u in getattr(o, f)]
        else:
            dct[f] = getattr(o, f)
    return dct


class Events(Resource):
    decorators = [jwt_required]

    @staticmethod
    def parse(o, fields):
        if fields == {'id'}:
            return o.id
        return parse(o, fields)

    def get(self):
        fields = set(request.args.get('fields', 'id').split(','))
        fields = check_fields(fields, access_fields)
        coords = request.args.get('coords')
        search = request.args.get('search')
        if coords:
            try:
                coords = list(map(float, coords.split(',')))
            except ValueError:
                return abort(400, 'Bad coords.')
            if len(coords) != 4:
                return abort(400, 'Bad coords.')
            events = models.Event.query.filter(models.Event.lat >= coords[0]) \
                .filter(models.Event.lng >= coords[1]) \
                .filter(models.Event.lat <= coords[2]) \
                .filter(models.Event.lng <= coords[3]).all()
        else:
            events = models.Event.query.all()
        # if search:
        #     events += models.Event.query.filter()

        res = [Events.parse(e, fields) for e in events]
        return res

    def post(self):
        """
        Create an event.
        Required json data:

            lat: latitude
            lng: longtitude
            name: short name
            description: detailed description
            date: date of event
            tags: list of tags of this event
        :return: 
        """
        data = request.get_json()
        creator_id = get_jwt_identity().get('id')
        name = data.get('name')
        date_time = data.get('date_time')
        desc = data.get('desc', '')
        coords = data.get('coords')
        if not all([creator_id, name, date_time, coords]):
            return abort(400, 'Bad params.')
        event = models.Event(creator_id, name, date_time, coords, desc=desc)
        db.session.add(event)
        db.session.commit()
        return {'id': event.id}, 201


class Event(Resource):
    decorators = [jwt_required]

    @staticmethod
    def parse(o, fields):
        if fields == {'id'}:
            return {'id': o.id, 'name': o.name}
        return parse(o, fields)

    def get(self, event_id):
        fields = set(request.args.get('fields', 'id').split(','))
        fields = check_fields(fields, access_fields)
        e = models.Event.query.get_or_404(event_id)
        res = Event.parse(e, fields)
        return res

    def put(self, event_id):
        e = models.Event.query.get_or_404(event_id)
        if not (e.creator_id == get_jwt_identity().get('id')
                or get_jwt_identity().get('role') in (
                    'moderator', 'admin')):
            return abort(403, 'You do not have permission to do this.')
        data = request.get_json()
        name = data.get('name')
        date_time = data.get('date_time')
        desc = data.get('desc')
        coords = data.get('coords')
        if name:
            e.name = name
        if date_time:
            e.date_time = date_time
        if desc:
            e.description = desc
        if coords:
            e.coords = coords
        db.session.add(e)
        db.session.commit()
        return {'message': 'Event has been successfully updated.'}, 200

    def delete(self, event_id):
        e = models.Event.query.get_or_404(event_id)
        if not e:
            return abort(404, 'There is no event with this id.')
        if get_jwt_identity().get('id') != e.creator_id \
                and get_jwt_identity().get('role') not in (
                        'moderator', 'admin'):
            return abort(403, 'You do not have permission to do this.')
        db.session.delete(e)
        db.session.commit()
        return {'message': 'Event has been successfully deleted.'}, 200

    def post(self, event_id):
        e = models.Event.query.get_or_404(event_id)
        user_id = get_jwt_identity().get('id')
        u = models.User.query.get(user_id)
        e.add_user(u)
        db.session.add(e)
        db.session.commit()
        return {'message': 'User '+str(user_id) + ' participate in event ' + str(event_id)}, 200
