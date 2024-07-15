import pandas as pd
from pathlib import Path


# Get the directory of the current script file
project_dir = Path(__file__).resolve().parents[3]
print(project_dir)
#input directory
parent_folder = project_dir /"src/data/interim/central-unit"
print(parent_folder)
# output directory
result_dir = project_dir /"data/processed/central-unit"
result_dir.mkdir(parents=True, exist_ok=True)


df = pd.read_csv("/Users/macbook/Desktop/bill/data/interim/central-unit/bbpcuDaily.csv")
df.columns.values[0]='year'
df.columns.values[1]='date'
df.columns.values[2]='transaction_volume'
df.columns.values[3]='transaction_value'


df.insert(4, 'unit', 'transaction_value in rupees crores, transaction_volume in millions')
df.insert(5, 'note', '')

# Convert date to datetime format
try:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
except ValueError:
    print("Error: Unable to parse dates. Check the date formats in the input CSV.")
    raise

# Format the date column to "dd-mm-yyyy"
df['date'] = df['date'].dt.strftime('%d-%m-%Y')

# Save the melted DataFrame as output.csv in result_dir
output_file = result_dir / "output.csv"
df.to_csv(output_file, index=False,)

print(f"Data saved successfully to {output_file}")
