import os
import pandas as pd

input_folder = 'data'
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
dfs = []

for file in csv_files:
    file_path = os.path.join(input_folder, file)
    df = pd.read_csv(file_path)
    dfs.append(df)

merged_df = pd.concat(dfs, ignore_index=True, sort=False)
merged_df.to_csv('results.csv', index=False, encoding='utf-8-sig')

print(f"Đã gộp {len(csv_files)} file CSV")
