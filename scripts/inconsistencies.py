import pandas as pd

# Load dataset
file_path = "All_Months_standardized_dates.csv"
df = pd.read_csv(file_path)

# Clean headers
df.columns = df.columns.str.strip().str.replace('\ufeff', '')

# Normalize Order ID
df["Order ID"] = df["Order ID"].astype(str).str.strip().str.upper()

# --- Issues dict ---
issues = {}

# 1. Negative Quantity
issues["negative_quantity"] = df[df["Quantity"] < 0]

# 2. Negative Sales
issues["negative_sales"] = df[df["Sales"] < 0]

# 3. Negative Profit
issues["negative_profit"] = df[df["Profit"] < 0]

# 4. Invalid Discounts
issues["invalid_discount"] = df[(df["Discount"] < 0) | (df["Discount"] > 1)]

# 5. Invalid Dates (Ship < Order)
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce", dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce", dayfirst=True)
issues["invalid_dates"] = df[
    (df["Order Date"].notna()) &
    (df["Ship Date"].notna()) &
    (df["Ship Date"] < df["Order Date"])
]

# 6. Exact Duplicates
issues["exact_duplicates"] = df[df.duplicated(keep=False)]
# this is when the whole row is duplicated exactly -> we can just delete one copy as the info is redundant

# 7. Duplicate Order Lines (same OrderID + ProductID)
issues["duplicate_order_lines"] = df[df.duplicated(subset=["Order ID","Product ID"], keep=False)]

# 8. Missing Values
issues["missing_values"] = df[df.isnull().any(axis=1)]

# 9. Mixed Data Types
dtype_report = []
for col in df.columns:
    unique_types = df[col].dropna().apply(type).unique()
    if len(unique_types) > 1:
        dtype_report.append({"Column": col, "Types": [t.__name__ for t in unique_types]})
if dtype_report:
    issues["mixed_data_types"] = pd.DataFrame(dtype_report)

# --- Save individual CSVs for each issue ---
for name, rows in issues.items():
    if not rows.empty:
        rows.to_csv(f"{name}.csv", index=False)

    # just a preference

# --- Build Excel Deliverable ---
with pd.ExcelWriter("Task_5_Inconsistencies_Analysis.xlsx") as writer:
    descriptions = {
        "negative_quantity": "Quantity is less than 0, which is invalid for an order",
        "negative_sales": "Sales values are negative, which may indicate refunds or incorrect data",
        "negative_profit": "Profit values are negative, which may be real losses or data errors",
        "invalid_discount": "Discount values are outside the range 0–1",
        "invalid_dates": "Ship Date occurs before Order Date",
        "exact_duplicates": "Entire row is duplicated",
        "duplicate_order_lines": "Same Order ID and Product ID are repeated",
        "missing_values": "One or more required fields are empty",
        "mixed_data_types": "A column contains mixed data types (e.g., numbers and text)"
    }
    suggestions = {
        "negative_quantity": "Needs SME review; could be data entry issue",
        "negative_sales": "Needs SME clarification (refund vs. error)",
        "negative_profit": "Keep if true losses, else SME review",
        "invalid_discount": "Clamp values between 0 and 1",
        "invalid_dates": "Flag rows; SME clarification required",
        "exact_duplicates": "Remove exact duplicate rows",
        "duplicate_order_lines": "Needs SME review (could be legit multiple lines)",
        "missing_values": "Impute if possible, otherwise flag",
        "mixed_data_types": "Normalize to consistent type"
    }

    summary = []
    for name, rows in issues.items():
        if not rows.empty:
            summary.append({
                "Inconsistency Type": name.replace("_"," ").title(),
                "Description": descriptions.get(name, "N/A"),
                "Suggestion to Handle": suggestions.get(name, "Review required"),
                "Distinct Count of Row ID": len(rows)
            })
    pd.DataFrame(summary).to_excel(writer, sheet_name="Inconsistencies_Summary", index=False)

    # 2. Examples (2 rows per issue)
    examples = []
    for name, rows in issues.items():
        if not rows.empty and name != "mixed_data_types":
            sample = rows.head(2).copy()
            sample.insert(0, "Inconsistency Type", name.replace("_"," ").title())
            examples.append(sample)
    if examples:
        pd.concat(examples).to_excel(writer, sheet_name="Inconsistencies_Examples", index=False)

    # 3. Quality Report (SME-only issues)
    sme_issues = [
        "negative_quantity",
        "negative_sales",
        "negative_profit",
        "invalid_dates",
        "duplicate_order_lines",
        "mixed_data_types",
        "missing_values"
    ]
    sme_rows = []
    for name in sme_issues:
        if name in issues and not issues[name].empty:
            tmp = issues[name].copy()
            tmp.insert(0, "Issue Type", name.replace("_"," ").title())
            sme_rows.append(tmp)
    if sme_rows:
        pd.concat(sme_rows).to_excel(writer, sheet_name="Quality_Report", index=False)

print("✅ Task_5_Inconsistencies_Analysis.xlsx generated with 3 sheets (SME list updated)")
