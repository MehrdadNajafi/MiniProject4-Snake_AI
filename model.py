import numpy as np
import tensorflow as tf

class Model:
    def __init__(self):
        self.model = tf.keras.models.load_model("Model\Snake_AI.h5")
    
    def predict_direction(self, x_test):
        dir_pred = self.model.predict(np.array([x_test]))
        return np.argmax(dir_pred)