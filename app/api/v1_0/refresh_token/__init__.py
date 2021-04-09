from datetime import datetime

from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token
from flask_restful import Resource

from app import app


class RefreshToken(Resource):
    decorators = [jwt_refresh_token_required]

    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity)
        return {'access_token': access_token,
                'expires_at': int((datetime.now() + app.config['JWT_ACCESS_TOKEN_EXPIRES']).timestamp())
                }
