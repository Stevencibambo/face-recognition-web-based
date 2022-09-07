# import the necessary package

from app.main import db
from app.main.model.face_image import FaceImage
from app.test.base import BaseTestCase

import unittest
import datetime

class TestFaceImageModel(BaseTestCase):

    def test_encode_auth_token(self):
        """* test encode authenticate token :"""
        face = FaceImage(
            uid=1,
            label='student',
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(face)
        db.session.commit()
        auth_token = face.encode_auth_token(face.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        """* test decode authenticate token :"""
        face = FaceImage(
            uid=1,
            label='student',
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(face)
        db.session.commit()
        auth_token = face.encode_auth_token(face.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(FaceImage.decode_auth_token(auth_token.decode("utf-8")) == 1)

if __name__ == '__main__':
    unittest.main()