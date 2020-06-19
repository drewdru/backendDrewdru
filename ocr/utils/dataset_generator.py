# -*- coding: utf-8 -*-

# -------------------------------- Imports ------------------------------#

# Import operating system lib
import os
from pathlib import Path

# Import random generator
from random import randint

from fontTools.ttLib import TTFont

# Import python imaging libs
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cleanup(font_dir, out_dir):
    # Delete ds_store file
    if os.path.isfile(font_dir + ".DS_Store"):
        os.unlink(font_dir + ".DS_Store")

    # Delete all files from output directory
    for file in os.listdir(out_dir):
        file_path = os.path.join(out_dir, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        return


def has_glyph(font_path, characters):
    font = TTFont(font_path)
    is_have_glyph = False
    for character in characters:
        for table in font["cmap"].tables:
            if ord(character) in table.cmap.keys():
                is_have_glyph = True
                break
        if not is_have_glyph:
            return False
        is_have_glyph = False
    return True


def generate_characters(font_dir, out_dir, characters, background_colors):
    k = 1
    font_size = 150
    x = 1
    y = -1
    for dirname, dirnames, filenames in os.walk(font_dir):
        for filename in filenames:
            if not filename.endswith(".ttf"):
                continue
            font_resource_file = os.path.join(dirname, filename)

            for character in characters:
                if not has_glyph(font_resource_file, character):
                    continue
                for background_color in background_colors:
                    try:
                        font = ImageFont.truetype(font_resource_file, font_size)
                        (font_width, font_height) = font.getsize(character)
                    except OSError as error:
                        print(error)
                        continue

                    char_image = Image.new(
                        "L", (font_width, font_height), background_color
                    )
                    draw = ImageDraw.Draw(char_image)

                    draw.text(
                        (x, y), character, (255 - background_color), font=font
                    )

                    # Final file name
                    if character == "/":
                        character = "SLASH"
                    upper_character = character.upper()
                    file_name = f"{out_dir}{upper_character}/{str(k)}_{filename}_fs_{str(font_size)}_bc_{str(background_color)}.{character}.png"
                    Path(f"{out_dir}{upper_character}").mkdir(
                        parents=True, exist_ok=True
                    )
                    # Save image
                    char_image.save(file_name)

                    # Increment counter
                    k = k + 1
    return


def run_generation():
    font_dir = f"{BASE_DIR}/fonts/"
    dataset_dir = f"{BASE_DIR}/dataset/"

    # Do cleanup
    cleanup(font_dir, dataset_dir)

    # fmt: off
    en_letters = ['(', '-', '1', '4', '7', 'A', 'D', 'G', 'J', 'M', 'P', 'S', 'U', 'X', ')', '?', '2', '5', '8', 'B', 'E', 'H', 'K', 'N', 'Q', '/', 'V', 'Y', ',', '0', '3', '6', '9', 'C', 'F', 'I', 'L', 'O', 'R', 'T', 'W', 'Z', 'a', 'd', 'g', 'j', 'm', 'p', 's', 'u', 'x', 'b', 'e', 'h', 'k', 'n', 'q', 'v', 'y', 'c', 'f', 'i', 'l', 'o', 'r', 't', 'w', 'z', ]
    ru_letters = ['(', '-', '1', '4', '7', 'I', 'Б', 'Д', 'Ж', 'Й', 'М', 'П', 'Т', 'Х', 'Ш', 'Ы', 'Ю', ')', '?', '2', '5', '8', '/', 'В', 'Е', 'З', 'К', 'Н', 'Р', 'У', 'Ц', 'Щ', 'Ь', 'Я', ',', '0', '3', '6', '9', 'А', 'Г', 'Ё', 'И', 'Л', 'О', 'С', 'Ф', 'Ч', 'Ъ', 'Э', 'i', 'б', 'д', 'ж', 'й', 'м', 'п', 'т', 'х', 'ш', 'ы', 'ю', 'в', 'е', 'з', 'к', 'н', 'р', 'у', 'ц', 'щ', 'ь', 'я', 'а', 'г', 'ё', 'и', 'л', 'о', 'с', 'ф', 'ч', 'ъ', 'э', ]
    ru_kz_letters = ['(', '0', '5', 'I', 'АЗ', 'В', 'Ё', 'Й', 'Л', 'Ө', 'ТТ', 'ҰН', 'Ч', 'Ь', ')', '1', '6', '№', 'АЛ', 'Г', 'Ж', 'К', 'М', 'П', 'У', 'Ф', 'Ш', 'Э', ',', '2', '7', '/', 'АН', 'Ғ', 'ЖҰМ', 'Қ', 'Н', 'Р', 'Ү', 'Х', 'Щ', 'Ю', '-', '3', '8', 'W', 'Ә', 'Д', 'З', 'ҚҰ', 'Ң', 'С', 'Ұ', 'h', 'Ъ', 'Я', '?', '4', '9', 'А', 'Б', 'Е', 'И', 'ҚҰЖ', 'О', 'Т', 'ҰЛ', 'Ц', 'Ы', 'i', 'аз', 'в', 'ё', 'й', 'л', 'ө', 'тт', 'ұн', 'ч', 'ь', 'ал', 'г', 'ж', 'к', 'м', 'п', 'у', 'ф', 'ш', 'э', 'ан', 'ғ', 'жұм', 'қ', 'н', 'р', 'ү', 'х', 'щ', 'ю', 'w', 'ә', 'д', 'з', 'құ', 'ң', 'с', 'ұ', 'h', 'ъ', 'я', 'а', 'б', 'е', 'и', 'құж', 'о', 'т', 'ұл', 'ц', 'ы', ]
    # fmt: on

    characters = {
        "en": en_letters,
        "ru": ru_letters,
        "ru_kz": ru_kz_letters,
    }

    background_colors = (0, 255)

    languages = [
        "ru_kz",
        "ru",
        "en",
    ]

    for lang in languages:
        print(lang)
        out_dir = f"{dataset_dir}{lang}/"
        generate_characters(
            font_dir, out_dir, characters[lang], background_colors
        )


if __name__ == "__main__":
    run_generation()
