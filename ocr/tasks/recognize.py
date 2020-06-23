import json
import os
import uuid

import cv2
import numpy as np
import pdf2image
import redis
import tensorflow as tf
from django.conf import settings

from backendDrewdru.celery import app
from ocr.neural_networks.ocr import OcrNeuralNetwork
from ocr.utils.horizon import fix_horizon
from ocr.utils.segmetation import (
    character_segmentation,
    lines_segmentation,
    word_segmentation,
)



@app.task
def train(lang):
    ocr = OcrNeuralNetwork(lang)
    ocr.train()



@app.task
def recognize(path, uid, lang):
    redis_instance = redis.StrictRedis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
    )
    try:
        redis_instance.set(f"status_{uid}", "start")
        pages = pdf2image.convert_from_path(path, 500)
        ocr = OcrNeuralNetwork(lang)
        output = ""
        wrong_recognized_classes = set()
        for index, page in enumerate(pages):
            progress = 0
            redis_instance.set(
                f"status_{uid}", f"Pre-processing page {index+1}"
            )
            redis_instance.set(f"progress_{uid}", progress)

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
            invert = 255 - binarized_image[1]

            lines, lines_count = lines_segmentation(invert)

            redis_instance.set(f"status_{uid}", f"Processing page {index+1}")
            
            for index, line in enumerate(lines):
                line_tag = '<p>'
                print(progress)
                redis_instance.set(f"progress_{uid}", progress)
                
                line_from = line[0]
                line_to = line[1]
                if line_from == line_to:
                    continue
                # elif line_from > line_to:
                #     line_from = line[1]
                #     line_to = line[0]
                if line_from - 15 > 0:
                    line_from -= 15
                if line_to + 15 < invert.shape[0]:
                    line_to += 15
                

                text_line = invert[line_from : line_to]
                # cv2.imshow("text_line", text_line)

                for word in word_segmentation(text_line):
                    # cv2.imshow("word", word)
                    recognized_word = ""
                    for character in character_segmentation(word):
                        recognized_word = ocr.recognize(
                            character, recognized_word
                        )
                        # # Generate Dataset
                        # if len(recognized_word):
                        #     value = recognized_word[-1]
                        #     # cv2.imshow("character", character)
                        #     # cv2.waitKey(500)
                        #     class_name = input(f'character is "{value}"? Press enter if True or type class_name:') or value
                        #     class_name = class_name.upper()
                        #     if class_name != value:
                        #         img_uid = str(uuid.uuid4())
                        #         path = f'{ocr.DATASET_TRAIN_PATH}{class_name}/{img_uid}.png'
                        #         cv2.imwrite(path, character)
                        #         wrong_recognized_classes.add(value)
                        #         print(wrong_recognized_classes)
                    output += f"{recognized_word} "
                output += "</p>"
                progress = (index + 1) / lines_count * 100
            output += "<br>" * 10
        # print(output)
        redis_instance.set(uid, output)
        redis_instance.set(f"status_{uid}", f"done")
    except Exception as error:
        # TODO: LOG Error
        redis_instance.set(f"status_{uid}", f"Error: {error}")
    os.remove(path)
    # TODO: add natural language processing
