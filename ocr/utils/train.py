import os

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

# import matplotlib.pyplot as plt
train_dir = "./dataset/train"
validation_dir = "./dataset/validation"
MODEL_FILE = "./models/model.h5"

# train_cats_dir = './cats_and_dogs_filtered/train/cats'  # directory with our training cat pictures
# train_dogs_dir = './cats_and_dogs_filtered/train/dogs'  # directory with our training dog pictures
# validation_cats_dir = './cats_and_dogs_filtered/validation/cats' # directory with our validation cat pictures
# validation_dogs_dir = './cats_and_dogs_filtered/validation/dogs' # directory with our validation dog pictures

# num_cats_tr = len(os.listdir(train_cats_dir))
# num_dogs_tr = len(os.listdir(train_dogs_dir))

# num_cats_val = len(os.listdir(validation_cats_dir))
# num_dogs_val = len(os.listdir(validation_dogs_dir))

total_train = sum([len(files) for r, d, files in os.walk(train_dir)])
total_val = sum([len(files) for r, d, files in os.walk(validation_dir)])

# print('total training cat images:', num_cats_tr)
# print('total training dog images:', num_dogs_tr)
# print('total validation cat images:', num_cats_val)
# print('total validation dog images:', num_dogs_val)
# print("--")
# print("Total training images:", total_train)
# print("Total validation images:", total_val)

BATCH_SIZE = 128
EPOCHS = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150

train_image_generator = ImageDataGenerator(
    rescale=1.0 / 255
)  # Generator for our training data
validation_image_generator = ImageDataGenerator(
    rescale=1.0 / 255
)  # Generator for our validation data
classes = [
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
    "№",
    "slash",
    "W",
    "А",
    "АЗ",
    "АЛ",
    "АН",
    "Ә",
    "Б",
    "В",
    "Г",
    "Ғ",
    "Д",
    "Е",
    "Ё",
    "Ж",
    "ЖҰМ",
    "З",
    "И",
    "І",
    "Й",
    "К",
    "Қ",
    "ҚҰ",
    "ҚҰЖ",
    "Л",
    "М",
    "Н",
    "Ң",
    "О",
    "Ө",
    "П",
    "Р",
    "С",
    "Т",
    "ТТ",
    "У",
    "Ү",
    "Ұ",
    "ҰЛ",
    "ҰН",
    "Ф",
    "Х",
    "Һ",
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
]
# classes = {0: '(', 1: ')', 2: ',', 3: '0', 4: '1', 5: '2', 6: '3', 7: '4', 8: '5', 9: '6', 10: '7', 11: '8', 12: '9', 13: '№', 14: 'slash', 15: 'W', 16: 'А', 17: 'АЗ', 18: 'АЛ', 19: 'АН', 20: 'Ә', 21: 'Б', 22: 'В', 23: 'Г', 24: 'Ғ', 25: 'Д', 26: 'Е', 27: 'Ё', 28: 'Ж', 29: 'ЖҰМ', 30: 'З', 31: 'И', 32: 'І', 33: 'Й', 34: 'К', 35: 'Қ', 36: 'ҚҰ', 37: 'ҚҰЖ', 38: 'Л', 39: 'М', 40: 'Н', 41: 'Ң', 42: 'О', 43: 'Ө', 44: 'П', 45: 'Р', 46: 'С', 47: 'Т', 48: 'ТТ', 49: 'У', 50: 'Ү', 51: 'Ұ', 52: 'ҰЛ', 53: 'ҰН', 54: 'Ф', 55: 'Х', 56: 'Һ', 57: 'Ц', 58: 'Ч', 59: 'Ш', 60: 'Щ', 61: 'Ъ', 62: 'Ы', 63: 'Ь', 64: 'Э', 65: 'Ю', 66: 'Я',}
train_data_gen = train_image_generator.flow_from_directory(
    batch_size=BATCH_SIZE,
    directory=train_dir,
    shuffle=True,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    # classes=classes,
    # class_mode='sparse',
    # classes=classes
)

val_data_gen = validation_image_generator.flow_from_directory(
    batch_size=BATCH_SIZE,
    directory=validation_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    # classes=classes,
    # save_to_dir='output',
    # class_mode='sparse',
    # classes=classes
)

