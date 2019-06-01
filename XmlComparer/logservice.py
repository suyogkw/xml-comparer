import json
import os
import logging

def init():
    with open('xmlcomparer.config.json') as f:
        __data = json.load(f) 

        os.makedirs(__data['output_dir'], exist_ok=True)
        logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s][%(name)-15s]: %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(__data['output_dir'], 'xmlcomparer')),
            logging.StreamHandler()
        ])
    
def getLogger(fname):
   return logging.getLogger(fname)
    

