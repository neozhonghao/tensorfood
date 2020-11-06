import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import logging

log_fmt = '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='logs',format=log_fmt)
logger = logging.getLogger(__name__)

class Datapipeline():
    
    def __init__(self):
        """
        Initialize datapipeline object.

        :param
        ------
        None: Input nothing

        :return:
        --------
        None: Return nothing
        """        
        self.test_params = {'featurewise_center':False,
                       'samplewise_center':False,
                       'featurewise_std_normalization':False,
                       'samplewise_std_normalization':False,
                       'zca_whitening':False,
                       'zca_epsilon':1e-06,
                       'rotation_range':0, 
                       'width_shift_range':0,
                       'height_shift_range':0,
                       'brightness_range':None,
                       'shear_range':0,
                       'zoom_range':0,
                       'channel_shift_range':0,
                       'fill_mode':'constant',
                       'cval':0,
                       'horizontal_flip':False,
                       'vertical_flip':False,
                       'rescale':None,
                       'preprocessing_function':None,
                       'data_format':None,
                       'validation_split':0,
                       'dtype':np.float32}        
                
        self.test_flow_params = {'x_col':'path',
                                 'y_col':'class',
                                 'batch':32,
                                 'target_size':(200, 300),
                                 'shuffle':False,
                                 'validate_filenames':False}
        
        self.test_ds = None

    def transform_test_data(self, test_data_path):
        """
        Feature engineer the data

        :param
        ------
        data_path: str
            csv file directory

        :return:
        --------
        test_ds: test generator
            iterator of test tuple (batch of input images, batch of one-hot encoded labels)
        """        
        df = pd.DataFrame({'path': [test_data_path],'class': ['wanton_noodle']})
        datagen = ImageDataGenerator(**self.test_params)
        self.test_ds = datagen.flow_from_dataframe(dataframe=df,**self.test_flow_params)
        logger.info('**********PREPROCESSING COMPLETED**********')
        
        return self.test_ds
    
    def transform_data_frame(self, test_data_path):
        """
        Feature engineer the data

        :param
        ------
        data_path: str
            csv file directory

        :return:
        --------
        test_ds: test generator
            iterator of test tuple (batch of input images, batch of one-hot encoded labels)
        """        
                
        df = pd.read_csv(test_data_path,index_col=0)  
        datagen = ImageDataGenerator(**self.test_params)
        self.test_ds = datagen.flow_from_dataframe(dataframe=df,**self.test_flow_params)
        
        return self.test_ds        