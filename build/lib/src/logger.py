import sys
import os
import logging 
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log"

logs_path  = os.path.join(os.getcwd(),"logs", LOG_FILE) # creating path -> log_file in current dir.

os.makedirs(logs_path, exist_ok= True) # making dir of the logs_path 

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE ) # joined with path and log_file

logging.basicConfig(
    filename= LOG_FILE_PATH,
    format= "[%(asctime)s] %(lineno)d %(name)s - %(message)s",
    level= logging.INFO
)