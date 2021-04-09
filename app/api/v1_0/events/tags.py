from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app import models


class Tags(Resource):
    decorators = [jwt_required]

    def get(self):
        tags = models.Tag.query.all()
        res = [{'id': tag.id, 'name': tag.name} for tag in tags]
        return res

    def post(self):
        return 'Tags post'


class Tag(Resource):
    decorators = [jwt_required]

    def get(self, tag_id):
        tag = models.Tag.query.get(tag_id)
        if not tag:
            return {
                'error': {
                    'code': 404,
                    'message': 'Not found'
                }
            }
        return {'id': tag.id,
                'name': tag.name}

    def post(self, tag_id):
        return str(tag_id) + ' Tag post'
