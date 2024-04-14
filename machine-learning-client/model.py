import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, load_model

import pathlib

import os
# Path to the saved model
model_path = './recog.keras'

model = load_model(model_path)

batch_size = 32
img_height = 180
img_width = 180

class_names = ["Angry", "Happy", "Neutral", "Sad", "Surprise"]

# Connect to MongoDB
# connect to the database
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")


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
# ############

# smile_path = "test_photos/test1.jpg"

# img = tf.keras.utils.load_img(
#     smile_path, target_size=(img_height, img_width)
# )
# img_array = tf.keras.utils.img_to_array(img)
# img_array = tf.expand_dims(img_array, 0) # Create a batch

# predictions = model.predict(img_array)
# score = tf.nn.softmax(predictions[0])

# print(
#     "This image most likely belongs to {} with a {:.2f} percent confidence."
#     .format(class_names[np.argmax(score)], 100 * np.max(score))
# )

# #########


# surprise_path = "test_photos/surprise.jpg"

# img = tf.keras.utils.load_img(
#     surprise_path, target_size=(img_height, img_width)
# )
# img_array = tf.keras.utils.img_to_array(img)
# img_array = tf.expand_dims(img_array, 0) # Create a batch

# predictions = model.predict(img_array)
# score = tf.nn.softmax(predictions[0])

# print(
#     "This image most likely belongs to {} with a {:.2f} percent confidence."
#     .format(class_names[np.argmax(score)], 100 * np.max(score))
# )
# ############



# sad_path = "test_photos/sad_test.jpg"

# img = tf.keras.utils.load_img(
#     sad_path, target_size=(img_height, img_width)
# )
# img_array = tf.keras.utils.img_to_array(img)
# img_array = tf.expand_dims(img_array, 0) # Create a batch

# predictions = model.predict(img_array)
# score = tf.nn.softmax(predictions[0])

# print(
#     "This image most likely belongs to {} with a {:.2f} percent confidence."
#     .format(class_names[np.argmax(score)], 100 * np.max(score))
# )
# ############


# neutral_path = "test_photos/neutral_test.jpg"

# img = tf.keras.utils.load_img(
#     neutral_path, target_size=(img_height, img_width)
# )
# img_array = tf.keras.utils.img_to_array(img)
# img_array = tf.expand_dims(img_array, 0) # Create a batch

# predictions = model.predict(img_array)
# score = tf.nn.softmax(predictions[0])

# print(
#     "This image most likely belongs to {} with a {:.2f} percent confidence."
#     .format(class_names[np.argmax(score)], 100 * np.max(score))
# )
############