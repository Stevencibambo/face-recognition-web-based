# app/__init__.py

from flask_restplus import Api
from flask import Blueprint
from .main.controller.face_controller import api as face_ns

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='Face recognition system [REST API]',
          version='1.0.0',
          description='api for face recognition'
          )
api.add_namespace(face_ns)