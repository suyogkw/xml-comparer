import pandas as pd
from multiprocessing import Queue
import appconfig as config
import logservice
logger = logservice.getLogger('dataextractor')
import os
import time

def fetchextract_data(q, key_prepost):
    logger.info(os.getpid())
    logger.info(getattr(config,key_prepost).server)
    time.sleep(10)
    q.put(True)
