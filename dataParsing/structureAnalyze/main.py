from StixParseWorker import StixParseWorker
from FieldsDocumentaryWorker import FieldsDocumentaryWorker
from parseStixXml import *
from printUtils import pprintDict
from DataParsingFactory import DataParsingFactory
from JobType import JobType
from settings import os, DATA_DIR, BIG_DATA_DIR
import warnings

XML_FILE_NAME = os.path.join(BIG_DATA_DIR,'ais_disclosable.xml')
CSV_FILE_NAME = os.path.join(DATA_DIR,'structureForGrephi.csv')
DEGREE_CSV_FILE_NAME = os.path.join(DATA_DIR,'degreeForStixStructure.csv')
FREQUENCY_CSV_FILE_NAME = os.path.join(DATA_DIR,'frequencyOfFieldInData.csv')
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
# factory.goFindSomeoneDoThisJob( JobType.AnalyzeStixFromXmlAndDrawAGraph, xmlfilename=XML_FILE_NAME, stopafter=1)
# factory.goFindSomeoneDoThisJob( JobType.AnalyzeStixFromXmlAndDrawAGraph, xmlfilename=XML_FILE_NAME, stopafter=2, csvfilename=DEGREE_CSV_FILE_NAME)
factory.goFindSomeoneDoThisJob( JobType.FeedDataAndDrawWeightedGraph, xmlfilename=XML_FILE_DIR, stopafter=2, isdrawgraph=True, isforeachpackage=True, iswidthasweight=False, isdrawminspintree=False)
# factory.goFindSomeoneDoThisJob( JobType.FeedDataAndDrawWeightedGraph, xmlfilename=XML_FILE_NAME, stopafter=2, csvfilename=FREQUENCY_CSV_FILE_NAME)
