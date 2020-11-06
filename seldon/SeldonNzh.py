import os
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array

class SeldonNzh:
    def __init__(self):
        self.FOOD = ['chilli_crab', 'curry_puff', 'dim_sum', 'ice_kacang', 'kaya_toast', 'nasi_ayam',
               'popiah', 'roti_prata', 'sambal_stingray', 'satay', 'tau_huay', 'wanton_noodle']             
        self.model_path = 'tensorfood.h5'
        self.height = 200
        self.width = 300        
        self.loaded = False
        self.total_req = 0
        self.success_req = 0
        self.failure_req = 0

    def load(self):
        self.model = tf.keras.models.load_model(self.model_path)
        self.loaded = True
        print("-----zhong_hao_neo initialized model-----")        

    def pre_processing(self, image_np):
        image_uint8 = np.uint8(image_np)
        img_pil = Image.fromarray(image_uint8)
        img_resize_pil = img_pil.resize((self.width,self.height))
        img_np = tf.keras.preprocessing.image.img_to_array(img_resize_pil)
        img_np = img_np.reshape(1,self.height,self.width,3)
        print("-----zhong_hao_neo preprocessed image-----")        
        return img_np

    def inference(self, img_np):
        y_pred = self.model.predict(img_np)
        print("-----zhong_hao_neo completed inference-----")        
        return y_pred        

    def post_processing(self, y_pred):
        y_class = y_pred.argmax(1)[0]
        y_name = self.FOOD[y_class]
        y_prob = float(y_pred[0,y_class])
        print("-----zhong_hao_neo postprocessed results-----")        
        return [[y_name], [y_prob]]

    def predict(self, image_np, feature_names=""):
        self.total_req += 1
        try:
            if not self.loaded:
                self.load()
            img_np = self.pre_processing(image_np)
            y_pred = self.inference(img_np)
            result = self.post_processing(y_pred)
            self.success_req += 1
            return result            
        except:
            print("-----Error Request-----")
            self.failure_req += 1

    def metrics(self):
        return [            
            {"type": "COUNTER", "key": "nzh_requests_total", "value": self.total_req},
            {"type": "COUNTER", "key": "nzh_success_total", "value": self.success_req},
            {"type": "COUNTER", "key": "nzh_failure_total", "value": self.failure_req}
        ]        

    def init_metadata(self):
        meta = {
            "name": "SeldonNzh",
            "versions": ["1.0.0"],
            "platform": "Seldon-Core",
        }
        return meta