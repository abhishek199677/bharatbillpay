import pandas as pd
from pathlib import Path

project_dir = Path(__file__).resolve().parents[4]

# Input and output directories
input_dir = project_dir / "data/interim/billers"
output_dir = project_dir / "data/processed/billers/categories"
output_dir.mkdir(parents=True, exist_ok=True)

input_file = input_dir / "categories.csv"
df = pd.read_csv(input_file)

df.columns = df.columns.str.strip()

# Drop columns 'volume(%)' and 'value(%)'
columns_to_drop = ['Volume(%)', 'Value(%)'] 
df.drop(columns=columns_to_drop, axis=1, inplace=True)


df.rename(columns={
    'Category Name': 'biller_category',
    'Volume(Mn)': 'volume',
    'Value(Cr)': 'value'
}, inplace=True)

# Add empty columns 'unit' and 'note'
df['unit'] = 'volume in millions, value in rupee crores'
df['note'] = ''

# Convert column names to lowercase
df.columns = df.columns.str.lower()

output_file = output_dir / "output.csv"
df.to_csv(output_file, index=False)

print(f"Data saved successfully to {output_file}")
