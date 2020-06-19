import os

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import (
    Conv2D,
    Dense,
    Dropout,
    Flatten,
    MaxPooling2D,
)
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class OcrNeuralNetwork:
    BATCH_SIZE = 120
    EPOCHS = 20
    IMG_HEIGHT = 150
    IMG_WIDTH = 150
    CLASSES = []

    def __init__(self, lang="en"):
        self.DATASET_PATH = f"{BASE_DIR}/dataset/{lang}/"
        self.MODEL_PATH = f"{BASE_DIR}/neural_networks/{lang}.h5"
        self.init_train_data()
        self.init_model()

    def init_train_data(self):
        train_image_generator = ImageDataGenerator(
            rescale=1.0 / 255,
            rotation_range=45,
            width_shift_range=0.15,
            height_shift_range=0.15,
            zoom_range=0.5,
        )
        self.train_data_gen = train_image_generator.flow_from_directory(
            batch_size=self.BATCH_SIZE,
            directory=self.DATASET_PATH,
            shuffle=True,
            target_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
        )
        self.CLASSES = list(self.train_data_gen.class_indices.keys())

        validation_image_generator = ImageDataGenerator(rescale=1.0 / 255)
        self.val_data_gen = validation_image_generator.flow_from_directory(
            batch_size=self.BATCH_SIZE,
            directory=self.DATASET_PATH,
            target_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
        )

    def init_model(self):
        if os.path.exists(self.MODEL_PATH):
            self.model = tf.keras.models.load_model(self.MODEL_PATH)
        else:
            self.model = Sequential(
                [
                    Conv2D(
                        16,
                        3,
                        padding="same",
                        activation="relu",
                        input_shape=(self.IMG_HEIGHT, self.IMG_WIDTH, 3),
                    ),
                    MaxPooling2D(),
                    Conv2D(32, 3, padding="same", activation="relu"),
                    MaxPooling2D(),
                    Conv2D(64, 3, padding="same", activation="relu"),
                    MaxPooling2D(),
                    Conv2D(128, 3, padding="same", activation="relu"),
                    MaxPooling2D(),
                    Flatten(),
                    Dense(512, activation="relu"),
                    Dense(len(self.CLASSES)),
                ]
            )
        self.model.compile(
            optimizer="adam",
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
            metrics=["accuracy"],
        )
        self.model.summary()

    def train(self):
        total = sum([len(files) for r, d, files in os.walk(self.DATASET_PATH)])
        steps = total // self.BATCH_SIZE
        history = self.model.fit(
            self.train_data_gen,
            steps_per_epoch=steps,
            epochs=self.EPOCHS,
            validation_data=self.val_data_gen,
            validation_steps=steps,
        )
        self.model.save(self.MODEL_PATH)

    def recognize(self, img, word):
        result = cv2.resize(
            img,
            dsize=(self.IMG_WIDTH, self.IMG_HEIGHT),
            interpolation=cv2.INTER_CUBIC,
        )
        color_image = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        input_arr = np.array([color_image])
        predictions = self.model.predict(input_arr)
        character_idx = tf.argmax(predictions[0]).numpy()
        value = self.CLASSES[character_idx]
        if value == "SLASH":
            value = "/"
        if value == "DOT":
            value = "."
        if len(word) and word[-1] == "Ь" and value == "I":
            value = "Ы"
            word = word[:-1]
        word += value
        return word
