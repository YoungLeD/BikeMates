from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db, models
from app.api.v1_0 import check_fields

access_fields = {'id', 'name', 'creator_id', 'desc', 'points'}


def parse(o, fields):
    dct = {}
    for f in fields:
        if f == 'desc':
            dct[f] = getattr(o, 'description')
        elif f == 'points':
            dct[f] = [getattr(p, 'coords') for p in getattr(o, f)]
        else:
            dct[f] = getattr(o, f)
    return dct


class Routes(Resource):
    decorators = [jwt_required]

    @staticmethod
    def parse(o, fields):
        if fields == {'id'}:
            return o.id
        return parse(o, fields)

    def get(self):
        fields = set(request.args.get('fields', 'id').split(','))
        fields = check_fields(fields, access_fields)
        routes = models.Route.query
        res = [Routes.parse(r, fields) for r in routes]
        return res

    def post(self):
        data = request.get_json()
        creator_id = get_jwt_identity().get('id')
        name = data.get('name')
        points = data.get('points')
        desc = data.get('desc')
        if not (creator_id and name and points):
            return abort(400, 'Bad request.')
        r = models.Route(creator_id, name, desc=desc)
        db.session.add(r)
        db.session.commit()
        points = [models.Point(point, r.id) for point in points]
        r.set_points(points)
        for point in points:
            db.session.add(point)
        db.session.commit()
        return {'id': r.id}, 201


class Route(Resource):
    decorators = [jwt_required]

    @staticmethod
    def parse(o, fields):
        if fields == {'id'}:
            return {'id': o.id, 'name': o.name}
        return parse(o, fields)

    def get(self, route_id):
        fields = set(request.args.get('fields', 'id').split(','))
        fields = check_fields(fields, access_fields)
        r = models.Route.query.get_or_404(route_id)
        res = Route.parse(r, fields)
        return res

    def put(self, route_id):
        r = models.Route.query.get_or_404(route_id)
        if not (r.creator_id == get_jwt_identity().get('id')
                or get_jwt_identity().get('role') in (
                    'moderator', 'admin')):
            return abort(403, 'You do not have permission to do this.')
        data = request.get_json()
        name = data.get('name')
        desc = data.get('desc')
        points = data.get('points')
        if name:
            r.name = name
        if desc:
            r.description = desc
        if points:
            for point in r.points:
                db.session.delete(point)
            points = [models.Point(point, r.id) for point in points]
            r.set_points(points)
        db.session.add(r)
        db.session.commit()
        return {'message': 'Event has been successfully updated.'}, 200

    def delete(self, route_id):
        r = models.Route.query.get_or_404(route_id)
        if get_jwt_identity().get('id') != r.creator_id \
                and get_jwt_identity().get('role') not in (
                        'moderator', 'admin'):
            return abort(403, 'You do not have permission to do this.')
        db.session.delete(r)
        db.session.commit()
        return {'message': 'Event has been successfully deleted.'}, 200
