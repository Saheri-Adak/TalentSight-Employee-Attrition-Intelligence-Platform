# Import necessary libraries
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create connection
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Load datasets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(BASE_DIR, '..', 'data', 'processed')

# Load and push each table
tables = {
    'employee_master': 'employee_master_clustered.csv',
    'bls_monthly': 'bls_monthly_macro.csv',
    'bls_eci': 'bls_quarterly_eci.csv',
    'payroll': 'synthetic_Payroll_24_Months_cleaned.csv'
}

for table_name, filename in tables.items():
    df = pd.read_csv(os.path.join(data_dir, filename))
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Loaded {table_name}: {df.shape[0]} rows")

print("All tables loaded successfully")