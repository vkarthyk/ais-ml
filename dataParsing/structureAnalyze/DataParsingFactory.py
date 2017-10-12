from FieldsDocumentaryWorker import FieldsDocumentaryWorker
from GraphicWorker import GraphicWorker
from GraphicWithDataWorker import GraphicWithDataWorker
from JobType import *
from StixParseWorker import StixParseWorker
from common.Logger import Logger
from parseStixXml import *
from printUtils import pprintDict
from settings import DATA_DIR, os

DEFAULT_TREE_PICKLE_FILE_NAME = os.path.join(DATA_DIR, 'fieldTree.pkl')


class DataParsingFactory:

    def __init__(self):
        self.logger = Logger(self)

    def stix_packages_fn_iterater(self, fn_or_dir, stopafter, onlyuse=None):
        if fn_or_dir[-1] == '/':
            self.is_dir = True
            for i in stixFileNameInDirectory(fn_or_dir, stopafter=stopafter, onlyuse=onlyuse):
                yield i
        else:
            self.is_dir = False
            for i in xmlFileName2EnumStixFileName(fn_or_dir, stopafter=stopafter):
                yield i

    def __getParam(self, requirements, argname):
        if argname is 'xmlfilename':
            if not requirements.has_key('xmlfilename'):
                self.logger.log('err','at least give me a xml file name to parse, please :)')
                return -1
            return requirements['xmlfilename']
        elif argname is 'stopafter':
            stopAfterFinishRound = requirements['stopafter'] if requirements.has_key('stopafter') else -1
        elif argname is 'justdo':
            justDoThisRound = requirements['justdo'] if requirements.has_key('justdo') else -1

    def goFindSomeoneDoThisJob(self, *jobs, **requirements):
        for job in jobs:
            self.logger.log('info', 'Start to work on', job)

            if job is JobType.ParseStixFromXmlAndPrintValuesToConsole:
                if not requirements.has_key('xmlfilename'):
                    self.logger.log('err', '{',job, '}','at least give me a xml file name to parse, please :)')
                    return -1
                xmlfilename = requirements['xmlfilename']
                stopAfterFinishRound = requirements['stopafter'] if requirements.has_key('stopafter') else -1
                justDoThisRound = requirements['justdo'] if requirements.has_key('justdo') else -1

                worker = StixParseWorker()
                for ind, stix_fn in enumerate(self.stix_packages_fn_iterater(xmlfilename,stopafter=stopAfterFinishRound)):
                    # if stopAfterFinishRound > -1:
                    #     if ind > stopAfterFinishRound:
                    #         break
                    if justDoThisRound > -1:
                        if ind is not justDoThisRound:
                            continue
                    self.logger.log('info','I\'m working on stix_package #'+str(ind))
                    stix_package = stixFileName2StixPackageObj(stix_fn)
                    worker.consumeStix(stix_package)

                stix_fields_list_of_list = worker.getStixFieldsList()
                stix_fields_dict_of_list = worker.getStixFieldsDict()
                pprintDict(stix_fields_dict_of_list)

            if job is JobType.AnalyzeStixFromXmlAndBuildFieldTree:
                if not requirements.has_key('xmlfilename'):
                    self.logger.log('err', '{',job, '}','at least give me a xml file name to parse, please :)')
                    return -1
                xmlfilename = requirements['xmlfilename']
                stopAfterFinishRound = requirements['stopafter'] if requirements.has_key('stopafter') else -1
                justDoThisRound = requirements['justdo'] if requirements.has_key('justdo') else -1

                worker = FieldsDocumentaryWorker()
                for ind, stix_fn in enumerate(self.stix_packages_fn_iterater(xmlfilename, stopafter=stopAfterFinishRound)):
                    # if stopAfterFinishRound > -1:
                    #     if ind > stopAfterFinishRound:
                    #         break
                    if justDoThisRound > -1:
                        if ind is not justDoThisRound:
                            continue
                    self.logger.log('info','I\'m working on stix_package #'+str(ind))
                    stix_package = stixFileName2StixPackageObj(stix_fn)
                    worker.consumeStix(stix_package)

                self.fieldTree = worker.getTree()

            if job is JobType.SaveFieldTree:
                if not hasattr(self, 'fieldTree'):
                    self.logger.log('err', '{',job, '}', 'we don\'t even a field-tree at this point to save, we need to build it first.')
                    return -1
                fieldtreepklfn = requirements['fieldtreepklfn'] if requirements.has_key('fieldtreepklfn') else DEFAULT_TREE_PICKLE_FILE_NAME
                worker = FieldsDocumentaryWorker()
                worker.saveTreeToFile(self.fieldTree, fieldtreepklfn)

            if job is JobType.LoadFieldTree:
                fieldtreepklfn = requirements['fieldtreepklfn'] if requirements.has_key('fieldtreepklfn') else DEFAULT_TREE_PICKLE_FILE_NAME
                worker = FieldsDocumentaryWorker()
                self.fieldTree = worker.loadTreeFrFile(fieldtreepklfn)

            if job is JobType.PrintFieldTreeToConsole:
                if not hasattr(self, 'fieldTree'):
                    self.logger.log('err', '{',job, '}', 'we don\'t even a field-tree at this point to save, we need to build it first.')
                    return -1
                worker = FieldsDocumentaryWorker()
                worker.printTree2Console(self.fieldTree)

            if job is JobType.PrintFieldTreeToCsvFile:
                if not hasattr(self, 'fieldTree'):
                    self.logger.log('err', '{',job, '}', 'we don\'t even a field-tree at this point to save, we need to build it first.')
                    return -1
                if not requirements.has_key('csvfilename'):
                    self.logger.log('err', '{',job, '}','we need a CSV file name to save your tree')
                    return -1
                csvfilename = requirements['csvfilename']
                worker = FieldsDocumentaryWorker()
                worker.printTree2Csv(self.fieldTree, csvfilename)

            if job in [JobType.AnalyzeStixFromXmlAndDrawAGraph, JobType.FeedDataAndDrawWeightedGraph]:
                if not requirements.has_key('xmlfilename'):
                    self.logger.log('err', '{',job, '}','at least give me a xml file name to parse, please :)')
                    return -1
                xmlfilename = requirements['xmlfilename']
                stopAfterFinishRound = requirements['stopafter'] if requirements.has_key('stopafter') else -1
                justDoThisRound = requirements['justdo'] if requirements.has_key('justdo') else -1
                weightCsvFileName = requirements['csvfilename'] if requirements.has_key('csvfilename') else -1
                isdrawgraph = requirements['isdrawgraph'] if requirements.has_key('isdrawgraph') else False
                isforeachpackage = requirements['isforeachpackage'] if requirements.has_key('isforeachpackage') else False
                isdrawminspintree = requirements['isdrawminspintree'] if requirements.has_key('isdrawminspintree') else False
                iswidthasweight = requirements['iswidthasweight'] if requirements.has_key('iswidthasweight') else False

                # worker = FieldsDocumentaryWorker()
                worker = GraphicWorker() if job is JobType.AnalyzeStixFromXmlAndDrawAGraph else GraphicWithDataWorker()
                # for ind, stix_fn in enumerate(xmlFileName2EnumStixFileName(xmlfilename,stopafter=stopAfterFinishRound)):
                for ind, stix_fn in enumerate(self.stix_packages_fn_iterater(xmlfilename,stopafter=stopAfterFinishRound)):
                    # if stopAfterFinishRound > -1:
                    #     if ind > stopAfterFinishRound:
                    #         break
                    if justDoThisRound > -1:
                        if ind is not justDoThisRound:
                            continue
                    self.logger.log('info','I\'m working on stix_package #'+str(ind))
                    stix_package = stixFileName2StixPackageObj(stix_fn)

                    if isforeachpackage:
                        worker.clear_graph()

                    worker.doYourWork(stix_package)

                    if isforeachpackage:
                        worker.ava_degree_conn()
                        if isdrawgraph:
                            stix_name = stix_fn.split('/')[-1] if self.is_dir else ind
                            worker.draw(stix_name, is_width_as_weight=iswidthasweight, is_draw_min_spin_tree=isdrawminspintree)
                if weightCsvFileName is not -1:
                    worker.outputWeight(weightCsvFileName)
                if not isforeachpackage:
                    worker.ava_degree_conn()
                    if isdrawgraph:
                        worker.draw("All Stix Packages", is_width_as_weight=iswidthasweight, is_draw_min_spin_tree=isdrawminspintree)
                if isdrawgraph:
                    worker.draw_show()




            self.logger.log('info', 'Job', job, 'has done!')

        self.logger.log('info', 'All the jobs have done! Enjoy your data!')

# # worker = StixParseWorker()
# worker = FieldsDocumentaryWorker()
# for ind, stix_fn in enumerate(xmlFileName2EnumStixFileName(XML_FILE_NAME)):
#     # if ind is not 20:
#     #     continue
#     if ind > 2:
#         break
#     print 'I\'m working on stix_package #'+str(ind)
#     stix_package = stixFileName2StixPackageObj(stix_fn)
#     worker.consumeStix(stix_package)

# worker.saveTreeToFile()
# worker.printTree2Csv(CSV_FILE_NAME)

# stix_fields_list_of_list = worker.getStixFieldsList()
# stix_fields_dict_of_list = worker.getStixFieldsDict()
# pprintDict(stix_fields_dict_of_list)
