import pathlib
import matplotlib.pyplot as plt
import numpy as np
import PIL
import os
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

## for loading data using keras utility?

#some parameteres for loader
batch_size = 8

data_dir = "training_photos/"
data_dir = pathlib.Path(data_dir).with_suffix('')


image_count = len(list(data_dir.glob('*/*.jpg')))
print(image_count)

def preprocess_image(image_path, img_height, img_width):
    # Read the image file
    img = tf.io.read_file(image_path)
    # Decode the image as a JPEG file (this will handle a .jpg image)
    img = tf.image.decode_jpeg(img, channels=3)
    # Resize the image to the desired size
    img = tf.image.resize(img, [img_height, img_width])
    # Normalize image pixels
    img = img / 255.0
    return img

# Assuming you decide on a standard square image size for CNNs
img_height = 224
img_width = 224

# Load and preprocess the example image

for folder in os.listdir(data_dir):
    fold = os.path.join(data_dir, folder)

    if os.path.isdir(fold):
        for img in os.listdir(fold):

            if img.endswith(".jpg"):
                pathimg = os.path.join(fold, img)
                image = preprocess_image(pathimg, img_height, img_width)

kds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    labels='inferred'
)

dataset = kds.batch(batch_size, drop_remainder=True)

# anger = list(data_dir.glob('anger/*'))
# PIL.Image.open(str(anger[0]))

# directory_path = 'training_photos/anger'
# try:
#     files = os.listdir(directory_path)
#     print("Files in the directory:", files)
# except Exception as e:
#     print("Error:", e)

# train_ds = tf.keras.utils.image_dataset_from_directory(
#   data_dir,
#   validation_split=0.2,
#   subset="training",
#   seed=123,
#   image_size=(img_height, img_width),
#   batch_size=batch_size)

class_names = kds.class_names
print(class_names)

plt.figure(figsize=(10, 10))
for images, labels in kds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")


## Keras Model Creation
# num_classes = len(class_names)

# model = Sequential([
#   layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
#   layers.Conv2D(16, 3, padding='same', activation='relu'),
#   layers.MaxPooling2D(),
#   layers.Conv2D(32, 3, padding='same', activation='relu'),
#   layers.MaxPooling2D(),
#   layers.Conv2D(64, 3, padding='same', activation='relu'),
#   layers.MaxPooling2D(),
#   layers.Flatten(),
#   layers.Dense(128, activation='relu'),
#   layers.Dense(num_classes)
# ])
