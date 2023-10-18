
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt


strategy = {"stock":1,
            "predictors":[
                [{"ind":2,"days_back":3,"change":0.03}, [{"ind":2,"days_back":3,"change":0.03}]],
                [{"ind":4,"days_back":3,"change":0.03}]
            ]}

df = pd.read_csv("./TA125.output_percentage.csv")

for day in df.iloc[:,[0]].iterrows():
    print (day[1][0])

