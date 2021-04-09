from flask import make_response, abort
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app import app, csrf


# Fields support
def check_fields(fields, access_fields):
    """
    Returns intersection of sets and adds 'id' if doesn't exist
    :param fields: 
    :param access_fields: 
    :return: 
    """
    if not (fields <= access_fields):
        return abort(400)
    return fields | {'id'}


# JWT
jwt = JWTManager(app)

# APIs
# V1.0
api1_0 = Api(app, prefix='/api/v1.0', decorators=[csrf.exempt])


@api1_0.representation('application/json')
def output_json(data, code, headers=None):
    import json
    resp = make_response(json.dumps(data, sort_keys=True, indent=4), code)
    resp.headers.extend(headers or {})
    return resp


# auth
from app.api.v1_0 import auth

api1_0.add_resource(auth.Auth, '/auth')

# refresh_token
from app.api.v1_0 import refresh_token

api1_0.add_resource(refresh_token.RefreshToken, '/refresh_token')

# users
from app.api.v1_0 import users

api1_0.add_resource(users.Users, '/users')
api1_0.add_resource(users.User, '/users/<int:user_id>')

# events
from app.api.v1_0 import events

api1_0.add_resource(events.Events, '/events')
api1_0.add_resource(events.Event, '/events/<int:event_id>')

# events.tags
from app.api.v1_0.events import tags

api1_0.add_resource(tags.Tags, '/events/tags')
api1_0.add_resource(tags.Tag, '/events/tags/<int:tag_id>')

# routes
from app.api.v1_0 import routes

api1_0.add_resource(routes.Routes, '/routes')
api1_0.add_resource(routes.Route, '/routes/<int:route_id>')
