from datetime import date
from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db, models
from app.api.v1_0 import check_fields

access_fields = {'id', 'name',
                 'email', 'bdate',
                 'created_events',
                 'about', 'email',
                 'events', 'comments'}


def parse(o, fields):
    dct = {}
    for f in fields:
        if f == 'events':
            dct[f] = [e.id for e in getattr(o, f)]
        elif f == 'created_events':
            dct[f] = [e.id for e in getattr(o, f)]
        elif f == 'comments':
            dct[f] = [c.id for c in getattr(o, f)]
        elif f == 'bdate':
            bdate = o.bdate
            print(bdate)
            dct[f] = str(bdate.day) + \
                     '.' + str(bdate.month) + \
                     '.' + str(bdate.year)
        else:
            dct[f] = getattr(o, f)
    return dct


class Users(Resource):
    decorators = [jwt_required]

    @staticmethod
    def parse(o, fields):
        if fields == {'id'}:
            return o.id
        return parse(o, fields)

    def get(self):
        fields = set(request.args.get('fields', 'id').split(','))
        fields = check_fields(fields, access_fields)
        users = models.User.query
        res = [Users.parse(u, fields) for u in users]
        return res

    def post(self):
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)
        name = data.get('name', None)
        if not (username and password and name):
            return abort(400, 'Bad Request')
        if models.User.query.filter_by(email=username).first():
            return abort(409, 'This username already exists.')
        if models.User.query.filter_by(name=name).first():
            return abort(409, 'This name already exists.')
        user = models.User(name, username, password)
        db.session.add(user)
        db.session.commit()
        uid = models.User.query.filter_by(email=username).first().id
        return {'id': uid}, 201


class User(Resource):
    decorators = [jwt_required]

    @staticmethod
    def parse(o, fields):
        if fields == {'id'}:
            return {'id': o.id, 'name': o.name}
        return parse(o, fields)

    def get(self, user_id):
        fields = set(request.args.get('fields', 'id').split(','))
        fields = check_fields(fields, access_fields)
        u = models.User.query.get_or_404(user_id)
        res = User.parse(u, fields)
        return res

    def put(self, user_id):
        if get_jwt_identity().get('id') != user_id:
            return abort(403)
        u = models.User.query.get_or_404(user_id)
        if not u:
            return abort(404)
        params = request.get_json().get('params')
        if not params:
            return abort(400)
        for field in params:
            if field == 'username':
                if not models.User.query.get(user_id).email == params['username'] and \
                        models.User.query.filter_by(email=params['username']):
                    return abort(406)
                u.email = params['username']
            elif field == 'bdate':

                u.bdate = date(params['bdate'].split('.').day,
                               params['bdate'].split('.').month,
                               params['bdate'].split('.').year)
            else:
                setattr(u, field, params[field])
        db.session.add(u)
        db.session.commit()
        return {'message': 'User has been successfully updated.'}

    def delete(self, user_id):
        if get_jwt_identity().id != user_id:
            return abort(403)
        db.session.delete(models.User.query.get(user_id))
        db.session.commit()
        return {'message': 'User has been successfully deleted.'}
