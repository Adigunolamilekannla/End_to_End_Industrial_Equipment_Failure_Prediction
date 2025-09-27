import os, sys
import psycopg2
from industrial_failiture.exception.custom_exception import IndustralFailitureException
from industrial_failiture import constants



# AWS PostgreSQL credentials
host = constants.POSTGRES_DATABASE_URL
port = constants.PORT
database = constants.DATABASE
user = constants.USER

try:
    # Connect to AWS PostgreSQL
    conn = psycopg2.connect(
        host=host,
        dbname=database,
        user=user,
        password=constants.PASSWORD,
        port=port
    )
    cur = conn.cursor()

    # Create table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS industrial_failure (
        footfall       INTEGER NOT NULL,
        tempMode       INTEGER NOT NULL,
        AQ             INTEGER NOT NULL,
        USS            INTEGER NOT NULL,
        CS             INTEGER NOT NULL,
        VOC            INTEGER NOT NULL,
        RP             INTEGER NOT NULL,
        IP             INTEGER NOT NULL,
        Temperature    INTEGER NOT NULL,
        fail           INTEGER NOT NULL
    );
    """
    cur.execute(create_table_query)
    print("✅ Table created successfully (if not already).")

    # Load CSV into table
    with open("IF_DATA/data.csv", "r") as f:
        next(f)  # skip header to avoid duplicate column names
        cur.copy_from(f, "industrial_failure", sep=",")
    print("✅ Data copied successfully from CSV to industrial_failure table.")

    # Commit changes and close
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Connection closed.")

except Exception as e:
    raise IndustralFailitureException(e, sys)
