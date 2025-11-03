import pandas as pd
from faker import Faker
import random

# --- Configuration ---
NUM_RECORDS = 1000
PERCENT_MATCH = 0.60  # 60% will be perfect matches
PERCENT_ERRORS = 0.20 # 20% will have typos/errors
# The rest (20%) will be completely new records

# --- Helper function to introduce typos ---
def introduce_typo(text):
    """Introduces a random typo into a string."""
    if len(text) < 3:
        return text
    
    pos = random.randint(0, len(text) - 2)
    # Swap two adjacent characters for a simple typo
    chars = list(text)
    chars[pos], chars[pos+1] = chars[pos+1], chars[pos]
    return "".join(chars)

# --- Main generation logic ---
def generate_data():
    """Generates and saves Aadhar and PAN test data CSV files."""
    fake = Faker('en_IN')

    # 1. Generate Base Aadhar Data
    print("Generating base Aadhar data...")
    aadhar_data = []
    for i in range(NUM_RECORDS):
        aadhar_data.append({
            'id': i,
            'name': fake.name(),
            'dob': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            'address': fake.address().replace('\n', ', '),
            'aadhar_number': fake.unique.ssn().replace('-', '')
        })
    aadhar_df = pd.DataFrame(aadhar_data)
    aadhar_df.to_csv('aadhar_data.csv', index=False)
    print("✅ aadhar_data.csv created successfully.")

    # 2. Generate PAN Data based on Aadhar Data
    print("\nGenerating PAN data with variations...")
    pan_data = []
    num_match = int(NUM_RECORDS * PERCENT_MATCH)
    num_errors = int(NUM_RECORDS * PERCENT_ERRORS)
    num_new = NUM_RECORDS - num_match - num_errors

    # Add matching records
    for i in range(num_match):
        record = aadhar_data[i]
        pan_data.append({
            'id': record['id'],
            'name': record['name'],
            'dob': record['dob'],
            'pan_number': fake.unique.bothify(text='?????####?').upper()
        })

    # Add records with errors
    for i in range(num_match, num_match + num_errors):
        record = aadhar_data[i]
        pan_data.append({
            'id': record['id'],
            'name': introduce_typo(record['name']),
            'dob': record['dob'],
            'pan_number': fake.unique.bothify(text='?????####?').upper()
        })

    # Add new, unique records
    for i in range(num_new):
        pan_data.append({
            'id': NUM_RECORDS + i,
            'name': fake.name(),
            'dob': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            'pan_number': fake.unique.bothify(text='?????####?').upper()
        })
    
    pan_df = pd.DataFrame(pan_data)
    pan_df.to_csv('pan_data.csv', index=False)
    print("✅ pan_data.csv created successfully.")

if __name__ == '__main__':
    generate_data()
