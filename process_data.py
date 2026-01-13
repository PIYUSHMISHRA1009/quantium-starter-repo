import pandas as pd
from pathlib import Path

# Path to data folder
data_folder = Path("data")

# Read all CSV files
dataframes = []
for file in data_folder.glob("*.csv"):
    df = pd.read_csv(file)
    dataframes.append(df)

# Combine into one DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Normalize product names
combined_df["product"] = combined_df["product"].str.strip().str.lower()

# Ensure numeric types
combined_df["price"] = (
    combined_df["price"]
    .replace(r"[$,]", "", regex=True)
    .astype(float)
)
combined_df["quantity"] = pd.to_numeric(combined_df["quantity"], errors="coerce")

# Keep only pink morsel rows
pink_df = combined_df[combined_df["product"] == "pink morsel"].copy()

# Create sales column as numeric dollars
pink_df["sales"] = pink_df["quantity"] * pink_df["price"]

# Keep required columns and sort by date for downstream plotting
pink_df["date"] = pd.to_datetime(pink_df["date"])
final_df = (
    pink_df[["sales", "date", "region"]]
    .dropna(subset=["sales", "date", "region"])
    .sort_values("date")
)

# Save output
final_df.to_csv("processed_pink_morsel_sales.csv", index=False)

print("✅ Data processing complete. Output saved as processed_pink_morsel_sales.csv")
