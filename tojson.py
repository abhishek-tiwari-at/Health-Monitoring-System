import pandas as pd
import json

# Input and output file paths
csv_file = "datasets/cardio_train.csv"
json_output_file = "datasets/cardio_train.json"

# Read the semicolon-separated CSV file
try:
    df = pd.read_csv(csv_file, sep=';', quotechar="'")
except FileNotFoundError:
    print(f"Error: The file {csv_file} was not found. Please ensure it exists in the working directory.")
    exit(1)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)

# Expected columns
expected_columns = [
    'id', 'age', 'gender', 'height', 'weight',
    'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active'
]

# Validate columns
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    print(f"Error: The following required columns are missing: {missing_columns}")
    exit(1)

# Ensure correct data types
try:
    df = df.astype({
        "id": int,
        "age": int,
        "gender": int,
        "height": float,
        "weight": float,
        "ap_hi": int,
        "ap_lo": int,
        "cholesterol": int,
        "gluc": int,
        "smoke": int,
        "alco": int,
        "active": int
    })
except Exception as e:
    print(f"Error during type conversion: {e}")
    exit(1)

# Convert to JSON
records = df[expected_columns].to_dict(orient="records")

# Write each record to JSON file (newline-delimited JSON)
try:
    with open(json_output_file, "w", encoding='utf-8') as f:
        for record in records:
            json.dump(record, f)
            f.write("\n")
    print(f"✅ Successfully converted {csv_file} to {json_output_file}. {len(records)} records written.")
except Exception as e:
    print(f"Error writing JSON file: {e}")
    exit(1)

# Show sample records
print("\nSample JSON records (first 3):")
for i, record in enumerate(records[:3]):
    print(f"Record {i + 1}:\n{json.dumps(record, indent=2)}")
