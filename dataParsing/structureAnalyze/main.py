from StixParseWorker import StixParseWorker
from FieldsDocumentaryWorker import FieldsDocumentaryWorker
from parseStixXml import *
from printUtils import pprintDict
from DataParsingFactory import DataParsingFactory
from JobType import JobType
from settings import os, DATA_DIR, BIG_DATA_DIR
from hooks.HookFunctions import indicator_type_desc_start, close_file, indicator_type_desc
import warnings

XML_FILE_NAME = os.path.join(BIG_DATA_DIR,'ais_disclosable.xml')
CSV_FILE_NAME = os.path.join(DATA_DIR,'structureForGrephi.csv')
DEGREE_CSV_FILE_NAME = os.path.join(DATA_DIR,'degreeForStixStructure.csv')
FREQUENCY_CSV_FILE_NAME = os.path.join(DATA_DIR,'frequencyOfFieldInData.csv')
FREQUENCY_ROWS_CSV_FILE_NAME = os.path.join(DATA_DIR,'frequencyOfEdgesInData.csv')
ALL_AVG_DEGREE_CON_FILE_NAME = os.path.join(DATA_DIR,'all_avg_degree_con.pkl')

# %s is where the stix filename while be put at
FREQUENCY_CSV_FILE_NAMES = os.path.join(BIG_DATA_DIR,'weight_csv_files/frequencyOfFieldInData_%s.csv')

XML_FILE_DIR = os.path.join(BIG_DATA_DIR,'ais_201710/')

factory = DataParsingFactory()

'''
Notice: notice that there are args like justdo and stopafter, please use them during test period otherwise our workers
        have to keep working until get all the stix packages done which might cause about 20 minutes

Example:
        factory.goFindSomeoneDoThisJob( JobType.ParseStixFromXmlAndPrintValuesToConsole, xmlfilename=XML_FILE_NAME, justdo=1, stopafter=1)
        
    these methods will create or load field tree
        factory.goFindSomeoneDoThisJob( JobType.AnalyzeStixFromXmlAndBuildFieldTree, xmlfilename=XML_FILE_NAME, justdo=1, stopafter=1)
        factory.goFindSomeoneDoThisJob( JobType.AnalyzeStixFromXmlAndBuildFieldTree, xmlfilename=XML_FILE_NAME, stopafter=20)
        
        factory.goFindSomeoneDoThisJob( JobType.LoadFieldTree)
        
    these methods require a field tree created or loaded before called
        factory.goFindSomeoneDoThisJob( JobType.SaveFieldTree)
        factory.goFindSomeoneDoThisJob( JobType.PrintFieldTreeToConsole)
        factory.goFindSomeoneDoThisJob( JobType.PrintFieldTreeToCsvFile, csvfilename=CSV_FILE_NAME)
'''

warnings.filterwarnings('ignore')
# factory.goFindSomeoneDoThisJob( JobType.AnalyzeStixFromXmlAndBuildFieldTree, xmlfilename=XML_FILE_NAME)
# factory.goFindSomeoneDoThisJob( JobType.ParseStixFromXmlAndPrintValuesToConsole, xmlfilename=XML_FILE_NAME, stopafter=2)
# factory.goFindSomeoneDoThisJob( JobType.SaveFieldTree)
# factory.goFindSomeoneDoThisJob( JobType.LoadFieldTree)
# factory.goFindSomeoneDoThisJob( JobType.PrintFieldTreeToConsole)
# factory.goFindSomeoneDoThisJob( JobType.PrintFieldTreeToCsvFile, csvfilename=CSV_FILE_NAME)
# factory.goFindSomeoneDoThisJob( JobType.AnalyzeStixFromXmlAndDrawAGraph, xmlfilename=XML_FILE_NAME, stopafter=1, isdrawgraph=True)
# factory.goFindSomeoneDoThisJob( JobType.AnalyzeStixFromXmlAndDrawAGraph, xmlfilename=XML_FILE_NAME, stopafter=2, csvfilename=DEGREE_CSV_FILE_NAME)
# factory.goFindSomeoneDoThisJob( JobType.FeedDataAndDrawWeightedGraph, xmlfilename=XML_FILE_DIR, stopafter=3, isdrawgraph=True, isforeachpackage=True, iswidthasweight=False, isdrawminspintree=False)
# factory.goFindSomeoneDoThisJob( JobType.FeedDataAndDrawWeightedGraph, xmlfilename=XML_FILE_DIR, stopafter=20, isdrawgraph=True, isforeachpackage=False, iswidthasweight=True, isdrawminspintree=True)
# factory.goFindSomeoneDoThisJob( JobType.FeedDataAndDrawWeightedGraph, xmlfilename=XML_FILE_NAME, stopafter=15, isdrawgraph=True, isforeachpackage=False, iswidthasweight=True, isdrawminspintree=False, csvfilename=FREQUENCY_CSV_FILE_NAME)


