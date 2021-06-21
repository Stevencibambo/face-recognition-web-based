# import the necessary package

import os

# DIR VARIABLE
APP = 'app'
MODEL_NET = 'modelnet'
DETECTOR = "face_detector"
PROCESS_DATA = 'processdata'
BASEDATA = 'basedata'
TRAIN = 'train'
VAL = 'val'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PROCESS_DATA_DIR = os.path.sep.join([APP, MODEL_NET, PROCESS_DATA])
BASE_DATA_DIR = os.path.sep.join([APP, MODEL_NET, BASEDATA])
MODEL_DIR = os.path.sep.join([APP, MODEL_NET, 'model'])
MODEL_FACENET = os.path.sep.join([APP, MODEL_NET, 'model', 'model'])
PROTO_PATH = os.path.sep.join([APP, MODEL_NET, DETECTOR, "deploy.prototxt"])
MODEL_PATH = os.path.sep.join([APP, MODEL_NET, DETECTOR, "res10_300x300_ssd_iter_140000.caffemodel"])

# DB URL FOR MYSQL
DATABASE_URI = "mysql+pymysql://admin:admin@localhost/face_reco"

# GET A SECRET KEY
SECRET_KEY = os.urandom(59).hex()

os.environ['DATABASE_URI'] = DATABASE_URI
os.environ['SECRET_KEY'] = SECRET_KEY

mysql_local_base = os.environ.get('DATABASE_URI')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.environ.get('SECRET_KEY'))
    DEBUG = False

    # using for development mode

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = mysql_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # using for testing mode


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'eproc_api_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# using for production mode
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = mysql_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
key = Config.SECRET_KEY
