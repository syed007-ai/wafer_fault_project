from pymongo.mongo_client import MongoClient
import pandas as pd 
import json 

# uniform resource identifier 
uri = "mongodb+srv://obaidabubakar377:obaidabubakar377@cluster0.c8jeyzg.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# create database name and collection name 
DATABASE_NAME = "ML_Project"
COLLECTION_NAME = "waferfault"

#read data as df 
df = pd.read_csv("/Users/syed/Desktop/sensor_project/notebooks/wafer_23012020_041211.csv")
df.drop(columns=["Unnamed: 0"], axis = 1, inplace= True)

json_record = list(json.loads(df.T.to_json()).values()) # Transposing df, and then converting it to json

# now dump the data into database

client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)