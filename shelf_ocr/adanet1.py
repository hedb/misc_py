# A simple example of learning to ensemble linear and neural network
# models.

import adanet
import pandas as pd
import tensorflow as tf
import time

start_ts = time.time()
def time_print():
    print('{} seconds elapsed'.format(time.time() - start_ts))

BATCH_SIZE = 100
LEARNING_RATE = 0.2
TRAIN_URL = "http://download.tensorflow.org/data/iris_training.csv"
TEST_URL = "http://download.tensorflow.org/data/iris_test.csv"

CSV_COLUMN_NAMES = ['SepalLength', 'SepalWidth',
                    'PetalLength', 'PetalWidth', 'Species']
SPECIES = ['Setosa', 'Versicolor', 'Virginica']



def maybe_download():
    train_path = tf.keras.utils.get_file(TRAIN_URL.split('/')[-1], TRAIN_URL)
    test_path = tf.keras.utils.get_file(TEST_URL.split('/')[-1], TEST_URL)

    return train_path, test_path

def load_data(y_name='Species'):
    """Returns the iris dataset as (train_x, train_y), (test_x, test_y)."""
    train_path, test_path = maybe_download()

    train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
    train_x, train_y = train, train.pop(y_name)

    test1 = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)

    predict = test1.iloc[:2,:]
    test = test1.iloc[2:,:]

    test_x, test_y = test, test.pop(y_name)
    predict_x, predict_y = predict, predict.pop(y_name)

    return (train_x, train_y), (test_x, test_y), (predict_x, predict_y)



(train_x, train_y), (test_x, test_y), (predict_x, predict_y) = load_data()

print(train_x.shape)
print(train_y.shape)
exit()

for df in [train_x, train_y, test_x, test_y, predict_x, predict_y]:
    print(df.shape)



feature_columns = list([
        tf.feature_column.numeric_column(key='SepalLength', shape=[1]),
        tf.feature_column.numeric_column(key='SepalWidth', shape=[1]),
        tf.feature_column.numeric_column(key='PetalLength', shape=[1]),
        tf.feature_column.numeric_column(key='PetalWidth', shape=[1])
    ])


head = tf.contrib.estimator.multi_class_head(n_classes=3)

# Learn to ensemble linear and DNN models.
estimator = adanet.AutoEnsembleEstimator(
    head=head,
    candidate_pool=[
        tf.contrib.estimator.LinearEstimator(
            head=head,
            feature_columns=feature_columns,
            optimizer=tf.train.FtrlOptimizer(LEARNING_RATE)),
        tf.contrib.estimator.DNNEstimator(
            head=head,
            feature_columns=feature_columns,
            optimizer=tf.train.ProximalAdagradOptimizer(LEARNING_RATE),
            hidden_units=[1000, 500, 100])],
    max_iteration_steps=50)

# Input builders
def input_fn_train() :

    dataset = tf.data.Dataset.from_tensor_slices((dict(train_x), train_y))
    dataset = dataset.shuffle(1000).repeat().batch(BATCH_SIZE)

    iterator = dataset.make_one_shot_iterator()
    features, labels = iterator.get_next()

    print("Train data is:", train_x.shape, train_y.shape)
    return features, labels

def input_fn_eval () :

    dataset = tf.data.Dataset.from_tensor_slices((dict(test_x), test_y))
    dataset = dataset.shuffle(1000).repeat().batch(BATCH_SIZE)

    iterator = dataset.make_one_shot_iterator()
    features, labels = iterator.get_next()

    print("Test data is:", test_x.shape, test_y.shape)
    return features, labels


def input_fn_predict ():
    dataset = tf.data.Dataset.from_tensor_slices((dict(predict_x), predict_y))
    dataset = dataset.batch(1)

    iterator = dataset.make_one_shot_iterator()
    features, labels = iterator.get_next()

    print("Predict data is:", predict_x.shape, predict_y.shape)
    return features, labels


estimator.train(input_fn=input_fn_train, steps=100)
time_print()

metrics = estimator.evaluate(input_fn=input_fn_eval, steps=10)
time_print()
print("Model Results:\n", metrics)

predictions = estimator.predict(input_fn=input_fn_predict)

for p in predictions:
    print(p)
