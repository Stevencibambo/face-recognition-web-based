# import the necessary package

import numpy as np

class Features:
    def __init__(self, model):
        self.model = model

    def extract_feature(self, face_pixels):
        # scale pixel values
        face_pixels = face_pixels.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean)
        # transform face into one sample
        samples = np.expand_dims(face_pixels, axis=0)

        # make prediction and return embedding
        yhat = self.model.predict(samples)

        return yhat[0]

    def get_embedding(self, face_pixels):
        embeddings = list()
        for face in face_pixels:
            emb = self.extract_feature(face)
            embeddings.append(emb)

        embeddings = np.asarray(embeddings)
        # return list of embedding faces
        return embeddings