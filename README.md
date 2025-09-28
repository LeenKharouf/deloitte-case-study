<p align="left">
  <img src="deloitte_logo2.jpeg" alt="Deloitte" width="120">
</p>

<br>

# Data Engineering Case Study: Data Engineering and Master Data Management MVP for Retail Orders Analytics

<br>
<!-- Optional logo (place your file at assets/deloitte_logo.png)
     Change size by editing width="120" (e.g., 90 or 150). -->

This project delivers an end-to-end **ETL & Data Quality** pipeline for monthly sales data:
- Ingest latest monthly files
- Combine and standardise
- Profile and flag inconsistencies (with an SME review track)
- Normalise to a **star schema** (Fact + Dimensions)
- Export **clean data marts** + produce a **row/PK audit report**

<br>

---
<br>

## 📂 Project Overview
Tasks covered: KPI glossary, HLD, ERD, DDL, inconsistency analysis, data marts, and final documentation.  
This README links the scripts and shows + explains the workflow.

<br>

---
<br>

## Pipeline Workflow  

### 1️⃣ Extract Recent Data
**Script:** [scripts/most_recent_months.py](scripts/most_recent_months.py)  

#### What it does
- Picks the latest CSV for each month  
- Saves them into `most_recent_months/`  

<br>

---
<br>

### 2️⃣ Build Master Dataset
**Script:** [scripts/master_dataset.py](scripts/master_dataset.py)  

#### What it does
- Combines all recent CSVs into `All_Months_Combined.csv`  

<br>

---
<br>

### 3️⃣ Date Quality Check
**Script:** [scripts/date_check.py](scripts/date_check.py)  

#### What it does
- Counts `/` vs `-` in dates  
- Useful for spotting format inconsistencies  

#### Why this matters
Different tools interpret and display dates differently:  
- **Excel** might display everything in `/` style (MM/DD/YYYY)  
- **Google Sheets** may show `-` style (DD-MM-YYYY)  
This means the same row can look different depending on where you open it.  
⚠️ Because of this, the check is only approximate — it’s meant as a rough indicator, not a reliable fix.

<br>

---
<br>

### 4️⃣ Date Standardization
**Script:** [scripts/dates_standardiser.py](scripts/dates_standardiser.py)  

#### What it does
- Converts European (DD-MM-YYYY) and US (MM/DD/YYYY) into standard `YYYY-MM-DD`  
- Outputs: `All_Months_Standardised_Dates.csv`

#### Why this matters
Since display depends on the software, detecting “bad” dates with a script isn’t 100% possible.  
The safest solution is to **force all formats into a single standard** — which is what this script does.  
This ensures downstream checks (inconsistencies, marts) don’t misread the date fields.

<br>

---
<br>

### 5️⃣ Inconsistency Analysis (Task 5)
**Script:** [scripts/inconsistencies.py](scripts/inconsistencies.py)  

#### What it does
- Flags: Negative Quantity, Negative Profit, Duplicates, Missing Values, etc.  
- Produces: `deliverables/Task_5_Inconsistencies_Analysis.xlsx`  

<br>

---
<br>

### 6️⃣ Data Marts (Task 6)
**Script:** [scripts/data_mart.py](scripts/data_mart.py)  

#### What it does
- Excludes SME-flagged rows  
- Creates star-schema CSVs in `deliverables/Task_6_1_Data_Marts.zip`  
- Generates audit report: `deliverables/Task_6_2_Data_Marts_Rows.csv`

---

### Results — What the Data Marts Show  

From `deliverables/Task_6_2_Data_Marts_Rows.csv`:

| Data Mart      | Rows   | Distinct PK (column) | Distinct Row ID (Fact only) |
|----------------|--------|----------------------|------------------------------|
| DimCustomer    | 791    | 791 (`Customer ID`)  | —                            |
| DimProduct     | 1,841  | 1,837 (`Product ID`) | —                            |
| DimGeography   | 607    | 607 (`GeographyID`)  | —                            |
| FactOrders     | 7,920  | 4,312 (`Order ID`)   | 7,920 (`Row ID`)             |

**Interpretation:**
- **DimCustomer** — each customer is unique (clean dimension).  
- **DimProduct** — 1,841 rows but only 1,837 unique IDs → 4 duplicate products detected. This links back to source inconsistencies (e.g., same product described differently).  
- **DimGeography** — geography dimension is consistent (no duplicates).  
- **FactOrders** — 7,920 rows but only 4,312 distinct orders → multiple product lines per order. `Row ID` ensures each line remains unique.  

<br>

---
<br>

### 7️⃣ Final Documentation (Task 7)
**This README** 📘

<br>

---
<br>

## ▶️ How to Run

1) Install dependencies  
```bash
python3 -m pip install --upgrade pip
python3 -m pip install pandas openpyxl
```
1) Run scripts in order
```bash
python3 most_recent_months.py
python3 master_Dataset.py
python3 date_check.py          # optional
python3 dates_standardiser.py
python3 inconsistencies.py
python3 data_mart.py
```


---
<br>

## 👤 Prepared by **Leen Kharouf**  
Deloitte Data Engineering Case Study – September 2025  
