"""Module for predicting emotions from images using a trained TensorFlow model."""

import os
import io
# import base64
import numpy as np
from PIL import Image
import pymongo
import tensorflow as tf
from tensorflow.keras.models import load_model
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables and TensorFlow model
load_dotenv()
MODEL_PATH = "./recog.keras"
model = load_model(MODEL_PATH)

# Configuration constants
BATCH_SIZE = 32
IMG_HEIGHT = 180
IMG_WIDTH = 180
CLASS_NAMES = ["Angry", "Happy", "Neutral", "Sad", "Surprise"]

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# MongoDB connection
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]

@app.route("/predict", methods=["POST"])
def fetch_and_predict():
    """Receive an image via POST and predict the emotion."""
    if not request.data:
        return jsonify({"error": "No data provided"}), 400

    image_bytes = request.data
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((IMG_HEIGHT, IMG_WIDTH))
    image = image.convert("RGB")  # Ensure image is in RGB format

    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)  # Create a batch for prediction

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    predicted_class = CLASS_NAMES[np.argmax(score)]
    confidence = np.max(score) * 100

    return jsonify({"predicted_class": predicted_class, "confidence": confidence})

angry_path = "test_photos/angry_guy.jpg"

img = tf.keras.utils.load_img(
    angry_path, target_size=(IMG_HEIGHT, IMG_HEIGHT)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(CLASS_NAMES[np.argmax(score)], 100 * np.max(score))
)


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app.run(port=FLASK_PORT)
    