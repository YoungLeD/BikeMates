from datetime import datetime

from flask import (abort, request)
from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask_login import login_user
from flask_restful import Resource

from app import app, models


class Auth(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not (username and password):
            return abort(400, 'Bad request')
        u = models.User.query.filter_by(email=username).first()
        if not (u and u.pass_hash == models.User.hash_password(password)):
            return abort(401, 'Bad username or password')
        login_user(u)  # должно быть в sign_in()
        access_token = create_access_token(identity={'id': u.id,
                                                     'role': u.role})
        refresh_token = create_refresh_token(identity={'id': u.id,
                                                       'role': u.role})
        return {'access_token': access_token,
                'access_token_expires_at': int((datetime.now() + app.config['JWT_ACCESS_TOKEN_EXPIRES']).timestamp()),
                'refresh_token': refresh_token,
                'refresh_token_expires_at': int((datetime.now() + app.config['JWT_REFRESH_TOKEN_EXPIRES']).timestamp())
                }
