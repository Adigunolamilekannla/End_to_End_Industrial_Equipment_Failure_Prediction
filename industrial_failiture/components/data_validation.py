from industrial_failiture.logging.logger import logging
from industrial_failiture.exception.custom_exception import IndustralFailitureException
from industrial_failiture.utils.main_utils import read_yaml, write_yaml
from industrial_failiture.entity.entity_artifacts import (
    DataValidationArtifacts,
    DataIngestionArtifacts,
)
from industrial_failiture.entity.entity_config import DataValidationConfig
from industrial_failiture import constants
import os, sys
from scipy.stats import ks_2samp
import pandas as pd


class DataValidation:
    def __init__(
        self,
        data_validation_config: DataValidationConfig,
        data_ingestion_artifacts: DataIngestionArtifacts,
    ):
        try:
            logging.info("Initializing DataValidation component...")
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml(constants.SCHEMA_FILE_PATH)
            logging.info("Schema configuration loaded successfully.")
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """Read CSV file into pandas DataFrame"""
        try:
            logging.info(f"Reading data from {file_path}")
            df = pd.read_csv(file_path)
            logging.info(f"Data shape after loading: {df.shape}")
            return df
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """Check if dataframe has expected number of columns"""
        try:
            required_columns = len(self.schema_config["COLUMNS"].keys())
            print(required_columns)
            print(len(dataframe.columns))
            logging.info(
                f"Validating number of columns. Expected: {required_columns}, Found: {len(dataframe.columns)}"
            )
            if len(dataframe.columns) == required_columns:
                logging.info("✅ Number of columns validation passed.")
                return True
            else:
                logging.warning("❌ Number of columns validation failed.")
                return False
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def detect_dataset_drift(
        self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.6
    ) -> bool:
        """Check dataset drift between base and current dataset"""
        try:
            logging.info("Starting dataset drift detection...")
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                ks_test = ks_2samp(d1, d2)
                p_value = ks_test.pvalue

                drift_detected = p_value < threshold
                if drift_detected:
                    status = False
                    logging.warning(
                        f"Drift detected in column '{column}' with p-value={p_value:.5f}"
                    )
                else:
                    logging.info(
                        f"No drift in column '{column}' (p-value={p_value:.5f})"
                    )

                report[column] = {
                    "p_value": float(p_value),
                    "drift_detected": drift_detected,
                }

            # Save drift report
            drift_report_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_path), exist_ok=True)
            write_yaml(drift_report_path, report, True)
            logging.info(f"Drift report saved at: {drift_report_path}")

            return status
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifacts:
        """Run the data validation process"""
        try:
            logging.info("===== Starting Data Validation Process =====")
            data_file_path = self.data_ingestion_artifacts.data_file_path

            # 1. Load Data
            data = DataValidation.read_data(data_file_path)

            # 2. Validate column count
            data_status = self.validate_number_of_columns(data)
            if not data_status:
                raise IndustralFailitureException(
                    "Training dataframe has column mismatch", sys
                )

            # 3. Drift detection (for now comparing dataset with itself)
            drift_status = self.detect_dataset_drift(data, data)

            # 4. Save validated data
            os.makedirs(
                os.path.dirname(self.data_validation_config.valid_data_path),
                exist_ok=True,
            )
            data.to_csv(
                self.data_validation_config.valid_data_path, index=False, header=True
            )
            logging.info(
                f"Validated data saved at: {self.data_validation_config.valid_data_path}"
            )

            # 5. Create artifacts
            data_validation_artifacts = DataValidationArtifacts(
                validation_status=data_status,
                valid_data_file_path=self.data_validation_config.valid_data_path,
                invalid_data_file_path=self.data_validation_config.invalid_data_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
                drift_status=drift_status,
            )

            logging.info("✅ Data Validation completed successfully.")
            return data_validation_artifacts

        except Exception as e:
            raise IndustralFailitureException(e, sys)
