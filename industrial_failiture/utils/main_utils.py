import yaml
from industrial_failiture.logging.logger import logging
from industrial_failiture.exception.custom_exception import IndustralFailitureException
import os,sys
import pickle
import numpy as np



def read_yaml(file_path:str) -> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise IndustralFailitureException(e,sys)
    
def write_yaml(file_path:str,content:object,replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as f:
            yaml.dump(content,f)
    except Exception as e:
        IndustralFailitureException(e,sys)




def load_object(file_path:str,) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            print(file_path)
            return pickle.load(file_obj)
    except Exception as e:
        raise IndustralFailitureException(e,sys)


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of mainUtils class")
        
        # make sure the parent directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # save the object into the file
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info("Exited the save_object method of mainUtils class")

    except Exception as e:
        raise IndustralFailitureException(e, sys)
    





