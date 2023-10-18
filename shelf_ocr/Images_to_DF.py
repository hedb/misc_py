import matplotlib.pyplot as plt
import pandas as pd
import os
import string
import tensorflow as tf

# tf.enable_eager_execution()
# tf.VERSION
# AUTOTUNE = tf.data.experimental.AUTOTUNE

def load_image_dataset():
    label_names = string.ascii_lowercase[:26]
    label_to_index = dict((name, index) for index,name in enumerate(label_names))


    image_paths = []
    image_labels = []

    dir = 'C:/Users/hedbn/Desktop/shelf_ocr/training_sets/one_letter/'
    for filename in os.listdir(dir):
        image_labels.append(label_to_index[filename[:1]])
        image_paths.append(dir + filename)


    path_ds = tf.data.Dataset.from_tensor_slices(image_paths)

    def preprocess_image(image):
      image = tf.image.decode_jpeg(image, channels=3)
      image = tf.image.resize_images(image, [100, 100])
      image /= 255.0  # normalize to [0,1] range

      return image

    def load_and_preprocess_image(path):
      image = tf.read_file(path)
      return preprocess_image(image)


    image_ds = path_ds.map(load_and_preprocess_image)#, num_parallel_calls=AUTOTUNE)

    label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(image_labels, tf.int64))

    image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))

    BATCH_SIZE = 32

    # Setting a shuffle buffer size as large as the dataset ensures that the data is
    # completely shuffled.
    ds = image_label_ds.shuffle(buffer_size=len(image_paths))
    ds = ds.repeat()
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(buffer_size=10)
    return ds, len(image_paths)

