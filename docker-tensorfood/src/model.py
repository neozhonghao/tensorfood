import os
import numpy as np
import tensorflow as tf

from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import confusion_matrix

import logging

log_fmt = '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='logs',format=log_fmt)
logger = logging.getLogger(__name__)

class Model:

    def __init__(self):
        """
        DSCRPT: Initialize model object from saved model.
        PARAMS: None
        RETURN: None
        """
        model_path = 'models/tensorfood.h5'
        if not os.path.isfile(model_path):
            PATH_MODEL = os.path.join(os.getcwd())
            model_path = os.path.join(PATH_MODEL, "tensorfood.h5")          
        self.model = tf.keras.models.load_model(model_path)
        logger.info('**********MODEL LOADED**********')
        
    def predict(self, test_ds):
        """
        DSCRPT: Makes prediction.
        PARAMS:
            test_ds: Pandas dataframe of one image sample.
        RETURN:
            y_class: integer of food class
            y_prob: numpy float of probability of prediction
        """        
        logger.info('**********PREDICTION STARTING**********') 
        y_pred = self.model.predict(test_ds)
        y_class = y_pred.argmax(1)[0]
        y_prob = y_pred[0,y_class]
        logger.info('**********PREDICTION COMPLETED**********') 
        return y_class, y_prob
    
    def evaluate(self, test_ds):
        """
        DSCRPT: An evaluation for pytest unit test.
        PARAMS:
            test_ds: Pandas dataframe of the pytest test cases.
        RETURN:
            results: dictionary of metrics.
        """                
        y_pred = self.model.predict(test_ds)

        for i in range(len(test_ds)):
            X, y = test_ds[i]
            if i == 0:
                y_test = y
            else:
                y_test = np.concatenate((y_test, y), axis=0)

        tot = len(y_test)
        tot_prec, tot_rec, tot_f1, tot_spec, tot_auc = (0,0,0,0,0)
        cm = confusion_matrix(np.argmax(y_test,1),np.argmax(y_pred,1))
        
        for i in range(12):
            tp, fp, fn, tn = np.zeros((4),np.float32)

            fpr, tpr, thresholds = roc_curve(y_test[:,i], y_pred[:,i])
            tot_auc += auc(fpr,tpr)

            tp = cm[i,i]
            fp = cm[:,i].sum() - cm[i,i]
            fn = cm[i,:].sum() - cm[i,i]
            tn = tot - tp - fp - fn 

            if tp or fp:
                prec = tp/(tp+fp)
            if tp or fn:    
                rec = tp/(tp+fn)
            if tp or fp or fn:
                f1 = 2*tp/(2*tp+fp+fn)
            if tn or fp:
                spec = tn/(tn+fp)

            tot_prec += prec
            tot_rec += rec
            tot_f1 += f1
            tot_spec += spec
            
        acc = np.float32(np.argmax(y_test,1)==np.argmax(y_pred,1)).mean()
        results = {'accuracy':acc,
                   'auc': tot_auc/12,
                   'precision':tot_prec/12,
                   'recall': tot_rec/12,
                   'f1': tot_f1/12,
                   'specificity': tot_spec/12,
                  }
        return results