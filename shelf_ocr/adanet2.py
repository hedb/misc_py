# A simple example of learning to ensemble linear and neural network
# models.

import string
import adanet
import pandas as pd
import tensorflow as tf
import time
# from Images_to_DF import load_image_dataset
from Images_to_DF1 import get_input_fn

start_ts = time.time()
def time_print():
    print('{} seconds elapsed'.format(time.time() - start_ts))

BATCH_SIZE = 100
LEARNING_RATE = 0.2


def get_data_sets():

    full_dataset, DATASET_SIZE = load_image_dataset()

    train_size = int(0.7 * DATASET_SIZE)
    val_size = int(0.15 * DATASET_SIZE)
    test_size = int(0.15 * DATASET_SIZE)

    train_dataset = full_dataset.take(train_size)
    test_dataset = full_dataset.skip(train_size)
    val_dataset = test_dataset.skip(test_size)
    test_dataset = test_dataset.take(test_size)
    return train_dataset,val_dataset,test_dataset

head = tf.contrib.estimator.multi_class_head(n_classes=26)

label_names = string.ascii_lowercase[:26]
feature_columns = list ([ tf.feature_column.numeric_column(key='x', shape=[1]) ])

# Learn to ensemble linear and DNN models.
estimator = adanet.AutoEnsembleEstimator(
    head=head,
    candidate_pool=[
        # tf.contrib.estimator.LinearEstimator(
        #     head=head,
        #     feature_columns=feature_columns,
        #     optimizer=tf.train.FtrlOptimizer(LEARNING_RATE)),
        tf.contrib.estimator.DNNEstimator(
            head=head,
            feature_columns=feature_columns,
            optimizer=tf.train.ProximalAdagradOptimizer(LEARNING_RATE),
            hidden_units=[1000, 500, 100])],
    max_iteration_steps=50)


# def input_fn_train():
#     train_dataset,val_dataset,test_dataset = get_data_sets()
#     return train_dataset

estimator.train(input_fn=get_input_fn(), steps=100)
time_print()
