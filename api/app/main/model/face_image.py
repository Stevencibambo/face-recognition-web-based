# import the necessary package
from .. import db

class FaceImage(db.Model):
    """FaceImage Model for storing face details"""
    __tablename__ = 'face_image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    label = db.Column(db.String(100), nullable=False, unique=True)
    accuracy = db.Column(db.Float, nullable=True)
    recall = db.Column(db.Float, nullable=True)
    registered_on = db.Column(db.BigInteger)
    updated_on = db.Column(db.BigInteger, nullable=True)

    def __repr__(self):
        return "<Face {}>".format(self.label)