factory.goFindSomeoneDoThisJob(
    JobType.FeedDataAndDrawWeightedGraph,
    xmlfilename=XML_FILE_DIR,
    stopafter=-1,
    isdrawgraph=False,
    isforeachpackage=True,
    iswidthasweight=False,
    isdrawminspintree=False,
    isclusteringnodebyname=True,
    islistnodeidx=False,
    isfullstructure=False,
    issaverowforeachpackage=False,
    isuseexistedtablenames=False,
    isavgdegreecon=True,
    picklefilename=ALL_AVG_DEGREE_CON_FILE_NAME,
    hookonstart=indicator_type_desc_start,
    hookonnode=indicator_type_desc,
    hookonend=close_file
)
"""
Enable these two function call to print COMPACT version edge frequency table
stopafter: stix number start from 0, -1 means use all
"""
'''
factory.goFindSomeoneDoThisJob(
    JobType.FeedDataAndDrawWeightedGraph,
    xmlfilename=XML_FILE_DIR,
    stopafter=0,
    isdrawgraph=False,
    isforeachpackage=False,
    iswidthasweight=False,
    isdrawminspintree=False,
    isclusteringnodebyname=True,
    islistnodeidx=False,
    isfullstructure=True,
)
factory.goFindSomeoneDoThisJob(
    JobType.FeedDataAndDrawWeightedGraph,
    xmlfilename=XML_FILE_DIR,
    stopafter=-1,
    isdrawgraph=False,
    isforeachpackage=True,
    iswidthasweight=False,
    isdrawminspintree=False,
    isclusteringnodebyname=True,
    islistnodeidx=False,
    isfullstructure=False,
    issaverowforeachpackage=True,
    isuseexistedtablenames=True,
    rowscsvfilename=FREQUENCY_ROWS_CSV_FILE_NAME
)
'''

"""
Enable these two function call to print MATRIX version edge frequency table
stopafter: stix number start from 0, -1 means use all
"""
'''
factory.goFindSomeoneDoThisJob(
    JobType.FeedDataAndDrawWeightedGraph,
    xmlfilename=XML_FILE_DIR,
    stopafter=0,
    isdrawgraph=False,
    isforeachpackage=False,
    iswidthasweight=False,
    isdrawminspintree=False,
    isclusteringnodebyname=True,
    islistnodeidx=False,
    isfullstructure=True,
)
factory.goFindSomeoneDoThisJob(
    JobType.FeedDataAndDrawWeightedGraph,
    xmlfilename=XML_FILE_DIR,
    stopafter=3,
    # justdo='poll_1479324463614_51.xml',  # ether filename or a number
    isdrawgraph=False,
    isforeachpackage=True,
    iswidthasweight=True,
    isdrawminspintree=False,
    isclusteringnodebyname=True,
    islistnodeidx=False,
    isfullstructure=False,
    issaverowforeachpackage=False,
    issavetablesforeachpackage=True,
    isuseexistedtablenames=True,
    csvfilename=FREQUENCY_CSV_FILE_NAMES,
    # rowscsvfilename=FREQUENCY_ROWS_CSV_FILE_NAME
    # csvfilename=FREQUENCY_CSV_FILE_NAME
)
'''
factory.print_time_per_job()
