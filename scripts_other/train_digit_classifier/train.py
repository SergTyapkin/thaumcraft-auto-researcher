import os
import pickle

import cv2
import keras
import numpy as np
import tensorflow as tf
from keras import layers
from keras.src.utils import to_categorical
from matplotlib import pyplot as plt


DIGIT_WIDTH = 13
DIGIT_HEIGHT = 17

ds = pickle.load(open("dataset.pkl", "rb"))
X, y = ds

# Приводим все изображения к одному размеру
for i in range(len(X)):
    X[i] = cv2.resize(X[i], (DIGIT_WIDTH, DIGIT_HEIGHT), interpolation=cv2.INTER_AREA)
    X[i] = np.pad(X[i], 5)

test_size = int(0.15 * len(y))

X = np.array(X)
y = np.array(y)
X = X.astype(float) / 255
X = np.expand_dims(X, axis=3)
y = to_categorical(y)

ds = tf.data.Dataset.from_tensor_slices((X, y))
ds = ds.shuffle(1000)

test_ds = ds.take(test_size)
test_ds = test_ds.batch(64)

train_ds = ds.skip(test_size)
train_ds = train_ds.batch(64)
augment = keras.Sequential([
    layers.RandomTranslation(height_factor=0.2, width_factor=0.2),
    layers.RandomZoom(height_factor=0.2, width_factor=0.2),
])
train_ds = train_ds.map(lambda x, y: (augment(x), y))

# for x, y in train_ds:
#     for img, label in zip(x, y):
#         plt.imshow(img)
#         plt.show()
#         print(label.numpy().argmax())

model = keras.Sequential([
    layers.Conv2D(filters=64, kernel_size=3),
    layers.MaxPool2D(),
    layers.Conv2D(filters=64, kernel_size=3),
    layers.MaxPool2D(),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dropout(0.15),
    layers.Dense(10, activation="softmax"),
])

model.compile(
    loss="categorical_crossentropy",
    optimizer="adam",
    metrics=["accuracy"],
)
model.fit(train_ds, epochs=10, validation_data=test_ds)

# model.save("model.keras")
model.export("model")
os.system(r"python -m tf2onnx.convert --saved-model model --output ..\..\models\digit_classification2.onnx")
