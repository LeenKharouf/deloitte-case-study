import pandas as pd
import os
import zipfile

# --- Load Cleaned Dataset ---
file_path = "All_Months_Combined_Cleaned_dates.csv"  # make sure this exists from Task 5
df = pd.read_csv(file_path)

# Clean headers
df.columns = df.columns.str.strip().str.replace('\ufeff', '')

# --- Exclude SME-flagged inconsistencies ---
sme_filter = (
    (df["Quantity"] < 0) |                   # Negative Quantity
    (df["Profit"] < 0) |                     # Negative Profit
    (df.duplicated(subset=["Order ID","Product ID"], keep=False)) |  # Duplicate Order Lines
    (df.isnull().any(axis=1))                 # Missing Values
)

clean_df = df[~sme_filter].copy()  # keep only rows not flagged

print(f"✅ Excluded {sme_filter.sum()} SME-flagged rows, {len(clean_df)} rows remain for marts")

# --- Build Data Marts ---

# 1. DimCustomer
dim_customer = clean_df[["Customer ID", "Customer Name", "Segment"]].drop_duplicates().reset_index(drop=True)

# 2. DimProduct
dim_product = clean_df[["Product ID", "Category", "Sub-Category", "Product Name"]].drop_duplicates().reset_index(drop=True)

# 3. DimGeography
dim_geography = clean_df[["Country", "City", "State", "Postal Code", "Region"]].drop_duplicates().reset_index(drop=True)
dim_geography["GeographyID"] = dim_geography.index + 1  # surrogate key

# 4. FactOrders (link to GeographyID)
fact_orders = clean_df[[
    "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
    "Customer ID", "Product ID", "Sales", "Quantity", "Discount", "Profit",
    "Country", "City", "State", "Postal Code", "Region"
]].copy()

# Join with DimGeography to assign GeographyID
fact_orders = fact_orders.merge(
    dim_geography,
    on=["Country", "City", "State", "Postal Code", "Region"],
    how="left"
)

# Keep only normalized columns
fact_orders = fact_orders[[
    "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
    "Customer ID", "Product ID", "GeographyID",
    "Sales", "Quantity", "Discount", "Profit"
]]

# --- Export Each to CSV ---
os.makedirs("data_marts", exist_ok=True)
dim_customer.to_csv("data_marts/DimCustomer.csv", index=False)
dim_product.to_csv("data_marts/DimProduct.csv", index=False)
dim_geography.to_csv("data_marts/DimGeography.csv", index=False)
fact_orders.to_csv("data_marts/FactOrders.csv", index=False)

# --- Create ZIP Archive ---
with zipfile.ZipFile("Task_6_1_Data_Marts.zip", "w") as z:
    for file in os.listdir("data_marts"):
        z.write(os.path.join("data_marts", file), file)

# --- Row & Key Counts Summary ---
summary = []

summary.append({
    "Data Mart System Name": "DimCustomer",
    "Count Rows": len(dim_customer),
    "Count Distinct Primary Key": dim_customer["Customer ID"].nunique()
})

summary.append({
    "Data Mart System Name": "DimProduct",
    "Count Rows": len(dim_product),
    "Count Distinct Primary Key": dim_product["Product ID"].nunique()
})

summary.append({
    "Data Mart System Name": "DimGeography",
    "Count Rows": len(dim_geography),
    "Count Distinct Primary Key": dim_geography["GeographyID"].nunique()
})

summary.append({
    "Data Mart System Name": "FactOrders",
    "Count Rows": len(fact_orders),
    "Count Distinct Primary Key": fact_orders["Order ID"].nunique(),
    "Count Distinct Row ID": fact_orders["Row ID"].nunique()
})

pd.DataFrame(summary).to_csv("Task_6_2_Data_Marts_Rows.csv", index=False)

print("✅ Task 6 Deliverables generated:")
print("- Task_6_1_Data_Marts.zip (contains 4 clean Data Marts)")
print("- Task_6_2_Data_Marts_Rows.csv (row/key counts)")