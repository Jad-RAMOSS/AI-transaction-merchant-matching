import pandas as pd
from model import call_model,predict
from embedding import embedded,decoded


def main():
    data_path='D:/projects/Transaction-Matching/data/NEWtest2.xlsx'
    model_path="D:/projects/Transaction-Matching/saved model"
    encoder_path="D:/projects/Transaction-Matching/saved model/label_encoder.pkl"

    model,tokenizer,le =call_model(model_path,encoder_path)
    print("================================== model succcesss =====================================")
    data_loader=embedded(data_path,tokenizer)
    print("================================== data_loader succcesss =====================================")
    all_texts,all_preds,all_dates,all_amounts=predict(model,data_loader)
    print("================================== predict succcesss =====================================")
    result=decoded(all_texts,all_preds,all_dates,all_amounts,le)
    print(result)
    result.to_excel('D:/projects/Transaction-Matching/data/predict.xlsx', index=False)






if __name__ == "__main__":
    main()