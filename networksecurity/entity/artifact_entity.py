from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str
    
    
def initiate_data_ingestion(self):
    try:
        df = self.export_collection_as_dataframe()
        df = self.export_data_to_feature_store(df)
        train_file_path, test_file_path = self.split_data_as_train_test(df)
        artifact = DataIngestionArtifact(
            train_file_path=train_file_path,
            test_file_path=test_file_path
        )
        return artifact
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    
from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    artifact = data_ingestion.initiate_data_ingestion()
    print(artifact)