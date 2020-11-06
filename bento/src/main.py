import os
import tensorflow as tf

from src.tensorfood_classifier import TensorfoodClassifier

if __name__ == "__main__":
  
  model_path = 'models/tensorfood.h5'  
  model = tf.keras.models.load_model(model_path)

  # Create a iris classifier service instance
  tensorfood_service = TensorfoodClassifier()

  # Pack the newly trained model artifact
  tensorfood_service.pack('model', model)

  # Save the prediction service to disk for model serving
  saved_path = tensorfood_service.save()