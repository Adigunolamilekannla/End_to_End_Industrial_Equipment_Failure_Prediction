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


 


