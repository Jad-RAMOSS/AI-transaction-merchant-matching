import pandas as pd
import os
import glob

# Folder containing Excel files
folder_path = "D:/projects/Damen-AI-Merchant-Transaction-Matching/Machine Learning/data/raw"

# Get all Excel files (excluding temporary files like ~$)
excel_files = [f for f in glob.glob(os.path.join(folder_path, "*.xls*")) if not os.path.basename(f).startswith("~$")]

# Columns to keep
columns_to_keep = ["Description", "Rep"]  # Adjust if needed

# List to hold DataFrames
selected_dataframes = []

for file in excel_files:
    try:
        df = pd.read_excel(file)
        df = df[columns_to_keep]  # Keep only selected columns
        selected_dataframes.append(df)
    except Exception as e:
        print(f"Skipping {file}: {e}")

# Combine and save
if selected_dataframes:
    combined_df = pd.concat(selected_dataframes, ignore_index=True)
    output_file = os.path.join(folder_path, "D:/projects/Transaction-Matching/data/combined_output.xlsx")
    combined_df.to_excel(output_file, index=False)
    print(f"Saved combined file to: {output_file}")
else:
    print("No valid files were found or columns not matched.")
