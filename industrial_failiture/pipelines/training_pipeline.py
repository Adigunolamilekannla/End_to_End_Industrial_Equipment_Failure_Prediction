from industrial_failiture.entity.entity_config import (
    DataInjectionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    TrainPipelineConfig,
)
from industrial_failiture.components.data_ingestion import DataIngestion
from industrial_failiture.components.data_validation import DataValidation
from industrial_failiture.components.data_transformation import DataTransformation
from industrial_failiture.components.model_trainer import ModelTrainer
from industrial_failiture.exception.custom_exception import IndustralFailitureException
from industrial_failiture.logging.logger import logging
from industrial_failiture.cloud.cloud import S3sync
from industrial_failiture.constants import TRAINING_BUCKET_NAME
import sys


class TrainingPipeline:
    def __init__(self):
        try:
            logging.info("Initializing TrainingPipeline configuration...")
            self.train_pipeline_config = TrainPipelineConfig()
            self.s3_sync = S3sync()
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def start_data_ingestion(self):
        try:
            logging.info("Starting data ingestion...")
            data_ingestion_config = DataInjectionConfig(self.train_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully.")
            return data_ingestion_artifacts
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def start_data_validation(self, data_ingestion_artifacts):
        try:
            logging.info("Starting data validation...")
            data_validation_config = DataValidationConfig(self.train_pipeline_config)
            data_validation = DataValidation(
                data_validation_config=data_validation_config,
                data_ingestion_artifacts=data_ingestion_artifacts,
            )
            data_validation_artifacts = data_validation.initiate_data_validation()
            logging.info("Data validation completed successfully.")
            return data_validation_artifacts
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def start_data_transformation(self, data_validation_artifacts):
        try:
            logging.info("Starting data transformation...")
            data_transformation_config = DataTransformationConfig(
                self.train_pipeline_config
            )
            data_transformation = DataTransformation(
                data_validation_artifacts=data_validation_artifacts,
                data_transformation_config=data_transformation_config,
            )
            data_transformation_artifacts = (
                data_transformation.initiate_data_transformation()
            )
            logging.info("Data transformation completed successfully.")
            return data_transformation_artifacts
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def start_model_trainer(self, data_transformation_artifacts):
        try:
            logging.info("Starting model training...")
            model_trainer_config = ModelTrainerConfig(self.train_pipeline_config)
            model_trainer = ModelTrainer(
                data_transformation_artifacts=data_transformation_artifacts,
                model_trainer_config=model_trainer_config,
            )
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info("Model training completed successfully.")
            return model_trainer_artifacts
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def sync_artifacts_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifacts/{self.train_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(
                folder=self.train_pipeline_config.artifact_dir,
                aws_bucket_url=aws_bucket_url,
            )
            logging.info(f"Artifacts synced to S3 bucket: {aws_bucket_url}")
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def run_pipeline(self):
        try:
            logging.info("Pipeline execution started.")
            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(
                data_ingestion_artifacts
            )
            data_transformation_artifacts = self.start_data_transformation(
                data_validation_artifacts
            )
            self.start_model_trainer(data_transformation_artifacts)
            logging.info("Pipeline execution completed successfully.")

            # Optional: sync artifacts after successful run
            self.sync_artifacts_dir_to_s3()
        except Exception as e:
            logging.error("Pipeline execution failed.")
            raise IndustralFailitureException(e, sys)


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()
