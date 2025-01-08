from svnm.basemodels import ImageClassificationbaseModel
import tensorflow as tf
from tensorflow.keras.applications.mobilenet import preprocess_input
from svnm.preprocessing import load_and_preprocess_image
import numpy as np
import os
class GenderDetection(ImageClassificationbaseModel):
    def __init__(self):
        super().__init__("GenderDetection")
    def predict(self, filepath,conf=0.8):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Image file not found: {filepath}")
        
        try:
            image =load_and_preprocess_image(filepath)
            image=preprocess_input(image)
            image = tf.expand_dims(image, axis=0)
            results=self.model.predict(image)
            id = np.argmax(results[0])
            conf = results[0][id]
            label = self.classes.get(id, "Unknown")
            return label, conf
        except Exception as e:
            raise ValueError(f"Error during prediction: {e}")
    