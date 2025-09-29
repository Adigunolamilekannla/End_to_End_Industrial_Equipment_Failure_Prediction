from industrial_failiture.entity.entity_artifacts import DataIngestionArtifacts
from industrial_failiture  import constants
import os
from datetime import datetime


class TrainPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S") # setting time format we want
        self.pipeline_name = constants.PIPELINE_NAME
        self.artifact_name = constants.ARTIFACTS_NAME
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp:str = timestamp
        self.model_dir:str = os.path.join("final_model","model.pkl")
        self.process_model_dir:str = os.path.join("final_model","process.pkl")




class DataInjectionConfig:
    def __init__(self,training_pipeline_config:TrainPipelineConfig):
        self.data_injection_dir:str = os.path.join(
           training_pipeline_config.artifact_name,constants.DATA_INGECTION_INGESTED_DIR # artifacts/ingested
        )
        
        self.feature_store_file_path:str = os.path.join(
            self.data_injection_dir,constants.DATA_INGECTION_FUTURE_STORAGE_DIR,constants.FILE_NAME # artifacts/ingested/"data_INGECTION"/"data.csv"
        )


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainPipelineConfig):
        self.validate_dir_name:str = os.path.join(training_pipeline_config.artifact_dir,constants.DATA_VALIDATION_DIR)
        self.valid_data_path:str = os.path.join(self.validate_dir_name,constants.VALID_DATA_PATH,constants.VALID_DATA_FILE_NAME)
        self.invalid_data_path:str = os.path.join(self.validate_dir_name,constants.INVALID_DATA_PATH,constants.INVALID_DATA_FILE_NAME)
        self.drift_report_file_path:str = os.path.join(
            self.validate_dir_name,
            constants.DATA_VALIDATION_DRIFT_REPORT_DIR,
            constants.DATA_VALIDATION_DRIFT_REPORT_DIR_FILE_NAME
        )


class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainPipelineConfig):
        self.transformed_data_dir:str = os.path.join(training_pipeline_config.artifact_dir,constants.DATA_TRANSFORMATION_DIR)
        self.transformed_train_data_file_path:str = os.path.join(self.transformed_data_dir,constants.TRAIN_DATA_DIR,constants.TRAINING_FILE_NAME)
        self.transformed_test_data_file_path:str = os.path.join(self.transformed_data_dir,constants.TEST_DATA_DIR,constants.TESTING_FILE_NAME)
        self.data_file_path:str =   os.path.join(
           training_pipeline_config.artifact_name,constants.DATA_INGECTION_INGESTED_DIR,constants.DATA_INGECTION_FUTURE_STORAGE_DIR,constants.FILE_NAME
        )

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainPipelineConfig):
        self.trained_model_dir:str  = os.path.join(training_pipeline_config.artifact_dir,constants.MODEL_TRAINER_DIR,constants.TRAINED_MODEL_FILE_NAME)