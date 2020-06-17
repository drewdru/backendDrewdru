import json
import os

import cv2
import numpy as np
import pdf2image
import redis
import tensorflow as tf
from django.conf import settings

from backendDrewdru.celery import app
from ocr.utils.horizon import fix_horizon
from ocr.utils.segmetation import (
    character_segmentation,
    lines_segmentation,
    word_segmentation,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_FILE = f"{BASE_DIR}/neural_network/model.h5"

CHARACTERS = [
    "(",
    ")",
    ",",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "W",
    "slash",
    "Ё",
    "І",
    "А",
    "АЗ",
    "АЛ",
    "АН",
    "Б",
    "В",
    "Г",
    "Д",
    "Е",
    "Ж",
    "ЖҰМ",
    "З",
    "И",
    "Й",
    "К",
    "Л",
    "М",
    "Н",
    "О",
    "П",
    "Р",
    "С",
    "Т",
    "ТТ",
    "У",
    "Ф",
    "Х",
    "Ц",
    "Ч",
    "Ш",
    "Щ",
    "Ъ",
    "Ы",
    "Ь",
    "Э",
    "Ю",
    "Я",
    "Ғ",
    "Қ",
    "ҚҰ",
    "ҚҰЖ",
    "Ң",
    "Ү",
    "Ұ",
    "ҰЛ",
    "ҰН",
    "Һ",
    "Ә",
    "Ө",
    "№",
]
IMG_HEIGHT = 150
IMG_WIDTH = 150

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)


@app.task
def recognize(path, uid):
    pages = pdf2image.convert_from_path(path, 500)
    model = tf.keras.models.load_model(MODEL_FILE)
    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    model.summary()

    output = ""

    for index, page in enumerate(pages):
        redis_instance.set(f"status_{uid}", f"Start processing page {index+1}")
        # Pre processing
        image = np.array(page)
        image = fix_horizon(image)
        # TODO: Add remove watermarks and printing
        # TODO: Fix blur
        # TODO: Filter by Text color?
        # TODO: remove long lines

        # Binarize
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        binarized_image = cv2.threshold(
            gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        # count = 0
        for text_line in lines_segmentation(binarized_image[1]):
            # cv2.imshow("text_line", text_line)
            for word in word_segmentation(text_line):
                # cv2.imshow("word", word)
                for character in character_segmentation(word):
                    # cv2.imwrite(f"dataset/character_{count}.png", character)
                    # count += 1
                    # TODO: reconize word with NN
                    result = cv2.resize(
                        character,
                        dsize=(IMG_WIDTH, IMG_HEIGHT),
                        interpolation=cv2.INTER_CUBIC,
                    )

                    color_image = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
                    input_arr = np.array([color_image])
                    predictions = model.predict(input_arr)
                    character_idx = tf.argmax(predictions[0]).numpy()
                    value = CHARACTERS[character_idx]
                    if value == "slash":
                        value = "/"
                    output += value
                output += " "
            output += "\n"
        output += "\n" * 10
    redis_instance.set(uid, output)
    redis_instance.set(f"status_{uid}", f"done")
    os.remove(path)
