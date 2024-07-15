import pandas as pd
from pathlib import Path


# Get the directory of the current script file
project_dir = Path(__file__).resolve().parents[4]
print(project_dir)
# #input directory
parent_folder = project_dir /"data/interim/billers/"
print(parent_folder)
# # output directory
result_dir = project_dir /"data/processed/billers/live_billers"
result_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("/Users/macbook/Desktop/bill/data/interim/billers/liveBillers.csv")

df.columns.values[0]='biller_name'
df.columns.values[1]='state'
df.columns.values[2]='billers'

# Save the melted DataFrame as output.csv in result_dir
result_dir = Path("/Users/macbook/Desktop/bill/data/processed/billers/live_billers")  
output_file = result_dir / "output.csv"
df.to_csv(output_file, index=False,)

print(f"Data saved successfully to {output_file}")