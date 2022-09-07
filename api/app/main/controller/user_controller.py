#import the necessary package

from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, update_user

api = UserDto.api
_user = UserDto.user
_user_update = UserDto.user_update

@api.route('/')
@api.doc('list_of_registered_users')
class UserList(Resource):
    @api.response(201, 'Users retrieved successful')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

@api.route('/add')
@api.doc('create new user')
class User(Resource):
    @api.response(201, 'User successfully created')
    @api.expect(_user, validate=True)
    def post(self):
        """creates a new User"""
        data = request.json
        return save_new_user(data=data)

@api.route('/<username>')
@api.param('username', 'User name')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_list_with(_user, envelope='data')
    def get(self, username):
        """get a user given its identifier"""
        user = get_a_user(username)
        if not user:
            api.abort(404)
        else:
            response_object = {
                'status': 'success',
                'message': 'request successfuly'
            }
            return user

@api.route('/<username>/update')
@api.doc("update user's informations")
class User(Resource):
    @api.expect(_user_update, validate=True)
    def put(self, username):
        """Update user's informations"""
        data = request.json
        return update_user(username, data=data)