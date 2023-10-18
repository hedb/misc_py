
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt



pd.set_option('display.max_columns', 130)

df = pd.read_csv("./TA125.output_percentage.csv")
headers = list(df.columns.values)


q95_90 = []
i = 0
for column in df:
    if i>0:
        q95_90.append(df[column].quantile(.95) - df[column].quantile(.90) )
    i += 1

plt.plot(q95_90)
plt.show()
