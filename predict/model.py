from transformers import BertTokenizer, BertForSequenceClassification
import joblib
import torch
import torch.nn.functional as F

# model_path="D:/projects/Transaction-Matching/saved model"
# encoder_path="D:/projects/Transaction-Matching/saved model/label_encoder.pkl"

def call_model(model_path, encoder_path):
    model = BertForSequenceClassification.from_pretrained(model_path, local_files_only=True)
    tokenizer = BertTokenizer.from_pretrained(model_path, local_files_only=True)
    le = joblib.load(encoder_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)
    model.to(device)
    return model, tokenizer, le


def predict(model, data_loader, label_encoder, threshold=0.9, temperature=2.0):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model.eval()
    all_preds, all_texts, all_dates, all_amounts = [], [], [], []

    with torch.no_grad():
        for batch in data_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            texts = batch['description']
            batch_dates = batch['date']
            batch_amounts = batch['amount']

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits / temperature
            probs = F.softmax(logits, dim=1)
            max_probs, pred_indices = torch.max(probs, dim=1)

            for prob, idx in zip(max_probs.cpu(), pred_indices.cpu()):
                if prob >= threshold:
                    pred_label = label_encoder.inverse_transform([idx.item()])[0]
                else:
                    pred_label = "Unknown"
                all_preds.append(pred_label)

            all_texts.extend(texts)
            all_dates.extend(batch_dates)
            all_amounts.extend(batch_amounts)

    return all_texts, all_preds, all_dates, all_amounts





