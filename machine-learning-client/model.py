import matplotlib.pyplot as plt
import numpy as np
import PIL
import requests
from PIL import Image
import pymongo
import os
import io
import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify
import pymongo

# from pymongo.server_api import ServerApi
import bcrypt
from dotenv import load_dotenv

# image imports
import base64
from bson import binary

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, load_model

import pathlib

# Path to the saved model
model_path = './recog.keras'

model = load_model(model_path)

batch_size = 32
img_height = 180
img_width = 180

class_names = ["Angry", "Happy", "Neutral", "Sad", "Surprise"]

#---------------------------------------------------------------

# load credentials and configuration options from .env file
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

# Connect to MongoDB
# connect to the database
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

@app.route('/predict', methods=['POST'])
def fetch_and_predict():
    if not request.data:
        return jsonify({"error": "No data provided"}), 400
    # file = request.files['image_data']

    # Fetch an image from MongoDB using its ID
    # image_data = db.users.find_one({"image_data": binary.Binary(image_id)})
    
    # Assuming image data is stored as binary data in the 'image' field
    image_bytes = request.data
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((img_height, img_width))
    image = image.convert('RGB')  # Ensure image is in RGB format

    # Convert image to a numpy array suitable for TensorFlow
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)  # Create a batch

    # Prediction
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['Angry', 'Happy', 'Neutral', "Sad", "Surprise"]  # Update as per your model classes

    predicted_class = class_names[np.argmax(score)]
    confidence = np.max(score) * 100
    return jsonify({"predicted_class": predicted_class, "confidence": confidence})

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app.run(port=FLASK_PORT)