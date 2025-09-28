from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    data_file_path:str


@dataclass
class DataValidationArtifacts:
    validation_status:bool
    valid_data_file_path:str
    invalid_data_file_path:str
    drift_report_file_path:str
    drift_status: bool