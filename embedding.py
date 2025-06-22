
import pandas as pd
from torch.utils.data import DataLoader,Dataset
from clean_data import clean_pre_data

class TextDataset(Dataset):
    def __init__(self, encodings, descriptions,dates,amounts):
        self.encodings = encodings
        self.descriptions = descriptions
        self.dates = dates
        self.amounts = amounts

    def __getitem__(self, idx):
        return {
            'input_ids': self.encodings['input_ids'][idx],
            'attention_mask': self.encodings['attention_mask'][idx],
            'description': self.descriptions[idx],
            'date': self.dates[idx],
            'amount': self.amounts[idx]
        }

    def __len__(self):
        return len(self.descriptions)
    

def embedded(data_path, tokenizer, batch_size=16):
    # Load and clean data
    test_data = clean_pre_data(data_path)
    test_data = test_data[test_data['Description'].apply(lambda x: isinstance(x, str))]
    test_data.dropna(subset=['Description'], inplace=True)

    # Prepare inputs
    descriptions = test_data['Description'].astype(str).tolist()
    dates = test_data['Value Date'].tolist() if 'Date' in test_data.columns else [''] * len(test_data)
    amounts = test_data['Amount'].tolist() if 'Amount' in test_data.columns else [''] * len(test_data)

    # actual_reps = test_data['Rep'].astype(str).tolist()

    encodings = tokenizer(descriptions, truncation=True, padding=True, return_tensors='pt')
    dataset = TextDataset(encodings, descriptions,dates,amounts)
    loader = DataLoader(dataset, batch_size=batch_size)
    return loader

def decoded(all_texts,all_pred,all_dates,all_amounts,le):
    pred_labels = le.inverse_transform(all_pred)

    # Results DataFrame
    result_df = pd.DataFrame({
        'Date': all_dates,
        'Amount': all_amounts,
        'Description': all_texts,
        'Predicted_Rep': pred_labels
     })

    return result_df
