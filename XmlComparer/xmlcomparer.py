import logservice
logservice.init()
logger = logservice.getLogger('xmlcomparer')

import appconfig as config
config.init()

from multiprocessing import Process, Queue
from dataextractor import fetchextract_data
from datacomparer import compare_data

if __name__ == '__main__':

    q = Queue()

    logger.info('extracting post data from database')
    p_post = Process(target=fetchextract_data, args=(q, 'post'))
    p_post.start()

    if not config.post_only:
        logger.info('extracting pre data from database')
        p = Process(target=fetchextract_data, args=(q, 'pre'))
        p.start()
        p.join()
    
    p_post.join()

    success = [q.get()]    
    while not q.empty():
        success.append(q.get())

    logger.info('data fetch and extract complete. status : {}'.format(success))
    
    if all(success) :
        logger.info('reading pre and post data from files and writing output')
        compare_data()
    else:
        logger.info('failed fetching and extracting pre and post data. status : {}'.format(success))
        logger.info('exiting xmlcomparer')
    