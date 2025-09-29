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



"""
Defining common constant for training pipeline 
"""

TARGET_COLUMNS = "fail"
PIPELINE_NAME:str = "INDUSTRIAL_FAILITURE"
ARTIFACTS_NAME:str = "Artifacts"
FILE_NAME: str = "data.csv"

TRAINING_FILE_NAME = "train.csv"
TESTING_FILE_NAME = "test.csv"
SCHEMA_FILE_PATH =  "schema/schema.yaml"




"""
Data injection related constant start with DATA_INJECTION VAR NAME
"""
DATA_INGECTION_COLLECTION_NAME:str = "IndustralFailiture"
DATA_INGECTION_DATABASE_NAME:str = "industrial_failiture_dataset"
DATA_INGECTION_FUTURE_STORAGE_DIR:str = "data_ingestion"
DATA_INGECTION_INGESTED_DIR:str = "ingested"



"""
Defining common constant for data validation
"""
DATA_VALIDATION_DIR = "validate"
VALID_DATA_PATH = "valid"
VALID_DATA_FILE_NAME = "data.csv"
INVALID_DATA_PATH = "invalid"
INVALID_DATA_FILE_NAME = "data.csv"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_DIR_FILE_NAME:str = "report.yaml"



"""
Defining common constant for data trainsfformation
"""

DATA_TRANSFORMATION_DIR:str = "transformed_data"
TRAIN_DATA_DIR:str = "training_data" 
TEST_DATA_DIR:str = "testing_data" 


"""
Defining common constant for model training
"""

MODEL_TRAINER_DIR:str = "trained_model"
TRAINED_MODEL_FILE_NAME:str = "model.pkl"


PARAM_GRID = {
    "n_estimators": [100, 200, 300, 500],         # number of trees
    "max_depth": [None, 10, 20, 30, 50],          # depth of trees
    "min_samples_split": [2, 5, 10],              # minimum samples to split a node
    "min_samples_leaf": [1, 2, 4],                # minimum samples in a leaf node
    "max_features": ["auto", "sqrt", "log2"],     # number of features considered at each split
    "bootstrap": [True, False]                    # whether bootstrap samples are used
}


