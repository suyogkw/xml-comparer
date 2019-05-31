import os
import logging as logger
import appconfig as config
from multiprocessing import Process, Queue
from dataextractor import fetchextract_data
from datacomparer import compare_data

if __name__ == '__main__':

    logger.info(os.getpid())
    q = Queue()

    if not config.post_only:
        logger.info('extracting pre data from database')
        p = Process(target=fetchextract_data, args=(q, 'pre'))
        p.start()
        p.join()

    logger.info('extracting post data from database')
    p_post = Process(target=fetchextract_data, args=(q, 'post'))
    p_post.start()
    p_post.join()

    success = q.get()

    logger.info('reading pre and post data from files and writing output')

    compare_data()