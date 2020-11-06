from PIL import Image
import requests
import matplotlib.pyplot as plt
import argparse

def py_client(image_path):
    """
    A python script to post request to API.
    An image of the food will be outputted.
    PARAMS: 
        image_path: str path of the image wrt to package
    RETURNS: None
    """        
    img = Image.open(image_path)
    url = 'http://localhost:8000/predict'
    with open(image_path, 'rb') as f:
        x = requests.post(url, files={'image': f})
    plt.imshow(img)
    plt.text(0,0,x.text)
    frame1 = plt.gca()
    frame1.axes.xaxis.set_ticklabels([])
    frame1.axes.yaxis.set_ticklabels([])    
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', default='data/image_wanton_noodle.png')
    args = parser.parse_args()
    image_path = args.image_path
    py_client(image_path)