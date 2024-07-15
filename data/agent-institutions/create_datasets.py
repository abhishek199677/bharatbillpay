import pandas as pd
from pathlib import Path

# Get the directory of the current script file
project_dir = Path(__file__).resolve().parents[3]

# Define input and output directories
input_dir = project_dir / "data/interim/agent-institutions/"
result_dir = project_dir / "data/processed/agent-instituitions/"
result_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("/Users/macbook/Desktop/bill/data/interim/agent-institutions/agentInstitutionsTop20.csv")

# Rename columns
df.columns = ['year', 'month', 'agent_institution_name', 'brand_name', 'channel', 'volume', 'value']

# Insert 'unit' and 'note' columns
df.insert(7, 'unit', 'value in rupees crore, volume in lakhs')
df.insert(8, 'note', '')

# Load standard names mapping from CSV file
standard_file = project_dir / "data/external/agent_institution_standardisation.csv"
standard_names = pd.read_csv(standard_file)

# Create mappings
mapping1 = dict(zip(standard_names["agent_instution_name"], standard_names["standard_agent_instution_name"]))
mapping2 = dict(zip(standard_names["brand_name"], standard_names["standard_brand_name"]))

# Apply mappings to DataFrame
df["agent_institution_name"] = df["agent_institution_name"].map(mapping1)
df["brand_name"] = df["brand_name"].map(mapping2)

# Save the modified DataFrame to CSV in the result_dir
output_file = result_dir / "output.csv"
df.to_csv(output_file, index=False)