# print('train_data_gen', train_data_gen)
# print('train_data_gen:', next(train_data_gen))


# sample_training_images, _ = next(train_data_gen)

# # This function will plot images in the form of a grid with 1 row and 5 columns where images are placed in each column.
# def plotImages(images_arr):
#     fig, axes = plt.subplots(1, 5, figsize=(20,20))
#     axes = axes.flatten()
#     for img, ax in zip( images_arr, axes):
#         ax.imshow(img)
#         ax.axis('off')
#     plt.tight_layout()
#     plt.show()

# plotImages(sample_training_images[:5])
if os.path.exists(MODEL_FILE):
    model = tf.keras.models.load_model(MODEL_FILE)
    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    model.summary()
else:
    model = Sequential(
        [
            Conv2D(
                16,
                3,
                padding="same",
                activation="relu",
                input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
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
            Dense(67),
        ]
    )
    # model.compile(
    #     optimizer='adam',
    #     loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    #     metrics=['accuracy']
    # )
    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    model.summary()

    # Train:
    history = model.fit(
        train_data_gen,
        steps_per_epoch=total_train // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=val_data_gen,
        validation_steps=total_val // BATCH_SIZE,
    )
    model.save(MODEL_FILE)
print(model)

image = tf.keras.preprocessing.image.load_img("./a.png")
input_arr = tf.keras.preprocessing.image.img_to_array(image)
input_arr = np.array([input_arr])  # Convert single image to a batch.
predictions = model.predict(input_arr)
print(input_arr)
print("-" * 60)
print("labels:", model.metrics_names)
print("predictions:", predictions)
print("predictions len:", predictions.shape[1])
# print('evaluate:', model.evaluate(input_arr, batch_size=batch_size,))
class_names = list(train_data_gen.class_indices.keys())
print(
    class_names
)  # ['(', ')', ',', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'W', 'slash', 'Ё', 'І', 'А', 'АЗ', 'АЛ', 'АН', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'ЖҰМ', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'ТТ', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'Ғ', 'Қ', 'ҚҰ', 'ҚҰЖ', 'Ң', 'Ү', 'Ұ', 'ҰЛ', 'ҰН', 'Һ', 'Ә', 'Ө', '№']
print(len(class_names))
class_idx = tf.argmax(predictions[0]).numpy()
p = tf.nn.softmax(predictions[0])[class_idx]
name = class_names[class_idx]
print("prediction: {} ({:4.1f}%)".format(name, 100 * p))


# # Vizualize:
# # acc = history.history['accuracy']
# # val_acc = history.history['val_accuracy']
# # loss=history.history['loss']
# # val_loss=history.history['val_loss']
# # epochs_range = range(epochs)
# # plt.figure(figsize=(8, 8))
# # plt.subplot(1, 2, 1)
# # plt.plot(epochs_range, acc, label='Training Accuracy')
# # plt.plot(epochs_range, val_acc, label='Validation Accuracy')
# # plt.legend(loc='lower right')
# # plt.title('Training and Validation Accuracy')
# # plt.subplot(1, 2, 2)
# # plt.plot(epochs_range, loss, label='Training Loss')
# # plt.plot(epochs_range, val_loss, label='Validation Loss')
# # plt.legend(loc='upper right')
# # plt.title('Training and Validation Loss')
# # plt.show()

# # Train with horizontal flip
# image_gen = ImageDataGenerator(rescale=1./255, horizontal_flip=True)
# train_data_gen = image_gen.flow_from_directory(
#     batch_size=batch_size,
#     directory=train_dir,
#     shuffle=True,
#     target_size=(IMG_HEIGHT, IMG_WIDTH)
# )

# # augmented_images = [train_data_gen[0][0][0] for i in range(5)]
# # plotImages(augmented_images)

# # train with rotations
# image_gen = ImageDataGenerator(rescale=1./255, rotation_range=45)
# train_data_gen = image_gen.flow_from_directory(
#     batch_size=batch_size,
#     directory=train_dir,
#     shuffle=True,
#     target_size=(IMG_HEIGHT, IMG_WIDTH)
# )

# # augmented_images = [train_data_gen[0][0][0] for i in range(5)]
# # plotImages(augmented_images)


# # train with zooming
# # zoom_range from 0 - 1 where 1 = 100%.
# image_gen = ImageDataGenerator(rescale=1./255, zoom_range=0.5) #
# train_data_gen = image_gen.flow_from_directory(
#     batch_size=batch_size,
#     directory=train_dir,
#     shuffle=True,
#     target_size=(IMG_HEIGHT, IMG_WIDTH)
# )

# # augmented_images = [train_data_gen[0][0][0] for i in range(5)]
# # plotImages(augmented_images)

# # Train with all augmentations at once
# image_gen_train = ImageDataGenerator(
#     rescale=1./255,
#     rotation_range=45,
#     width_shift_range=.15,
#     height_shift_range=.15,
#     horizontal_flip=True,
#     zoom_range=0.5
# )
# train_data_gen = image_gen_train.flow_from_directory(
#     batch_size=batch_size,
#     directory=train_dir,
#     shuffle=True,
#     target_size=(IMG_HEIGHT, IMG_WIDTH),
#     class_mode='binary'
# )
# # augmented_images = [train_data_gen[0][0][0] for i in range(5)]
# # plotImages(augmented_images)

# # Validate data generator
# image_gen_val = ImageDataGenerator(rescale=1./255)
# val_data_gen = image_gen_val.flow_from_directory(
#     batch_size=batch_size,
#     directory=validation_dir,
#     target_size=(IMG_HEIGHT, IMG_WIDTH),
#     class_mode='binary'
# )


# #Creating a new network with Dropouts
# # Here, you apply dropout to first and last max pool layers. Applying dropout will randomly set 20% of the neurons to zero during each training epoch. This helps to avoid overfitting on the training dataset.
# model_new = Sequential([
#     Conv2D(16, 3, padding='same', activation='relu',
#            input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
#     MaxPooling2D(),
#     Dropout(0.2),
#     Conv2D(32, 3, padding='same', activation='relu'),
#     MaxPooling2D(),
#     Conv2D(64, 3, padding='same', activation='relu'),
#     MaxPooling2D(),
#     Dropout(0.2),
#     Flatten(),
#     Dense(512, activation='relu'),
#     Dense(1)
# ])

# model_new.compile(optimizer='adam',
#                   loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
#                   metrics=['accuracy'])
# model_new.summary()

# history = model_new.fit_generator(
#     train_data_gen,
#     steps_per_epoch=total_train // batch_size,
#     epochs=epochs,
#     validation_data=val_data_gen,
#     validation_steps=total_val // batch_size
# )

# # acc = history.history['accuracy']
# # val_acc = history.history['val_accuracy']

# # loss = history.history['loss']
# # val_loss = history.history['val_loss']
# # epochs_range = range(epochs)
# # plt.figure(figsize=(8, 8))
# # plt.subplot(1, 2, 1)
# # plt.plot(epochs_range, acc, label='Training Accuracy')
# # plt.plot(epochs_range, val_acc, label='Validation Accuracy')
# # plt.legend(loc='lower right')
# # plt.title('Training and Validation Accuracy')
# # plt.subplot(1, 2, 2)
# # plt.plot(epochs_range, loss, label='Training Loss')
# # plt.plot(epochs_range, val_loss, label='Validation Loss')
# # plt.legend(loc='upper right')
# # plt.title('Training and Validation Loss')
# # plt.show()


# # Save entire model to a HDF5 file
# model.save('./cats_and_dogs_filtered/models/model.h5')
# model_new.save('./cats_and_dogs_filtered/models/model_new.h5')


# # Recreate the exact same model, including weights and optimizer.
# load_model = keras.models.load_model('./cats_and_dogs_filtered/models/model.h5')
# loss, acc = load_model.evaluate(x_test, y_test)
# print("Restored model, accuracy: {:5.2f}%".format(100*acc))

# # Recreate the exact same model, including weights and optimizer.
# load_new_model = keras.models.load_model('./model_path/my_model.h5')
# loss, acc = load_new_model.evaluate(x_test, y_test)
# print("Restored model, accuracy: {:5.2f}%".format(100*acc))
