from industrial_failiture.logging.logger import logging
from industrial_failiture.exception.custom_exception import IndustralFailitureException
from industrial_failiture.entity.entity_artifacts import DataTranformationArtifacts
from industrial_failiture.entity.entity_config import ModelTrainerConfig
from industrial_failiture import constants
from industrial_failiture.utils.metrics import get_classification_score
from industrial_failiture.utils.main_utils import save_object
import os, sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import mlflow
import mlflow.sklearn
import pandas as pd


class ModelTrainer:
    def __init__(self, data_transformation_artifacts: DataTranformationArtifacts,
                 model_trainer_config: ModelTrainerConfig):
        try:
            logging.info("Initializing ModelTrainer component...")
            self.data_transformation_artifacts = data_transformation_artifacts
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise IndustralFailitureException(e, sys)
        
    def mlflow_tracking(self, model_name, model, train_metrics, test_metrics, register_model=True):
        """Logs model, parameters, and metrics to MLflow"""
        try:
            logging.info(f"Starting MLflow tracking for {model_name}")

            with mlflow.start_run(run_name=model_name):
                # Log best model
                logging.info("Logging model to MLflow...")
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="model",
                    registered_model_name=model_name if register_model else None
                )

                # Log parameters
                if hasattr(model, "get_params"):
                    logging.info("Logging model parameters to MLflow...")
                    mlflow.log_params(model.get_params())

                # Log metrics
                logging.info("Logging training metrics to MLflow...")
                for key, value in train_metrics.items():
                    mlflow.log_metric(f"train_{key}", value)

                logging.info("Logging testing metrics to MLflow...")
                for key, value in test_metrics.items():
                    mlflow.log_metric(f"test_{key}", value)

            logging.info(f"MLflow tracking completed successfully for {model_name}")

        except Exception as e:
            logging.error("Error occurred during MLflow tracking")
            raise IndustralFailitureException(e, sys)

    def train_model(self, train_data_file_path, test_data_file_path):
        try:
            logging.info("Loading training and testing data...")
            train_data = pd.read_csv(train_data_file_path)
            test_data = pd.read_csv(test_data_file_path)
            
            X_train, y_train = train_data.drop("fail", axis=1), train_data["fail"]
            X_test, y_test = test_data.drop("fail", axis=1), test_data["fail"]

            logging.info("Training RandomForest with GridSearchCV...")
            rf = RandomForestClassifier(random_state=42)
            param_grid = constants.PARAM_GRID

            gs = GridSearchCV(rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
            gs.fit(X_train, y_train)

            # Use the best model
            best_model = gs.best_estimator_
            logging.info(f"Best model selected: {best_model}")

            # Predictions
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            # Metrics
            y_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            y_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

            # MLflow logging
            self.mlflow_tracking("RandomForest", best_model, y_train_metric, y_test_metric)

            # Save model
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_dir), exist_ok=True)
            save_object(self.model_trainer_config.trained_model_dir, best_model)
            logging.info(f"Best model saved at {self.model_trainer_config.trained_model_dir}")

        except Exception as e:
            raise IndustralFailitureException(e, sys)
        
    def initiate_model_trainer(self):
        try:
            logging.info("Initiating model training pipeline...")
            self.train_model(
                self.data_transformation_artifacts.training_file_path,
                self.data_transformation_artifacts.testing_file_path
            )
            logging.info("Model training pipeline completed successfully ✅")
        except Exception as e:
            raise IndustralFailitureException(e,sys)
