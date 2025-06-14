import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import  numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifacts',"train.csv")
    test_data_path:str=os.path.join('artifacts',"test.csv")
    raw_data_path:str=os.path.join('artifacts',"raw.csv")


class DataIngestion:
    def __init__(self):
        # storing all path in one variable
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered the data ingestion method or component.')
        try:
            #  Reading the dataset from the csv file 
            df=pd.read_csv('notebook\\data\\stud.csv')
            logging.info('Read the dataset as dataframe.')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # store data to raw data file
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info('Train test split initiated')
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            # store training data to training file
            logging.info('Store training data')
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            # store test data to testing data
            logging.info('Store testing data')
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info('Ingestion of the data is completed.')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            ce=CustomException(e,sys)
            logging.error(ce)

            

if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()   
    data_transformation=DataTransformation()
    train_data,test_data,_=data_transformation.initiate_data_transformation(train_data,test_data)

    model_trainer=ModelTrainer()
    score=model_trainer.initiate_model_trainer(train_data,test_data)
    print(score)




