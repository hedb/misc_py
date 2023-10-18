
import os
import string
import tensorflow as tf
import imageio
import numpy  as np

label_names = string.ascii_lowercase[:26]
LABELS_NAME_TO_INDEX_MAP = dict((name, index) for index, name in enumerate(label_names))
IMAGE_DIR = 'C:/Users/hedbn/Desktop/shelf_ocr/training_sets/one_letter/'
# IMAGE_DIR = 'C:/Users/hedbn/Desktop/shelf_ocr/test_images/'

image_paths = []
image_labels = []

for filename in os.listdir(IMAGE_DIR):
    image_labels.append(LABELS_NAME_TO_INDEX_MAP[filename[:1]])
    image_paths.append(IMAGE_DIR + filename)

def get_input_fn():

    images_arr_simple = []
    for path in image_paths:
        image1 = imageio.imread(path)
        image = image1 / 255.0  # normalize to [0,1] range
        images_arr_simple.append(image)

    images_arr = np.array(images_arr_simple)

    ret = tf.estimator.inputs.numpy_input_fn(
        x={"x": images_arr},
        y=np.array(image_labels),
        num_epochs=1,
        shuffle=True)

    return ret

# print(type(get_input_fn()))