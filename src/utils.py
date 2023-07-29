import os
import sys 

import boto3
import dill
import numpy as np
import pandas as pd 

from pymongo import MongoClient

from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split 

from src.exception import CustomException
from src.logger import logging 

def export_collection_as_dataframe(collection_name, db_name) : #collecting the data as dataframe
    try :
        #uniform resource identifier
        uri = "mongodb+srv://obaidabubakar377:obaidabubakar377@cluster0.c8jeyzg.mongodb.net/?retryWrites=true&w=majority"
        
        mongo_client = MongoClient(uri) # create a new client and connect to the server 
        
        collection = mongo_client[db_name][collection_name]

        df = pd.DataFrame(list(collection.find()))

        if "_id" in df.columns.to_list():
            df = df.drop(columns=["_id"],axis=1)

        df.replace({"na" : np.nan}, inplace= True)

        return df 
    
    except Exception as e :
        logging.info("Error Occured in export_colection_as_data_frame method ")
        raise CustomException(e,sys)
    
def save_object(file_path,obj): # converting and saving our model as a pickle file 
    try :
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok= True)

        with open(file_path, "wb") as file_obj :
            dill.dump(obj, file_obj)

    except Exception as e:
        logging.info("Error Occured in save_object method of utils.py module")
        raise CustomException(e,sys)
    
def load_object(file_path) : # loading our pickle file 
    try :
        with open(file_path, "rb") as file_obj :
            return dill.load(file_obj)
    except Exception as e :
        logging.info("Error Occurred in load_object method of utils.py module")

def upload_file(from_filename, to_filename, bucket_name):
    try :
        s3_resource = boto3.resource("s3")

        s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)

    except Exception as e :
        raise CustomException(e,sys)
    

def download_model(bucket_name, bucket_file_name, best_file_name):
    try :
        s3_client = boto3.client("s3")

        s3_client.download_file(bucket_name,bucket_file_name, best_file_name)

        return best_file_name
    
    except Exception as e:
        raise CustomException(e,sys)
   

def evaluate_model(X,y, models):
    try :
        X_train, X_test, y_train, y_test = train_test_split(
            X,y, test_size= 0.2, random_state= 42
        ) 

        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]

            model.fit(X_train, y_train)  #train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report 
    
    except Exception as e :
        raise CustomException(e,sys)
    