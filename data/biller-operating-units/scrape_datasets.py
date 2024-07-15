import pandas as pd
from pathlib import Path

# Function to convert HH:MM format to minutes
def convert_to_minutes(hhmm):
    if pd.isna(hhmm):
        return None
    try:
        hours, minutes = map(int, hhmm.split(':'))
        total_minutes = hours * 60 + minutes
        return total_minutes
    except ValueError:
        return None 

project_dir = Path(__file__).resolve().parents[3]

# Define input and output directories
input_dir = project_dir / "data/interim/biller-operating-units/"
result_dir = project_dir / "data/processed/biller-operating-units/"

result_dir_transactions = result_dir / "transactions"
result_dir_transactions.mkdir(parents=True, exist_ok=True)

result_dir_uptime_downtime = result_dir / "uptime_downtime"
result_dir_uptime_downtime.mkdir(parents=True, exist_ok=True)

# Load data from CSV file
df = pd.read_csv(input_dir / 'bouTop20.csv')

# Select columns for the first dataset (Year to BD)
df1 = df.loc[:, 'Year':'BD'].copy()
df1.rename(columns={'BOU Name': 'biller_operating_unit'}, inplace=True)
df1['unit'] = 'value in rupees crore, volume in lakhs, approval in percentage'
df1['note'] = ''

df1['Approval'] = pd.to_numeric(df1['Approval'].str.replace('%', ''), errors='coerce')
df1['TD'] = pd.to_numeric(df1['TD'].str.replace('%', ''), errors='coerce')
df1['BD'] = pd.to_numeric(df1['BD'].str.replace('%', ''), errors='coerce')

df1.rename(columns={'TD': 'technical_decline'}, inplace=True)

df1.columns = df1.columns.str.lower()

# Load standard names mapping from Excel file
standard_file = project_dir / "data/external/biller-operating-units_standard_transactions.xlsx"
standard_names = pd.read_excel(standard_file)

mapping1 = dict(zip(standard_names["biller_operating_unit"], standard_names["standard"]))
df1["biller_operating_unit"] = df1["biller_operating_unit"].map(mapping1)

df2 = df[['Year', 'Month', 'BOU Name', 'Downtime Count', 'Downtime', 'Uptime']].copy()  # Create a copy of the slice
df2.rename(columns={'BOU Name': 'biller_operating_unit'}, inplace=True)

# Remove percentage sign from 'Uptime' column using .loc
df2.loc[:, 'Uptime'] = pd.to_numeric(df2['Uptime'].str.replace('%', ''), errors='coerce')

# Apply the conversion function to the Downtime column in df2 using .loc
df2.loc[:, 'Downtime'] = df2['Downtime'].apply(convert_to_minutes)
df2.rename(columns={'Downtime Count': 'downtime_count'}, inplace=True)

df2.loc[:, 'unit'] = 'downtime in minutes, uptime in percentage, downtime_count in absolute number'
df2.loc[:, 'note'] = ''
df2.columns = df2.columns.str.lower()


# Save the datasets to CSV files in the respective directories
df1.to_csv(result_dir_transactions / "output.csv", index=False)
df2.to_csv(result_dir_uptime_downtime / "output.csv", index=False)

print("Datasets saved successfully.")
