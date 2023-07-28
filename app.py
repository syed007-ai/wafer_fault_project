from flask import Flask, render_template, jsonify, request, send_file
from src.exception import CustomException
from src.logger import logging as lg 
import os, sys

from src.pipelines.trainingpipeline import TrainPipeline
#from src.pipelines.predictionpipeline import PredictionPipeline 

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my App"


@app.route("/train")
def train_route():
    try :
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()

        return "Training Completed ."
    except Exception as e:
        raise CustomException(e,sys)
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 5000, debug= True)