from flask import Flask, jsonify, request, render_template
from waitress import serve
from src.inference import run_inference
from src.model import Model
import os
import logging
import json

log_fmt = '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='logs',format=log_fmt)
logger = logging.getLogger(__name__)

app = Flask(__name__)
model = Model()

@app.route('/', methods=['GET','POST'])
def index():
    """
    Renders the html homepage.
    PARAMS: None
    RETURNS: 
        render_template: Rendering of homepage with results if POST,
                         and without results if GET.
    """
    if request.method == 'POST':
        results = predict()
        return render_template('index.html',prediction_text=results)
    return render_template('index.html')


@app.route('/info', methods=['GET'])
def short_description():
    """
    Gives a short summary of model.
    PARAMS: None
    RETURNS: json of the model information.
    """
    description = {"model": "Xception",
           "input-size": "200x300x3",
           "num-classes": 12,
           "pretrained-on": "ImageNet"}    
    return jsonify(description)


@app.route('/docs', methods=['GET'])
def readme():
    """
    Gives a short summary of model.
    PARAMS: None
    RETURNS: json of the model information.
    """
    return render_template('README.md')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Calls inference for prediction
    PARAMS: None
    RETURNS: json of food and probability.
    """
    image = request.files['image']
    logger.info('**********IMAGE DOWNLOADED**********')
    if not os.path.isdir('upload_folder'):
        os.mkdir('upload_folder')
    image_path = 'upload_folder/image.png'
    image.save(image_path)
    y_cls, y_prob = run_inference(image_path, model)
    return json.dumps({'food': y_cls, 'probability': float(y_prob) })

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
