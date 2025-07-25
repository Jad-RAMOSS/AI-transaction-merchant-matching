import pandas as pd
from model import call_model,predict
from embedding import embedded,decoded
from data_to_oracle import export_to_oracle
import os
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, DATE, FLOAT, INTEGER
import urllib.parse


def main():
    data_path='C:\\AI Merchant Transaction Matching\\BERT_api\\data\\Test\\NBE & BM 16-7-2025.xlsx'
    model_path="C:\\AI Merchant Transaction Matching\\BERT_api\\predict\\saved_model"
    encoder_path="C:\\AI Merchant Transaction Matching\\BERT_api\\predict\\saved_model\\label_encoder.pkl"
    
    model,tokenizer,le =call_model(model_path,encoder_path)
    print("================================== model succcesss =====================================")
    data_loader, test_data = embedded(data_path,tokenizer)
    print("================================== data_loader succcesss =====================================")
    all_texts,all_preds,all_dates,all_amounts,confidences,is_confident=predict(model,data_loader,label_encoder=le, threshold=0.52, temperature=1.6)
    print("================================== predict succcesss =====================================")
    result=decoded(all_texts,all_preds,confidences,is_confident,test_data,le)
    print(result)
    file_name = os.path.basename(data_path).split('.')[0]
    # Save to Excel and CSV
    result.to_excel(f'C:\\AI Merchant Transaction Matching\\BERT_api\\output\\prediction_{file_name}.xlsx', index=False)
    result.to_csv(f'C:\\AI Merchant Transaction Matching\\BERT_api\\output\\prediction_{file_name}.csv', index=False)
    
    # Export to Oracle Database
    # export_to_oracle(result)







if __name__ == "__main__":
    main()