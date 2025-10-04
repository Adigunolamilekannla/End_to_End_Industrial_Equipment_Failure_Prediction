from flask import Flask, request, render_template
import pandas as pd
from industrial_failiture.utils.main_utils import load_object
from industrial_failiture.pipelines.training_pipeline import TrainingPipeline
from industrial_failiture.entity.entity_config import (
    ModelTrainerConfig,
    TrainPipelineConfig,
)
from industrial_failiture.logging.logger import logging


# --- Initialize configs ---
train_pipeline_config = TrainPipelineConfig()
model_training_config = ModelTrainerConfig(
    training_pipeline_config=train_pipeline_config
)
trained_model_path = model_training_config.trained_model_dir

# --- Load model at startup ---

rf_model = load_object(trained_model_path)

app = Flask(__name__)


# --- Homepage (Prediction Form) ---
@app.route("/")
def home():
    return render_template("index.html")


# --- Handle Prediction from Form ---
@app.route("/predict_form", methods=["POST"])
def predict_form():
    try:
        input_data = {
            "footfall": float(request.form["footfall"]),
            "tempMode": float(request.form["tempMode"]),
            "AQ": float(request.form["AQ"]),
            "USS": float(request.form["USS"]),
            "CS": float(request.form["CS"]),
            "VOC": float(request.form["VOC"]),
            "RP": float(request.form["RP"]),
            "IP": float(request.form["IP"]),
            "Temperature": float(request.form["Temperature"]),
        }

        global rf_model
        # Convert to DataFrame
        features = pd.DataFrame([input_data])

        # 🔑 Normalize column names (lowercase to match training)
        features.columns = [col.lower() for col in features.columns]

        prediction = rf_model.predict(features)

        return render_template(
            "index.html", input_data=input_data, prediction=int(prediction)
        )
    except Exception as e:
        return render_template("index.html", error=str(e))


# --- Training Page ---
@app.route("/train_model")
def train_page():
    try:
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()

        # reload latest trained model
        global rf_model
        rf_model = load_object(trained_model_path)

        return render_template("train.html", accuracy="Model retrained successfully ✅")
    except Exception as e:
        logging.error("Training error: %s", e)
        return render_template("train.html", error=str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
