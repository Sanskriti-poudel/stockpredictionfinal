import pandas as pd

# Load the Excel
df = pd.read_excel("predicted_next_day_LTP.xlsx")

# inspect the columns
print(df.columns)

# if the columns are "Stock" and "Predicted_LTP", we can convert like this:
predictions = dict(zip(df['Symbol'], df['Predicted LTP']))

import json

# save as JSON
with open("predicted_ltp.json", "w") as f:
    json.dump(predictions, f, indent=2)

print("✅ JSON saved as predicted_ltp.json")
