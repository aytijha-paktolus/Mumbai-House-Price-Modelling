import os
import pandas as pd

folder_path = "output_files"
expected_count = 301  # for 10 pages
mismatch_files = []
total_rows = 0

for file in os.listdir(folder_path):
    if file.endswith('.xls') or file.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_excel(file_path)
            row_count = len(df)
            total_rows += row_count
            print(f"{file} has {row_count} rows")
            if row_count + 1 != expected_count:
                mismatch_files.append(file)
        except Exception as e:
            print(f"Error reading {file}: {e}")

print(f"Total rows across all files (excluding headers): {total_rows}")

if mismatch_files:
    print("Files with mismatched row count:")
    for file in mismatch_files:
        print(file)
else:
    print("All files have the expected row count.")