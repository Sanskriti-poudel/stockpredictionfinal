import os
import pandas as pd
import json

# Define paths
excel_dir = "stockprediction/data/historical"
json_dir = "static/stockprediction/data/json"

# Ensure output directory exists
os.makedirs(json_dir, exist_ok=True)

# Loop through Excel files
for file in os.listdir(excel_dir):
    if file.endswith(".xlsx"):
        try:
            symbol = file.replace(".xlsx", "").upper()
            file_path = os.path.join(excel_dir, file)

            # Read Excel
            df = pd.read_excel(file_path)

            # Keep only Date and LTP
            df = df[["Date", "LTP"]]
            df.dropna(inplace=True)

            # Convert to list of dicts
            records = df.to_dict(orient="records")

            # Save to JSON
            output_path = os.path.join(json_dir, f"{symbol}.json")
            with open(output_path, "w") as f:
                json.dump(records, f, indent=2, default=str)  # ensure Date is stringified

            print(f"✅ Converted: {file} -> {symbol}.json")

        except Exception as e:
            print(f"❌ Failed for {file}: {e}")
