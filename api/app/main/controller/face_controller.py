# import the necessary package

from flask_restplus import Resource
from flask import request
from app.main.util.dto import FacesDto
from app.main.service.face_service import update_face, save_faces, predict

api = FacesDto.api
_face = FacesDto.face
_face_regis = FacesDto.face_regis
_face_auth = FacesDto.face_auth

@api.route('/regisapi')
@api.doc('register new face')
class FaceRegistration(Resource):
    @api.response(201, 'face saved successful')
    @api.expect(_face_regis, validate=True)
    def post(self):
        """registration of a new face"""
        data = request.json
        return save_faces(data)

@api.route('/predapi')
@api.doc('predict a face given in parameter')
class Face(Resource):
    @api.expect(_face_auth, validate=True)
    def post(self):
        """predict a given face in parameter"""
        data = request.json
        return predict(data=data)

@api.route('/updatapi')
@api.param('username', 'Username')
class Face(Resource):
    @api.expect(_face, validate=True)
    def put(self, username):
        """update the existing face"""
        data = request.json
        return update_face(username, data)