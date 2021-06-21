# import the necessary package

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from keras.models import load_model
from . import config
from ..modelnet.embedding import Features
import numpy as np
import pickle
import os
from ..modelnet.preprocessing import Processing

db = SQLAlchemy()
flask_bcryp = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config.config_by_name[config_name])
    db.init_app(app)
    flask_bcryp.init_app(app)

    return app

