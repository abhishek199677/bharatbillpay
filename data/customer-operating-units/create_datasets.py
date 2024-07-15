import pandas as pd
from pathlib import Path

# Get the directory of the current script file
project_dir = Path(__file__).resolve().parents[3]

# Define input and output directories
input_dir = project_dir / "data/interim/customer-operating-units/"
result_dir = project_dir / "data/processed/customer-operating-units/"
result_dir.mkdir(parents=True, exist_ok=True)

transactions_dir = result_dir / "transactions"
transactions_dir.mkdir(parents=True, exist_ok=True)

uptime_downtime_dir = result_dir / "uptime-downtime"
uptime_downtime_dir.mkdir(parents=True, exist_ok=True)

complaints_dir = result_dir / "complaint"
complaints_dir.mkdir(parents=True, exist_ok=True)

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

# Load the CSV file
file_path = "/Users/macbook/Desktop/bill/data/interim/customer-operating-units/couTop30.csv"
df = pd.read_csv(file_path)

df.columns = df.columns.str.lower()

# Define fixed column indices
fixed_column_indices = [0, 1, 2]  # 'year', 'month', 'cou name'

# Dataset 1: Index 0 to 6 (Year to technical_decline)
df1_columns = fixed_column_indices + list(range(3, 9))  # 0, 1, 2, 3 to 6
df1 = df.iloc[:, df1_columns].drop_duplicates().copy()  # Use .copy() to create a copy
df1.columns = ['year', 'month', 'customer_operating_units', 'volume', 'value', 'approval', 'technical_decline', 'unit', 'note']

df1['unit'] = 'volume in lakhs, value in rupees crore, approval and technical_decline in percentage'
df1['note'] = ''

df1['approval'] = df1['approval'].str.replace('%', '')
df1['technical_decline'] = df1['technical_decline'].str.replace('%', '')

# Dataset 2: Index 0, 1, 7 to 10 (Year, Month, OU ID to Up Time)
df2_columns = fixed_column_indices + [7, 8, 9, 10]
df2 = df.iloc[:, df2_columns].copy()  # Use .copy() to create a copy
df2.columns = ['year', 'month', 'customer_operating_units', 'ou_id', 'down_time_count', 'down_time', 'up_time']

df2['up_time'] = df2['up_time'].str.replace('%', '').copy()  # Use .copy() to modify
df2['down_time'] = df2['down_time'].apply(convert_to_minutes).copy()  # Use .copy() to modify

df2['unit'] = 'down_time in minutes, uptime in percentage, down_time_count in absolute number'
df2['note'] = ''

# Dataset 3: Index 0, 1, -2 to -1 (Year, Month, last two columns)
df3_columns = fixed_column_indices + [-2, -1]
df3 = df.iloc[:, df3_columns].copy()  # Use .copy() to create a copy
df3.columns = ['year', 'month', 'customer_operating_units', 'Resolved_within_0-5_days (%)', 'Resolved_within_5+_days (%)']

df3 = pd.melt(df3, id_vars=['year', 'month', 'customer_operating_units'],
              var_name='type', value_name='percentage')

df3.columns = ['year', 'month', 'customer_operating_units', 'category', 'value']

df3['unit'] = 'value in percentage'
df3['note'] = ''

df3['value'] = df3['value'].str.replace('%', '')
df3.dropna(subset=['value'], inplace=True)

# Remove rows where value is 'NIL'
df3 = df3[df3['value'] != 'NIL']

standard_files = [
    project_dir / "data/external/standard_output_complaints.xlsx",
    project_dir / "data/external/standardisations_transactions.xlsx",
    project_dir / "data/external/standard_output_uptime_downtime.xlsx",
]

# Initialize an empty DataFrame to store mappings
standard_names = pd.DataFrame()

for file_path in standard_files:
    df_temp = pd.read_excel(file_path)
    standard_names = pd.concat([standard_names, df_temp], ignore_index=True)

# Create mappings
mapping1 = dict(zip(standard_names["customer_operating_units"], standard_names["standard"]))
mapping2 = dict(zip(standard_names["customer_operating_units"], standard_names["standard"]))
mapping3 = dict(zip(standard_names["customer_operating_units"], standard_names["standard"]))

df1.loc[:, "customer_operating_units"] = df1["customer_operating_units"].map(mapping1)
df2.loc[:, "customer_operating_units"] = df2["customer_operating_units"].map(mapping2)
df3.loc[:, "customer_operating_units"] = df3["customer_operating_units"].map(mapping3)

# Save the datasets to CSV files in the respective directories
df1.to_csv(transactions_dir / "output.csv", index=False)
df2.to_csv(uptime_downtime_dir / "output.csv", index=False)
df3.to_csv(complaints_dir / "output.csv", index=False)

print("Datasets saved successfully.")
