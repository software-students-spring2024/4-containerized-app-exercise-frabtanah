import matplotlib.pyplot as plt
import numpy as np
import PIL
import pymongo
import os
import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, session
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

# Connect to MongoDB
# connect to the database
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]
# app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")


def fetch_and_predict(image_id):
    # Fetch an image from MongoDB using its ID
    image_data = db.users.find_one({'_id': image_id})
    if not image_data:
        return "Image not found"

    # Assuming image data is stored as binary data in the 'image' field
    image_bytes = image_data['image']
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((img_height, img_width))
    image = image.convert('RGB')  # Ensure image is in RGB format

    # Convert image to a numpy array suitable for TensorFlow
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)  # Create a batch

    # Prediction
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['class1', 'class2', 'class3']  # Update as per your model classes

    predicted_class = class_names[np.argmax(score)]
    confidence = np.max(score) * 100
    return f"This image most likely belongs to {predicted_class} with a {confidence:.2f}% confidence."


if user and "assessments" in user:
        for assessment in user['assessments']:
            #check if the assessment is an image or text
            if 'image_data' in assessment:
                image_b64 = base64.b64encode(assessment['image_data']).decode('utf-8')
                assessments_list.append({
                    'type': 'image',
                    'image_b64': image_b64,
                    'currentDate': assessment['currentDate']
                })

# Fetch an image from MongoDB
image_data = collection.find_one({'image_id': 'specific_image_id'})
image_bytes = image_data['image']

# Convert binary data to image
image = image.open(io.BytesIO(image_bytes))
image = image.resize((img_height, img_width))  # Resize the image to match model input
image = image.convert('RGB')  # Ensure image is in RGB format

img_array = tf.keras.utils.img_to_array(image)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)