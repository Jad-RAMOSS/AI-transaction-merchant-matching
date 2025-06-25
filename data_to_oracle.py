import os
from dotenv import load_dotenv
import oracledb
import pandas as pd
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def export_to_oracle(df):
    try:
        # Oracle connection details loaded from environment variables
        username = os.getenv("ORACLE_USERNAME")
        password = os.getenv("ORACLE_PASSWORD")
        host = os.getenv("ORACLE_HOST")
        port = int(os.getenv("ORACLE_PORT"))
        service_name = os.getenv("ORACLE_SERVICE")

        if not all([username, password, host, service_name]):
            raise ValueError("Database credentials are not fully set in environment variables.")
        
        # Create connection string
        dsn = f"{host}:{port}/{service_name}"
        
        # Connect to Oracle
        with oracledb.connect(user=username, password=password, dsn=dsn) as connection:
            cursor = connection.cursor()
            
            # Prepare data for insertion (ensure correct data types)
            data_to_insert = []
            for _, row in df.iterrows():
                # Convert the Date column to a Python datetime (or None)
                dt_value = pd.to_datetime(row['Date'], errors='coerce')
                if pd.isna(dt_value):
                    dt_value = None
                else:
                    dt_value = dt_value.to_pydatetime()

                data_to_insert.append(tuple([
                    dt_value,
                    float(row['Amount']) if pd.notna(row['Amount']) else None,
                    str(row['Description']) if pd.notna(row['Description']) else None,
                    str(row['Reference_Number']) if pd.notna(row.get('Reference_Number')) else None,
                    str(row['Rep']) if pd.notna(row.get('Rep')) else None
                ]))

            # SQL statement using fixed column names (matching the table)
            sql = (
                'INSERT INTO REPORT.BANK_REP_PREDICTION '\
                '("DATE", "AMOUNT", "DESCRIPTION", "REFERENCE_NUMBER", "REP") '\
                'VALUES (:1, :2, :3, :4, :5)'
            )

            # Execute batch insert
            cursor.executemany(sql, data_to_insert, batcherrors=True)

            
            # Check for any batch errors
            for error in cursor.getbatcherrors():
                print(f"Error inserting row {error.offset}: {error.message}")
            
            connection.commit()
            print(f"Successfully inserted {len(data_to_insert)} rows into Oracle database.")
            
    except Exception as e:
        print(f"Error exporting to Oracle: {str(e)}")
        raise  # Re-raise the exception to see full traceback
