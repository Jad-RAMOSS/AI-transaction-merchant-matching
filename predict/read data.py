import pandas as pd
import os
import glob
from clean_data import clean_data
from dotenv import load_dotenv 

load_dotenv()

# Folder containing Excel files

folder_path = os.getenv("raw_data_path")

# Get all Excel files (excluding temporary files like ~$)
excel_files = [f for f in glob.glob(os.path.join(folder_path, "*.xls*")) if not os.path.basename(f).startswith("~$")]

# Columns to keep
columns_to_keep = ["description", "rep"]  # Adjust if needed

# List to hold DataFrames
selected_dataframes = []

for file in excel_files:
    try:
        df = pd.read_excel(file)
        df.columns = [col.lower() for col in df.columns]
        df = df[columns_to_keep]  # Keep only selected columns
        selected_dataframes.append(df)
    except Exception as e:
        print(f"Skipping {file}: {e}")

# Combine and save
if selected_dataframes:
    combined_df = pd.concat(selected_dataframes, ignore_index=True)
    output_file = os.path.join(folder_path, "combined_output.xlsx")
    combined_df.to_excel(output_file, index=False)
    print(f"Saved combined file to: {output_file}")
    clean_data(combined_df)
    
else:
    print("No valid files were found or columns not matched.")
