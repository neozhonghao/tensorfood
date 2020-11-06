from src.datapipeline import Datapipeline
from src.model import Model

import os
import argparse
import logging

log_fmt = '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='logs',format=log_fmt)
logger = logging.getLogger(__name__)

FOODS = ['chilli_crab',
         'curry_puff',
         'dim_sum',
         'ice_kacang',
         'kaya_toast',
         'nasi_ayam',
         'popiah',
         'roti_prata',
         'sambal_stingray',
         'satay',
         'tau_huay',
         'wanton_noodle']

def run_inference(image_path, model=None):
    """
    Performs inference
    PARAMS: 
        image_path: str path of the image wrt to package
        model: keras model object.
               If none, will initialize,
               else, will use passed model.
    RETURNS:
       result: str of food
       y_prob: probability of prediction
    """    
    dpl = Datapipeline()
    test_ds = dpl.transform_test_data(image_path)
    if model == None:
        model = Model()
    y_class, y_prob = model.predict(test_ds)
    result = FOODS[y_class]
    print('Food: {}, Probability:{}'.format(result, y_prob))
    logger.info("**********INFERENCE COMPLETED**********")
    logger.info('food:{}, probability:{}'.format(result,y_prob))
    return result, y_prob
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', default='data/image_wanton_noodle.png')
    args = parser.parse_args()
    image_path = args.image_path
    
    run_inference(image_path)