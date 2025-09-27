from industrial_failiture.entity.entity_artifacts import DataIngestionArtifacts
from industrial_failiture.entity.entity_config import DataInjectionConfig
from industrial_failiture.logging.logger import logging
from industrial_failiture.exception.custom_exception import IndustralFailitureException
import os, sys
import pandas as pd
import psycopg2
from industrial_failiture import constants
import industrial_failiture.constants as i


# AWS PostgreSQL credentials (from constants)
host = constants.POSTGRES_DATABASE_URL
port = constants.PORT
database = constants.DATABASE
password = constants.PASSWORD
user = "postgres"


class DataIngestion:
    def __init__(self, data_ingestion_config: DataInjectionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def load_data_from_postgres_db(self) -> pd.DataFrame:
        """Fetch data from PostgreSQL and return as DataFrame"""
        try:
            logging.info("Connecting to PostgreSQL...")
            with psycopg2.connect(
                host=host,
                dbname=database,
                user=user,
                password=password,
                port=port,
                sslmode="require"  # ensures SSL connection
            ) as conn:
                query = "SELECT * FROM industrial_failure;"
                df = pd.read_sql(query, conn)

            logging.info(f"✅ Data loaded successfully. Shape: {df.shape}")
            return df

        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def data_feature_storage(self, df: pd.DataFrame) -> pd.DataFrame:
        """Save DataFrame to CSV feature store"""
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False)

            logging.info(f"📂 Data saved to feature store at {feature_store_file_path}")
            return df

        except Exception as e:
            raise IndustralFailitureException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        """Orchestrates data ingestion process"""
        try:
            df = self.load_data_from_postgres_db()
            self.data_feature_storage(df)

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            data_ingestion_artifacts = DataIngestionArtifacts(
                data_file_path=feature_store_file_path
            )

            logging.info("🎯 Data Ingestion completed successfully")
            return data_ingestion_artifacts

        except Exception as e:
            raise IndustralFailitureException(e, sys)
