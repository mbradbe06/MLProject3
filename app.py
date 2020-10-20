#dependencies
from flask import Flask, url_for, jsonify, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import os
import re
import base64
from PIL import Image
from io import BytesIO
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# Read in our CNN model
modelCNN = load_model('model/modelCNN.h5')


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Classify
        predictions = classify_imageCNN(img)

        classes = ['Altar', 'Apse', 'Bell Tower', 'Column', 'Inner Dome',\
        'Outer Dome', 'Flying Buttress', 'Gargoyle', 'Stained Glass', 'Vault']

        class_descriptions = {
            "Altar" : "Structure for sacrifices for religious purposes typically found in shrines, temples, churches, and other places of worship.",\
            "Apse" : "Semicircular recess covered with a hemispherical vault - typically the apse of a church or basilica is where an altar resides.",\
            "Bell Tower" : "The term 'campanile' is synonymous with bell tower and in some traditions may be called a belfry, though that term can also specifically refer to the substructure that houses the bells and ringers.",\
            "Column" : "Pillar in architecture that transmits the weight of a structure above to the structural elements below - all significant Iron Age civilizations in the Near East and Mediterranean made use of columns.",\
            "Inner Dome" : "Arch element similar to the upper half of a sphere.  Its architectural lineage extends well into prehistory.  Domes were built in ancient Mesopotamia, and they have been found in Persian, Hellenistic, Roman, and Chinese architecture in the ancient world, as well as among a number of indigenous building traditions throughout the world.",\
            "Outer Dome" : "Arch element similar to the upper half of a sphere.  Its architectural lineage extends well into prehistory.  Domes were built in ancient Mesopotamia, and they have been found in Persian, Hellenistic, Roman, and Chinese architecture in the ancient world, as well as among a number of indigenous building traditions throughout the world.",\
            "Flying Buttress" : "Masonry structure typically consisting of an inclined bar carried on a half arch that extends (“flies”) from the upper part of a wall to a pier some distance away and carries the thrust of a roof or vault - also typical of the Gothic Era.",\
            "Gargoyle" : "Carved or formed grotesque typically characteristic of Gothic Architecture.  When they began appearing on churches throughout Europe in the 13th Century, they served as decorative water spouts, engineered to preserve stone walls by diverting the flow of rainwater.",\
            "Stained Glass" : "Colored glass has been produced since ancient times - both Egyptians and Romans excelled in its creation.  Evidence of stained glass in churches and monasteries can be found as early as the 7th century.",\
            "Vault" : "Self-supporting continuous arched form mean tot cover a space with a ceiling or a roof - its use dates as far back as 6000 BCE."
                       
        }
        # find index of predicted class
        classification = np.argmax(predictions, axis=-1)
        result = classes[classification[0]]
        description = class_descriptions[result][:]
        
        # Serialize the result, you can add additional fields
        return jsonify(result=result, description = description)

    return None

def base64_to_pil(img_base64):
   
    image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    return pil_image

def classify_imageCNN(image_new):
    img = image_new.resize((128, 128))
    img_np = image.img_to_array(img)
    img_np = np.expand_dims(img_np, axis = 0)
    prediction = modelCNN.predict(img_np)
    return prediction


if __name__ == '__main__':
    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
