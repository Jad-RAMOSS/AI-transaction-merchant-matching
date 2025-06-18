import pandas as pd 
import numpy as np
import re
data_path='data/combined_output.xlsx'
def clean_data(data_path):
    data=pd.read_excel(data_path)
    ##DROP INSTA AND NULL
    data = data[~data['Description'].str.contains('IPN', na=False)]
    data.dropna(inplace=True)

    ## Rep
    data['Rep'] =data['Rep'].str.lower()

    ## Description
    data['Description'] = data['Description'].str.replace(r'^.*?(?:\|| {3,})', '', regex=True)

    # data.to_excel('D:/projects/Transaction-Matching/data/NEW.xlsx', index=False)
    return data


print(clean_data(data_path))

