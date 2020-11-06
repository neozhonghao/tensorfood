import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image

from bentoml import api, artifacts, env, BentoService
from bentoml.adapters import FileInput, ImageInput
from bentoml.frameworks.tensorflow import TensorflowSavedModelArtifact

FOODS = ['chilli_crab', 'curry_puff', 'dim_sum', 'ice_kacang', 'kaya_toast',
         'nasi_ayam', 'popiah', 'roti_prata', 'sambal_stingray', 'satay',
         'tau_huay', 'wanton_noodle']

@env(requirements_txt_file='requirements.txt')
@artifacts([TensorflowSavedModelArtifact('model')])
class TensorfoodClassifier(BentoService):
        
  @api(input=FileInput(), batch=True)
  def predict(self, file_streams):
    height = 200
    width = 300
    if not os.path.isdir('upload_folder'):
      os.mkdir('upload_folder')
    image_path = 'upload_folder/image.png'

    for i, img in enumerate(file_streams):
      img = Image.open(img)
      img.save(image_path)

    img_pil = load_img(image_path, target_size=(height, width))
    img_np = img_to_array(img_pil)
    img_tf = tf.expand_dims(img_np, 0)

    model = self.artifacts.model
    y_pred_tf = model(img_tf)
    y_pred = np.float32(y_pred_tf)
    y_class = y_pred.argmax(1)[0]
    y_prob = y_pred[0,y_class]
    result = FOODS[y_class]
    return [[result, y_prob]]