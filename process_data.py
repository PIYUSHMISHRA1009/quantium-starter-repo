import pandas as pd
from pathlib import Path

# Path to data folder
data_folder = Path("data")

# Read all CSV files in the data folder
csv_files = data_folder.glob("*.csv")

dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Combine all CSVs into one DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Keep only Pink Morsel rows
pink_df = combined_df[combined_df["product"] == "Pink Morsel"]

# Create sales column
pink_df["sales"] = pink_df["quantity"] * pink_df["price"]

# Select required fields
final_df = pink_df[["sales", "date", "region"]]

# Save output file
final_df.to_csv("processed_pink_morsel_sales.csv", index=False)

print("✅ Data processing complete. Output saved as processed_pink_morsel_sales.csv")
