import os
from dotenv import load_dotenv
"""
Defining Common Constant  for connecting to database 
"""
# Load environment variables
load_dotenv()
PASSWORD = os.getenv("PASSWORD")
POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")

# AWS PostgreSQL credentials
HOST = POSTGRES_DATABASE_URL
PORT = os.getenv("POST")
DATABASE =os.getenv("DATABASE")
USER = os.getenv("USER")


"""
Defining common constant for training pipeline 
"""

TARGET_COLUMNS = "fail"
PIPELINE_NAME:str = "INDUSTRIAL_FAILITURE"
ARTIFACTS_NAME:str = "Artifacts"
FILE_NAME: str = "data.csv"

TRAINING_FILE_NAME = "train.csv"
TESTING_FILE_NAME = "test.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml") 
PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"
TRAINED_MODEL_FILE_NAME:str = "model.pkl"



"""
Data injection related constant start with DATA_INJECTION VAR NAME
"""
DATA_INGECTION_COLLECTION_NAME:str = "IndustralFailiture"
DATA_INGECTION_DATABASE_NAME:str = "industrial_failiture_dataset"
DATA_INGECTION_FUTURE_STORAGE_DIR:str = "data_ingestion"
DATA_INGECTION_INGESTED_DIR:str = "ingested"

