import os
import pandas as pd
from model import call_model, predict
from embedding import embedded, decoded
from data_to_oracle import export_to_oracle

# Paths to model artefacts (adjust if you move folders)
MODEL_DIR = "saved_model"
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")


def process_file(file_path: str) -> pd.DataFrame:
    """Full pipeline: given an Excel/CSV file path, run prediction & export to Oracle.

    Returns the resulting dataframe that was exported.
    """
    # 1. Load model & encoder
    print("jad")
    model, tokenizer, le = call_model(MODEL_DIR, ENCODER_PATH)
    print("jad2")
    # 2. Prepare data
    data_loader, test_data = embedded(file_path, tokenizer)

    # 3. Run predictions
    all_texts, all_preds, *_ = predict(model, data_loader)

    # 4. Decode predictions into final result dataframe
    result_df = decoded(all_texts, all_preds, test_data, le)

    # 5. Persist locally (optional diagnostics)
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    result_df.to_excel(os.path.join(output_dir, f"prediction_{base_name}.xlsx"), index=False)
    result_df.to_csv(os.path.join(output_dir, f"prediction_{base_name}.csv"), index=False)

    # 6. Export to Oracle DB
    # export_to_oracle(result_df)

    return result_df
