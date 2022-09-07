# import the necessary package

from app.main import db
from app.main.service.user_service import get_a_user
from app.main.model.tokens import Token
from datetime import datetime

def save_token(token):
    # token = Token(token=token)
    try:
        db.session.add(token)
        db.session.commit()
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, 500

def check_token(access_token):
    """check if the token is opened"""
    token = Token.check_opened_token_by_token(access_token)
    if token:
        response_object = {
            'status': 'successful',
            'message': "token's state opened",
            'access_token': token.token
        }
        return response_object, 201
    else:
        response_object = {
            "status": "fail",
            "message": "token's status close",
            "access_token": ""
        }
        return response_object, 501

def token_is_opened(id):
    try:
        # get a user
        uid = int(id)
        if uid:
            # check if user don't have an opened session
            token = Token.check_opened_user_token(uid)
            if token:
                now = datetime.utcnow()
                timestamp = int(datetime.timestamp(now))
                if (timestamp - token.start_on) > (45 * 60 * 60):
                    # close first the opened token
                    token.status = 0
                    token.end_on = timestamp
                    db.session.commit()
                    return False
                else:
                    return True
            else:
                return False
    except Exception as e:
        response_object = {
            "status": "fail",
            "message": "error to close opened token",
            "error": e
        }
        return response_object, 501