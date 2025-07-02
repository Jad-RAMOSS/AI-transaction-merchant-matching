import pandas as pd 
# import numpy as np
# import re
# data_path='D:/projects/Transaction-Matching/data/combined_output.xlsx'
def clean_data(data):
    ##DROP INSTA AND NULL
    data = data[data['description'].apply(lambda x: isinstance(x, str))]
    data = data[~data['description'].str.contains('IPN', case=False)]
    
    data.dropna(subset=['description', 'rep'], inplace=True)


    ## Rep
    # data['Rep'] =data['Rep'].str.lower()
    # data['Rep'] = data['Rep'].str.lower().str.strip()
    data['rep'] = data['rep'].str.lower().str.replace(" ", "", regex=False)

    ## Description
    data['description'] = data['description'].str.replace(r'^.*?(?:\|| {3,})', '', regex=True)

    data.to_excel('C:\\AI Merchant Transaction Matching\\BERT_api\\data\\Cleaned\\Cleaned_DATA.xlsx', index=False)
    print("cleaned data saved")
    return data


def clean_pre_data(data_path):
    data=pd.read_excel(data_path)
    ##DROP INSTA AND NULL
    data = data[data['Description'].apply(lambda x: isinstance(x, str))]
    data = data[~data['Description'].str.contains('IPN', case=False)]

    ## Description
    data['Description'] = data['Description'].str.replace(r'^.*?(?:\|| {3,})', '', regex=True)

    return data

