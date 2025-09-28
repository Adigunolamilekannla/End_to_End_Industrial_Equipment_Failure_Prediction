from industrial_failiture.entity.entity_config import DataInjectionConfig,DataValidationConfig,DataTransformationConfig
from industrial_failiture.components.data_ingestion import DataIngestion
from industrial_failiture.components.data_validation import DataValidation
from industrial_failiture.entity.entity_config import TrainPipelineConfig
from industrial_failiture.components.data_transformation import DataTransformation



train_pipeline_config = TrainPipelineConfig()
data_ingestion_config = DataInjectionConfig(training_pipeline_config=train_pipeline_config)
data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()



data_validation_config = DataValidationConfig(training_pipeline_config=train_pipeline_config)
data_validation = DataValidation(data_validation_config=data_validation_config,
                                 data_ingestion_artifacts=data_ingestion_artifacts)
data_validation_artifacts = data_validation.initiate_data_validation()



data_transformation_config = DataTransformationConfig(train_pipeline_config)
data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                         data_validation_artifacts=data_validation_artifacts)
data_transformation_artifacts = data_transformation.initiate_data_transformation()


