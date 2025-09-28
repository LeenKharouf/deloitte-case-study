import pandas as pd
import glob
import os

folder_path = "most_recent_months"
all_files = glob.glob(os.path.join(folder_path, "*.csv"))

df_list = []
for filename in all_files:
    print(f"Reading {filename} ...")
    df = pd.read_csv(filename, sep="|", engine="python", encoding="latin1")
    print(df.head())  # 👈 check if columns are split correctly
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)
combined_df.to_csv("All_Months.csv", index=False)
print("✅ Combined dataset saved as All_Months.csv")
