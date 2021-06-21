# import the necessary package

from mtcnn.mtcnn import MTCNN
from PIL import Image
import numpy as np
import cv2
import os

class Processing:

    def __init__(self, protoPath, modelPath, confidence=0.5):
        self.protoPath = protoPath
        self.modelPath = modelPath
        self.confidence = confidence
        self.net = cv2.dnn.readNetFromCaffe(self.protoPath, self.modelPath)

    # Return a numpy array of a cropped face
    # if the given file is whole image
    def face_extraction(self, filename, required_size=(160, 160)):
        image = cv2.imread(filename)
        image = cv2.resize(image, (600, 600))
        # convert to array
        (w, h) = image.shape[:2]

        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)),
                                 1.0, (300, 300), (104.0, 177.0, 123.0))
        # pass the blob through the network and obtain the detections and
        # predictions
        self.net.setInput(blob)
        detections = self.net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract  the confidence (i.e, probability) associated with the prediction
            confidence = detections[0, 0, i, 2]
            # filter out weak detections
            if confidence > self.confidence:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # ensure the detected bounding box does fall outside the
                # dimensions of the frame
                startX = max(0, startX)
                startY = max(0, startY)
                endX = min(w, endX)
                endY = min(h, endY)
                print(startX, startY, endX, endY)

                # extract the face ROI and then preprocess it in the exact
                # same manner as our training DATA

                face = image[startY:endY, startX:endX]
                face = np.array(face, dtype="uint8")
                image = Image.fromarray(face)
                image = image.resize(required_size)
                face_array = np.asarray(image)
            return face_array

        return image

    # return the numpy array as the the function below
    # use this function when MTCNN working well, otherwise
    # use below function
    def extract_face(sel, filename, required_size=(160, 160)):
        # load image from file
        image = Image.open(filename)
        #convert to RGB, if needed
        image = image.convert('RGB')
        # convert to array
        pixels = np.asarray(image, dtype='uint8')

        detector = MTCNN()
        # detect faces in the image
        results = detector.detect_faces(pixels)

        # extract the boundig box from the first face
        x1, y1, width, height, = results[0]['box']
        # bug fix
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        # extract the face
        face = pixels[y1:y2, x1:x2]
        # resize pixels to the model size
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = np.asarray(image)

        #return cropped face
        return face_array

    # use this function if the given image
    # is cropped yet
    def get_face_data(self, filename, required_size=(160, 160)):
        # load image
        image = Image.open(filename)
        image = image.convert('RGB')
        image = image.resize(required_size)
        face_array = np.asarray(image, dtype='uint8')

        #return numpy array as face
        return face_array

    def load_faces(self, directory):
        faces = list()
        # enumerate file
        for filename in os.listdir(directory):
            if filename.endswith('jpg'):
                # path
                path = os.path.join(directory, filename)
                # get face
                face = self.get_face_data(path)
                # store
                faces.append(face)
            else:
                continue
        return faces

    def load_dataset(self, directory):
        X = list()
        y = list()
        # enumerate folders, on per class
        for subdir in os.listdir(directory):
            path = os.path.join(directory, subdir)
            # get face
            if not os.path.isdir(path):
                continue

            # load all faces in the subdirectory
            faces = self.load_faces(path)
            labels = [subdir for _ in range(len(faces))]
            # summarize progress
            print('>> loaded %d examples for class: %s' %(len(faces), subdir))

            # store
            X.extend(faces)
            y.extend(labels)
        # return data, labels
        return np.asarray(X), np.asarray(y)