import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Read the CSV file into a DataFrame
df = pd.read_csv('tmp_data1.csv', )

X = df.drop(columns=['conversion','realm_id'])
y = df['conversion']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

dtrain = xgb.DMatrix(X_train, y_train)
dtest = xgb.DMatrix(X_test, y_test)

param = {
    'max_depth': 3,
    'eta': 0.1,
    'objective': 'binary:logistic'
}

model = xgb.train(param, dtrain)
predictions = model.predict(dtest)

#clone predictions to a new array
predictions_raw = predictions.copy()



# Convert predictions to binary values
for i in range(len(predictions)):
    if predictions[i] >= 0.5:
        predictions[i] = 1
    else:
        predictions[i] = 0

# print y_test and predictions side by side
for i in range(len(y_test)):
    print(y_test.iloc[i], predictions[i],predictions_raw[i])


accuracy = accuracy_score(y_test, predictions)
print('Accuracy:', accuracy)

#pritn the xgboost model parameters
print(model.get_params())
