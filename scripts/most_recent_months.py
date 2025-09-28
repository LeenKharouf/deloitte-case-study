import os
import glob
import shutil
from collections import defaultdict

# --- Paths ---
source_folder = "Case_Study_Data_For_Share"     # folder with all CSVs
dest_folder = "most_recent_months"      # new folder for latest versions
os.makedirs(dest_folder, exist_ok=True)

# --- Group files by month (YYYYMM) ---
files = glob.glob(os.path.join(source_folder, "*.csv"))
files_by_month = defaultdict(list)

for f in files:
    base = os.path.basename(f)
    month_key = base[:6]  # first 6 chars = YYYYMM
    files_by_month[month_key].append(f)

# --- Pick the most recent file in each month ---
for month, file_list in files_by_month.items():
    # sort by filename (timestamp part makes later ones "greater")
    latest_file = sorted(file_list)[-1]
    
    # copy to destination folder
    shutil.copy(latest_file, dest_folder)
    print(f"✅ {month}: {os.path.basename(latest_file)} copied.")

print("\n📂 All most recent monthly files are now in:", dest_folder)
