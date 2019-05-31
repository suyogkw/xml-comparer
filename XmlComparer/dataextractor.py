import pandas as pd
from multiprocessing import Queue
import logging as logger
import os

def fetchextract_data(q, prepost):
    logger.info(os.getpid())
    q.put(True)
