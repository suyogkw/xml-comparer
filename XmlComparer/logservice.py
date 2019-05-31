import json
import os
import logging as logger

with open('xmlcomparer.config.json') as f:
    __data = json.load(f) 

os.makedirs(__data['output_dir'], exist_ok=True)
logger.basicConfig(
    level=logger.INFO,
    format="%(asctime)s [%(levelname)-5.5s] %(module)s [%(filename)-12.12s] %(message)s",
    handlers=[
        logger.FileHandler("{0}/{1}.log".format(__data['output_dir'], 'xmlcomparer')),
        logger.StreamHandler()
    ])
