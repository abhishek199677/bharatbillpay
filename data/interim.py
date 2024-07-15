import json
import pandas as pd
from pathlib import Path

# Directory where JSON files are stored
json_dir = Path("data/raw")

processed_dir = Path("data/interim")
processed_dir.mkdir(parents=True, exist_ok=True)

# Get all JSON files in the directory and its subdirectories
json_files = json_dir.glob("**/*.json")

for json_file in json_files:
    # Load JSON data
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    
    # Convert JSON to DataFrame
    df = pd.DataFrame(json_data)

    # Extract folder name from JSON file path
    folder_name = json_file.parent.name  # Get the name of the parent directory
    
    # Extract file name without extension
    filename_without_extension = json_file.stem
    
    # Create CSV file path
    csv_file = processed_dir / folder_name / (filename_without_extension + ".csv")
    csv_file.parent.mkdir(parents=True, exist_ok=True)  # Create parent directories if they don't exist
    
    # Save DataFrame to CSV
    df.to_csv(csv_file, index=False)
    
    print(f"Converted {json_file} to {csv_file}")

print("Conversion complete.")
