# entry point of the application
# import the necessary packages

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from keras.models import load_model
from app.main import create_app, db
from app.main.util.process_train import processing, training, evaluation
from app.modelnet.preprocessing import Processing
from app.modelnet.embedding import Features
from app import blueprint
from app.main import config
from app.main.model import face_image
import numpy as np
import unittest
import pickle
import os

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    """set hot to default address to allow up coming request from anywhere"""
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)

@manager.command
def test():
    """Runs the unit tests"""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def proc():
    """Runs the processing data and save it"""
    processing()

@manager.command
def train():
    """ run the training of the model"""
    training()

@manager.command
def eval():
   """ evaluate the model"""
   evaluation()

if __name__ == '__main__':
    manager.run()