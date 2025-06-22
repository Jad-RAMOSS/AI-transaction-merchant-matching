# 💼 Transaction Classification using BERT (Accuracy: 94.6%)

This project delivers an end-to-end NLP solution for classifying financial transaction descriptions by predicting the corresponding representative. Leveraging a fine-tuned mBERT model, the system significantly enhances classification accuracy and is designed for real-world deployment.

## 📊 Performance
- **Baseline Accuracy**: 88%
- **Final Accuracy**: **94.6%**

## 🧠 Key Features
- Preprocessing of transaction descriptions for clean input to the model
- Custom PyTorch `Dataset` class and DataLoader for efficient training
- Fine-tuning of mBERT for multi-class text classification
- Batch inference pipeline for new Excel files
- Automatic evaluation with actual vs. predicted labels and correctness flag

## 🛠️ Tech Stack
- Python
- PyTorch
- Hugging Face Transformers
- Scikit-learn
- Pandas
- Excel I/O (OpenPyXL)

## 📁 Outputs
- Trained model artifacts (`.bin` / `.pt`)
- Label encoder (`.pkl`)
- Prediction results exported to Excel
