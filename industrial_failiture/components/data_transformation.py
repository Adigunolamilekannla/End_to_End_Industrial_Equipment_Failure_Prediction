from industrial_failiture.entity.entity_artifacts import (
    DataTranformationArtifacts,
    DataValidationArtifacts,
)
from industrial_failiture.entity.entity_config import DataTransformationConfig
import os, sys
from industrial_failiture.logging.logger import logging
from industrial_failiture.exception.custom_exception import IndustralFailitureException
import pandas as pd
from sklearn.model_selection import train_test_split


class DataTransformation:
    def __init__(
        self,
        data_validation_artifacts: DataValidationArtifacts,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            logging.info("✅ Initializing DataTransformation component...")
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def load_data(self, file_path) -> pd.DataFrame:
        try:
            logging.info(f"📂 Loading data from: {file_path}")
            if (
                self.data_validation_artifacts.drift_status
                and self.data_validation_artifacts.validation_status
            ):
                df = pd.read_csv(file_path)
                logging.info(f"✅ Data loaded successfully. Shape: {df.shape}")
                return df
            else:
                raise IndustralFailitureException(
                    "Data validation or drift check failed", sys
                )
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def transform_data(self, df: pd.DataFrame):
        try:
            logging.info("🔄 Splitting dataset into train and test...")
            train, test = train_test_split(df, test_size=0.2, random_state=101)

            # Ensure directories exist
            os.makedirs(
                os.path.dirname(
                    self.data_transformation_config.transformed_train_data_file_path
                ),
                exist_ok=True,
            )
            os.makedirs(
                os.path.dirname(
                    self.data_transformation_config.transformed_test_data_file_path
                ),
                exist_ok=True,
            )

            # Save CSVs
            train.to_csv(
                self.data_transformation_config.transformed_train_data_file_path,
                index=False,
            )
            test.to_csv(
                self.data_transformation_config.transformed_test_data_file_path,
                index=False,
            )

            logging.info(
                f"✅ Train data saved at {self.data_transformation_config.transformed_train_data_file_path} with shape {train.shape}"
            )
            logging.info(
                f"✅ Test data saved at {self.data_transformation_config.transformed_test_data_file_path} with shape {test.shape}"
            )

        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def initiate_data_transformation(self):
        try:
            logging.info("🚀 Starting Data Transformation process...")
            df = self.load_data(self.data_transformation_config.data_file_path)
            self.transform_data(df)

            data_transformation_artifacts = DataTranformationArtifacts(
                training_file_path=self.data_transformation_config.transformed_train_data_file_path,
                testing_file_path=self.data_transformation_config.transformed_test_data_file_path,
            )

            logging.info("🎯 Data Transformation completed successfully.")
            return data_transformation_artifacts

        except Exception as e:
            raise IndustralFailitureException(e, sys)
