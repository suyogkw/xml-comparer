import pandas as pd
import numpy as np
import appconfig as config
import logservice
logger = logservice.getLogger('datacomparer')

def prepare_data(df_pre, df_post):
    
    df_pre.drop_duplicates(config.identifiers,inplace=True)
    df_post.drop_duplicates(config.identifiers,inplace=True)

    df_outer = pd.merge(df_pre[config.identifiers], df_post[config.identifiers], on=config.identifiers, how='outer', indicator= True)
    df_outer = df_outer.query('_merge != "both"')[config.identifiers+['_merge']]

    df_combined = pd.merge(df_pre, df_post, on=config.identifiers, suffixes=('_pre', '_post'))
    df_pre = df_combined[config.identifiers+[x+'_pre' for x in config.columns]]
    df_pre.columns = config.identifiers+config.columns
    df_post = df_combined[config.identifiers+[x+'_post' for x in config.columns]]
    df_post.columns = config.identifiers+config.columns

    return df_pre, df_post, df_outer

def prepare_report(df_pre, df_post, diff):
    
    diff_stack = diff.stack()
    changed = diff_stack[diff_stack]
    difference_locations = np.where(diff)
    changed_from = df_pre[config.columns].values[difference_locations]
    changed_to = df_post[config.columns].values[difference_locations]

    changed.index.names = ['id','column']
    detail_diff.index.names = ['id']
    summary_diff = pd.DataFrame({'from': changed_from, 'to': changed_to},index=changed.index)
    summary_diff = df_pre[config.identifiers].join(summary_diff)
    summary_diff.reset_index('column', inplace=True)
    summary_diff = pd.concat([summary_diff.iloc[:,1:-2], summary_diff.iloc[:,0],summary_diff.iloc[:,-2:]], axis = 1)

    columnwise_summary = summary_diff.groupby('column',as_index=False).count().iloc[:,:2]
    columnwise_summary.columns = ['column','count']
    
    return columnwise_summary

def write_output(diff, summary_diff,df_summary_report, df_outer):
    
    os.makedirs(config.output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    diff_mapfilename = timestamp+'_diff_map.csv'
    detail_reportfilename = timestamp+'_detailreport.csv'
    summary_reportfilename = timestamp+'_summaryreport.csv'
    incomplete_reportfilename = timestamp+'_incompletedata.csv'

    diff.to_csv(output_dir+'/'+diff_mapfilename)
    summary_diff.to_csv(output_dir+'/'+detail_reportfilename, index=False)
    df_summary_report.to_csv(output_dir+'/'+summary_reportfilename, index=False)
    if not df_outer.empty : df_outer.to_csv(output_dir+'/'+incomplete_reportfilename, index=False)

def compare_data():

    logger.info('data reading and preparation : start') 

    df_pre = pd.read_csv(config.output_dir+'/'+config.pre.datafile)
    df_post = pd.read_csv(config.output_dir+'/'+config.pre.datafile)
    
    total_rows_pre = len(df_pre)
    total_rows_post = len(df_pre)
    
    df_pre, df_post, df_outer = prepare_data(df_pre, df_post)

    logger.info('data reading and preparation : complete') 

    logger.info('calculating difference : start') 

    diff = (df_pre[config.columns] != df_post[config.columns]) & ~(df_pre[config.columns].isnull() & df_post[config.columns].isnull())
    compared_rows = len(diff)
    different_rows = sum(diff.apply(lambda x: any(x), axis=1))

    logger.info('calculating difference : complete') 

    logger.info('creating summary and detailed report : start') 

    df_summary_report = pd.DataFrame({'column':['total pre','total post','comaprison rows', 'mismatch rows','',''],
    'count':[total_rows_pre,total_rows_post, compared_rows, different_rows,'','']})

    columnwise_summary = prepare_report(df_pre, df_post, diff)
    df_summary_report = df_summary_report.append(columnwise_summary)
    diff = df_pre[config.identifiers].join(~diff)
    
    logger.info('creating summary and detailed report : complete') 

    logger.info('writing report to output file : start') 

    write_output(diff, summary_diff,df_summary_report, df_outer)
    
    logger.info('writing report to output file : complete')

