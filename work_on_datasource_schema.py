import pandas as pd
import numpy as np
# import statsmodels.api as sm


def modify_input() :
    df = pd.read_csv("C:/Users/hedbn/Desktop/experts_training/experts_training.csv")

    for col_name in df:
        # print(col_name + " : " + str( df["arrange_elements"].unique().size ) )
        # print(col_name + " : " + str(df["arrange_elements"].unique()))
        unique_values = df[col_name].unique()
        if (unique_values.size == 3):
            if (str(unique_values) == '[ nan   0.   1.]' or str(unique_values) == '[ nan   1.   0.]'):
                df[col_name] = df[col_name].apply(
                    lambda x:
                        'True' if (x==1) else 'False'
                )
            else :
                print ( col_name + " : " + str(unique_values) )

    df.to_csv("C:/Users/hedbn/Desktop/experts_training/experts_training_modified.csv")




