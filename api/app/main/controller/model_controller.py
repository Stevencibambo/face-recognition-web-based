# import the necessary package

from flask_restplus import Resource
from flask import request
from app.main.util.dto import ModelDto
from app.main.service.model_service import model_training

api = ModelDto.api
_user = ModelDto.user

@api.route('/<username>/train')
@api.param('username', 'Username')
@api.doc('training the model')
class Model(Resource):
    @api.expect(_user, validate=True)
    def post(self, username):
        """train the model"""
        data = request.json
        return model_training(username, data=data)