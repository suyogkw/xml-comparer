import json
import pandas as pd
from collections import namedtuple
import logservice
logger = logservice.getLogger('appconfig')

def join_params(tables_file, join, suffix):
    params = pd.read_excel(tables_file,join)
    return ' and '.join(list(params.apply(lambda row: ' '.join([row['Table1']+suffix+'.'+row['Property1'],row['Operation'],row['Table2']+suffix+'.'+row['Property2']]), axis=1)))

def generate_sqlquery(tables_file, xmlcolumn, identifiers, suffix, select_clause, where_clause):
    tables = pd.read_excel(tables_file,'joins')    
    select_columns = ','.join(identifiers+[xmlcolumn])
    table_name = tables['Table'][0]+suffix    
    join_queries = '' if tables.iloc[1:].empty else ' '.join(list(tables.iloc[1:].apply(lambda x: ' '.join([x['Type'],x['Table']+suffix,'on',join_params(tables_file, x['Join'], suffix)]), axis=1)))
    
    return f'{select_clause} from {table_name} {join_queries} {where_clause}'


def init():
    global tables_file, chunksize, pre, post, release, output_dir, post_only, xpaths, xmlcolumn, identifiers, columns
    
    logger.info('*****************************  reading configuration : start *****************************')    

    with open('xmlcomparer.config.json') as f:
        __data = json.load(f)    
    
        tables_file = __data['tables_file']
   
        __sql = namedtuple('sql', __data['sql'].keys())(**__data['sql'])
        __pre = namedtuple('pre', __data['pre'].keys())(**__data['pre'])
        __post = namedtuple('post', __data['post'].keys())(**__data['post'])

        __tabledata = pd.read_excel(tables_file,'columns')
        
        xmlcolumn = __tabledata.iloc[0,'columns']
        identifiers = list(__tabledata.iloc[1:,'columns'].dropna())

        __data['pre']['query'] = generate_sqlquery(tables_file, xmlcolumn, identifiers, __pre.suffix, __sql.select_clause, __sql.where_clause)
        __data['post']['query'] = generate_sqlquery(tables_file, xmlcolumn, identifiers, __post.suffix, __sql.select_clause, __sql.where_clause)
    
        chunksize = __sql.chunksize 
        pre = namedtuple('pre', __data['pre'].keys())(**__data['pre'])
        post = namedtuple('post', __data['post'].keys())(**__data['post'])
        release = __data['release']
        output_dir = __data['output_dir']
        post_only = __data['post_only']
    

    with open('xmlcomparer.xpaths.json') as f:
        xpaths = json.load(f)
        columns = list(xpaths.keys())
    
    logger.info(f'using tables configuration : {tables_file}')
    logger.info(f'using identifiers : {identifiers}')
    logger.info(f'using chuncksize : {chuncksize}')
    logger.info(f'using pre configuration : {pre}')
    logger.info(f'using post configuration : {post}')
    logger.info(f'creating for release : {release}')
    logger.info(f'output configuration : {output_dir}')
    logger.info(f'run post_only : {post_only}')
    logger.info(f'xml comparison paths : {len(xpaths)}')
    
    logger.info('*****************************  reading configuration : complete *****************************')
