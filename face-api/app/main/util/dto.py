# import the necessary package
from flask_restplus import Namespace, fields

class FacesDto:
    api = Namespace('face', description='face related operations')
    face = api.model('get_faces_details', {
        'label': fields.String(required=True, description='face label'),
        'access_token': fields.String(required=True, description='authorization key')
    })
    face_ver = api.model('face_verified', {
        'access_token': fields.String(required=True, description='valid access_token'),
        'label': fields.String(required=True, description='face label'),
        'verified': fields.Integer(required=True, description='face verification value')
    })
    face_regis = api.model('registration_details', {
        'label': fields.String(required=True, description='first and last name of the user'),
        'face': fields.String(required=True, description='all faces for a user')
    })
    face_auth = api.model('predict_details', {
        'face': fields.String(required=True, description='student face descriptor')
    })

class ModelDto:
    api = Namespace('model', description='model related operations')
    user = api.model('model', {
        'access_token': fields.String(required=True, description='valid access token')
    })