import json
from collections import namedtuple
from logservice import logger


def generate_sqlquery(tables_file, suffix, select_clause, where_clause):
    pass


logger.info('reading configuration : start')

with open('xmlcomparer.config.json') as f:
    __data = json.load(f)    
    
    tables_file = __data['tables_file']
   
    __sql = namedtuple('sql', __data['sql'].keys())(**__data['sql'])
    __pre = namedtuple('pre', __data['pre'].keys())(**__data['pre'])
    __post = namedtuple('post', __data['post'].keys())(**__data['post'])
    __data['pre']['query'] = generate_sqlquery(tables_file, __pre.suffix ,__sql.select_clause,__sql.where_clause)
    __data['post']['query'] = generate_sqlquery(tables_file, __post.suffix ,__sql.select_clause,__sql.where_clause)
    
    chunksize = __sql.chunksize 
    pre = namedtuple('pre', __data['pre'].keys())(**__data['pre'])
    post = namedtuple('post', __data['post'].keys())(**__data['post'])
    release = __data['release']
    output_dir = __data['output_dir']
    post_only = __data['post_only']

with open('xmlcomparer.xpaths.json') as f:
    xpaths = json.load(f)

logger.info('reading configuration : complete')
