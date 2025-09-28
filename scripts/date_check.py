import pandas as pd

# Load dataset
file_path = "All_Months_Combined_final.csv"
df = pd.read_csv(file_path)

# Clean headers
df.columns = df.columns.str.strip().str.replace('\ufeff', '')

# Count cells with '/' in Order Date and Ship Date
order_slash_count = df["Order Date"].astype(str).str.contains("/", na=False).sum()
ship_slash_count = df["Ship Date"].astype(str).str.contains("/", na=False).sum()

print("🔎 Date Format Check:")
print(f"Order Date cells with '/': {order_slash_count}")
print(f"Ship Date cells with '/': {ship_slash_count}")
print(f"Total cells with '/': {order_slash_count + ship_slash_count}")

# Optional: save examples
examples = df[
    df["Order Date"].astype(str).str.contains("/", na=False) |
    df["Ship Date"].astype(str).str.contains("/", na=False)
]
examples.head(10).to_csv("date_slash_examples.csv", index=False)

print("\n📂 Saved first 10 examples to date_slash_examples.csv")
