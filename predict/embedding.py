import pandas as pd
from torch.utils.data import DataLoader,Dataset
from clean_data import clean_pre_data
import math

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
    dates = test_data['Transaction Date'].tolist() if 'Date' in test_data.columns else [''] * len(test_data)
    amounts = test_data['Amount'].tolist() if 'Amount' in test_data.columns else [''] * len(test_data)

    # actual_reps = test_data['Rep'].astype(str).tolist()

    encodings = tokenizer(descriptions, truncation=True, padding=True, return_tensors='pt')
    dataset = TextDataset(encodings, descriptions,dates,amounts)
    loader = DataLoader(dataset, batch_size=batch_size)
    return loader, test_data

def decoded(all_texts, all_pred, test_data, le):
    pred_labels = []
    for p in all_pred:
        if p is None or (isinstance(p, float) and math.isnan(p)):
            pred_labels.append("unknown")
        elif isinstance(p, str):
            pred_labels.append(p.lower().replace(' ', ''))
        else:
            label = le.inverse_transform([p])[0]
            pred_labels.append(label.lower().replace(' ', ''))

    # Ensure dates are in datetime format and format consistently
    date_column = 'Transaction Date' if 'Transaction Date' in test_data.columns else 'Date'
    dates = pd.to_datetime(test_data[date_column], errors='coerce')
    
    # Results DataFrame
    result_df = pd.DataFrame({
        'Date': dates,
        'Amount': test_data['Amount'],
        'Description': all_texts,
        'Rep': pred_labels,
        'Reference_Number': test_data['Transaction Reference No.']
    })

    # Format dates to 'YYYY-MM-DD HH:MM:SS'
    result_df['Date'] = result_df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    result_df['Date'] = result_df['Date'].replace('NaT', '')

    if 'original_rep' in test_data.columns:
        result_df['ManualRep'] = test_data['original_rep']
        result_df['ManualRep'] = result_df['ManualRep'].str.lower().str.replace(" ", "", regex=False)
        result_df['ManualRep'] = result_df['ManualRep'].str.replace(r'\s+', '', regex=True)
        result_df['is_correct'] = result_df['ManualRep'] == result_df['Rep']
    
    return result_df

