import pandas as pd

# Load dataset
file_path = "All_Months.csv"
df = pd.read_csv(file_path)

# --- Clean headers ---
df.columns = df.columns.str.strip().str.replace('\ufeff', '')

# --- Function to parse mixed date formats ---
def parse_mixed_date(x):
    if pd.isna(x):
        return pd.NaT
    try:
        # Try European style (DD-MM-YYYY, e.g. 14-01-2021)
        return pd.to_datetime(x, dayfirst=True, errors="raise")
    except:
        try:
            # Try US style (MM/DD/YYYY, e.g. 1/15/2021)
            return pd.to_datetime(x, dayfirst=False, errors="raise")
        except:
            return pd.NaT  # Not a Time if it fails both

# --- Apply to Order Date and Ship Date ---
df["Order Date"] = df["Order Date"].apply(parse_mixed_date)
df["Ship Date"] = df["Ship Date"].apply(parse_mixed_date)

# --- Standardise all to YYYY-MM-DD ---
df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d")
df["Ship Date"] = df["Ship Date"].dt.strftime("%Y-%m-%d")

# --- Save cleaned dataset ---
output_file = "All_Months_standardised_dates.csv"
df.to_csv(output_file, index=False)

print(f"✅ Mixed formats fixed → Dates standardized to YYYY-MM-DD in {output_file}")
