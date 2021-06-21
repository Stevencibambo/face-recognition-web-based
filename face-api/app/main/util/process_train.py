# import the necessary package
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.svm import SVC
from keras.models import load_model
from flask import jsonify
from app.modelnet.preprocessing import Processing
from app.modelnet.embedding import Features
from app.main import config
import numpy as np
import pickle
import os

def processing():
    """data processing"""
    if not os.path.isdir(os.path.join(config.BASE_DATA_DIR)):
        raise 'data directory {} not found'.format(os.path.join(config.BASE_DATA_DIR))

    proc = Processing(protoPath=config.PROTO_PATH, modelPath=config.MODEL_PATH, confidence=0.5)
    path_data = os.path.join(config.BASE_DATA_DIR)
    Xtrain, ytrain = proc.load_dataset(path_data)
    # Xtest, ytest = proc.load_dataset(os.path.sep.join([config.BASE_DATA_DIR, config.VAL]))

    processed_data = os.path.join(config.PROCESS_DATA_DIR)
    if not os.path.isdir(processed_data):
        os.mkdir(processed_data)

    print("[INFO] saved training data {} samples ...".format(Xtrain.shape[0]))
    np.savez_compressed(os.path.join(processed_data, "training_data.npz"), Xtrain, ytrain)

    data = np.load(os.path.join(processed_data, "training_data.npz"))
    # test_data = np.load(os.path.sep.join([config.APP, config.MODEL_NET, config.PROCESS_DATA, 'val_data.npz']))
    Xtrain, ytrain = data['arr_0'], data['arr_1']
    # Xtest, ytest = test_data['arr_0'], test_data['arr_1']
    # split data in train and test samples
    # Xtrain, Xtest, ytrain, ytest = train_test_split(Xtrain, ytrain, test_size=.20, random_state=42)

    print("[INFO] loading model facenet model for features extraction...")
    facenet_model = load_model(os.path.join(config.MODEL_FACENET, 'facenet_keras.h5'))
    feature = Features(facenet_model)

    # extract feature
    print("[INFO] features extraction samples training data {}".format(Xtrain.shape[0]))
    newTrain = feature.get_embedding(Xtrain)
    # newTest = feature.get_embedding(Xtest)

    print("[INFO] save embedding data ...")
    np.savez_compressed(os.path.sep.join([config.PROCESS_DATA_DIR,
                                          "embedding_face.npz"]), newTrain, ytrain)
    print("[INFO] saved test data ...")
    print(newTrain.shape, ytrain.shape)
    # np.savez_compressed(os.path.join(processed_data, 'val_data.npz'), Xtest, ytest)
    if Xtrain.shape[0] > 0:
        response_object = {
            'status': 'success',
            'message': 'data processed successfully',
            'size': Xtrain.shape[0]
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'error during data processing'
        }
        return response_object, 400

def training(new=False, label=''):
    """ loading embedding data for training"""
    data = np.load(os.path.join(config.PROCESS_DATA_DIR, 'embedding_face.npz'))
    Xtrain, ytrain = data['arr_0'], data['arr_1']
    #split data to training and testing samples
    Xtrain, Xtest, ytrain, ytest = train_test_split(Xtrain, ytrain, test_size=.33, random_state=42)

    # normalize input vector
    print("[INFO] normalize input vectors ...")
    in_encoder = Normalizer(norm='l2')
    Xtrain = in_encoder.transform(Xtrain)
    Xtest = in_encoder.transform(Xtest)

    # label encoder targets
    print("[INFO] encoding label target ...")
    out_encoder = LabelEncoder()
    out_encoder.fit(ytrain)
    ytrain = out_encoder.transform(ytrain)
    ytest = out_encoder.transform(ytest)

    # save label encoder targets
    processed_data = os.path.join(config.PROCESS_DATA_DIR)
    if not os.path.isdir(processed_data):
        os.mkdir(processed_data)
    pickle.dump(out_encoder, open(os.path.join(processed_data, "encoder_label.pickle"), 'wb'))

    # fit model
    print("[INFO] training SVM model ...")
    model = SVC(kernel='poly', degree=8, probability=True, random_state=42)
    model.fit(Xtrain, ytrain)

    print("[INFO] saved model ...")
    path_model = os.path.join(config.MODEL_DIR)
    if not os.path.isdir(path_model):
        os.mkdir(path_model)
    pickle.dump(model, open(os.path.join(path_model, "model.pickle"), 'wb'))

    # model evaluation with new data
    preds = model.predict(Xtest)

    # score
    score = accuracy_score(ytest, preds)

    # summarize
    print("[INFO] Model evaluation ...")
    # print(confusion_matrix(ytest, preds))
    report = classification_report(ytest, preds)
    print(report)
    acc = "[INFO] Accuracy: train=%.3f" % (score * 100)
    if new:
        encode = out_encoder.inverse_transform(model.classes_)
        classes_ = model.classes_
        index = np.where(encode == label)
        val = classes_[index]
        ind = np.where(classes_ == val)

        # calcute precision and recall
        precision = precision_score(ytest, preds, average=None)[ind[0]]
        recall = recall_score(ytest, preds, average=None)[ind[0]]
        response_object = {
            'status': 'successful',
            'message': 'class report classification',
            'class': label,
            'precision': precision,
            'recall': recall
        }
        return response_object
    else:
        print(acc)
        return acc

def evaluation():
    """evaluate the model using randomly same examples"""
    model = pickle.load(open(os.path.sep.join([config.MODEL_DIR, 'model.pickle']), 'rb'))
    processed_data = os.path.join(config.PROCESS_DATA_DIR)
    encoder_label = pickle.load(open(os.path.join(processed_data, 'encoder_label.pickle'), 'rb'))
    data = np.load(os.path.join(processed_data, 'embedding_face.npz'))
    embed = data['arr_0']
    # test model on a random example from the test dataset
    index = np.random.choice([i for i in range(embed.shape[0])])
    random_face_emb = embed[index]

    sample = np.expand_dims(random_face_emb, axis=0)
    yhat_class = model.predict(sample)
    yhat_proba = model.predict_proba(sample)
    print(model.classes_)
    print(encoder_label.inverse_transform(model.classes_))
    class_index = yhat_class[0]
    class_probability = yhat_proba[0, class_index] * 100
    predicct_name = encoder_label.inverse_transform(yhat_class)
    disp = 'Predicted: %s (%.3f)' % (predicct_name[0], class_probability)
    print(disp)