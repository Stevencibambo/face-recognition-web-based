# import the necessary package


from keras.models import load_model
from flask import jsonify
from sqlalchemy import update
from app.modelnet import preprocessing
from app.main.util.process_train import training, processing
from app.modelnet.embedding import Features
from app.modelnet.preprocessing import Processing
from app.main.model.tokens import Token
from app.main.service.user_service import get_a_user
from app.main import config
from app.main import db
import numpy as np
import shutil
import os

def model_training(username, data):
    """system user's model training"""
    user = get_a_user(username)
    if user:
        # check if the access token is valid
        auth_token = Token.check_token(data['access_token'])
        if auth_token:
            processing(username=username) # process data before train the model
            training(username=username)

            response_object = {
                'status': 'success',
                'message': 'model training sucessful'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Invalid access login. Please login again!'
            }
            return response_object, 401
















 # initializing process object
 #        proc = Processing(protoPath=config.PROTO_PATH, modelPath=config.MODEL_PATH, confidence=0.5)
 #        path_data = os.path.sep.join([config.BASE_DATA_DIR, config.TRAIN, data['label']])
 #        # load face to one directory
 #        face_data = proc.load_faces(path_data)
 #        labels = [data['label'] for _ in range(len(faces))]
 #        print('>> loaded %d examples for class: %s' % (len(face_data), data['label']))
 #
 #            data = np.load(os.path.sep.join([config.APP, config.MODEL_NET,
 #                                             config.PROCESS_DATA, "training_data.npz"]))
 #            X, y = data['arr_0'], data['arr_1']
 #            X = X.tolist()
 #            y = y.tolist()
 #            X.extend(face_data)
 #            y.extend(labels)
 #
 #            print("[INFO] saved training data {} samples ...".format(len(X)))
 #            np.savez_compressed(os.path.join(config.APP, config.MODEL_NET,
 #                                             config.PROCESS_DATA, "training_data.npz"), np.asarray(X), np.asarray(y))
 #
 #            print("[INFO] loading model facenet model for features extraction...")
 #            facenet_model = load_model(os.path.sep.join([config.APP, config.MODEL_NET,
 #                                                         config.MODEL_FACENET, 'facenet_keras.h5']))
 #
 #            feature = Features(facenet_model)
 #            # extract feature
 #            print("[INFO] features extraction samples training data {}".format(len(X)))
 #            embed_face = feature.get_embedding(face_data)
 #            data = np.load(os.path.sep.join([config.APP, config.MODEL_NET,
 #                                             config.PROCESS_DATA, "embedding_face.npz"]))
 #            newTrain, ytrain = data['arr_0'], data['arr_1']
 #            newTrain = newTrain.tolist()
 #            ytrain = ytrain.tolist()
 #
 #            newTrain.extend(embed_face)
 #            ytrain.extend(np.asarray(labels))
 #
 #            print("[INFO] save embedding data ...")
 #            np.savez_compressed(os.path.sep.join([config.APP, config.MODEL_NET,
 #                                                  config.PROCESS_DATA, "embedding_face.npz"]),
 #                                np.asarray(newTrain), np.asarray(ytrain))
 #            # call training method to retrain and saved model with a new data
 #            resp = training(new=True, label=data['label'])