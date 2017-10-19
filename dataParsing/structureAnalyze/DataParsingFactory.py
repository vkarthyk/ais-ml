from FieldsDocumentaryWorker import FieldsDocumentaryWorker
from GraphicWorker import GraphicWorker
from GraphicWithDataWorker import GraphicWithDataWorker
from IOWorker import IOWorker
from JobType import *
from StixParseWorker import StixParseWorker
from common.Logger import Logger
from parseStixXml import *
from printUtils import pprintDict
from settings import DATA_DIR
import os, errno
import time

DEFAULT_TREE_PICKLE_FILE_NAME = os.path.join(DATA_DIR, 'fieldTree.pkl')


class DataParsingFactory:

    def __init__(self):
        self.logger = Logger(self)
        self.tmp_G=None
        self.tmp_dict=None
        self.jobs=[]
        self.time_per_job=[]

    def stix_packages_fn_iterater(self, fn_or_dir, stopafter, onlyuse=None):
        # if fn_or_dir[-1] == '/':
        if os.path.isdir(fn_or_dir):
            self.is_dir = True
            for i in stixFileNameInDirectory(fn_or_dir, stopafter=stopafter, onlyuse=onlyuse):
                yield i
        else:
            self.is_dir = False
            for i in xmlFileName2EnumStixFileName(fn_or_dir, stopafter=stopafter):
                yield i

    def __getParam(self, argname, nonevalue=None, errmsg=None):
        if errmsg is not None and not self.requirements.has_key(argname):
            self.logger.log('err', errmsg)
            exit(-1)
        return self.requirements[argname] if self.requirements.has_key(argname) else nonevalue

    def goFindSomeoneDoThisJob(self, *jobs, **requirements):
        self.requirements=requirements
        self.jobs.append(jobs)
        for job in jobs:
            self.logger.log('info', 'Start to work on', job)
            time_start = time.time()
            time_end = -1

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

            '''
            notice: there are two job types
            '''
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
                isclusteringnodebyname = requirements['isclusteringnodebyname'] if requirements.has_key('isclusteringnodebyname') else False
                islistnodeidx = requirements['islistnodeidx'] if requirements.has_key('islistnodeidx') else False
                isfullstructure = requirements['isfullstructure'] if requirements.has_key('isfullstructure') else False
                isuseexistedtablenames = requirements['isuseexistedtablenames'] if requirements.has_key('isuseexistedtablenames') else False
                issavetablesforeachpackage = requirements['issavetablesforeachpackage'] if requirements.has_key('issavetablesforeachpackage') else False
                issaverowforeachpackage = requirements['issaverowforeachpackage'] if requirements.has_key('issaverowforeachpackage') else False
                rowsCsvFileName = requirements['rowscsvfilename'] if requirements.has_key('rowscsvfilename') else -1

                # worker = FieldsDocumentaryWorker()
                worker = GraphicWorker() if job is JobType.AnalyzeStixFromXmlAndDrawAGraph else GraphicWithDataWorker()
                if isclusteringnodebyname:
                    worker.set_is_clustering_node_by_name()
                if isfullstructure:
                    worker.set_is_full_structure()
                if islistnodeidx:
                    worker.set_is_display_list_node_index()
                if weightCsvFileName is not -1 or rowsCsvFileName is not -1:
                    ioworker=IOWorker()
                    if issavetablesforeachpackage:
                        if isuseexistedtablenames:
                            rowlist, collist = ioworker.get_child_parent_lists(self.tmp_dict)
                    if issaverowforeachpackage:
                        if isuseexistedtablenames:
                            allstructure = self.tmp_dict


                # for ind, stix_fn in enumerate(xmlFileName2EnumStixFileName(xmlfilename,stopafter=stopAfterFinishRound)):
                for ind, stix_fn in enumerate(self.stix_packages_fn_iterater(xmlfilename,stopafter=stopAfterFinishRound)):
                    # if stopAfterFinishRound > -1:
                    #     if ind > stopAfterFinishRound:
                    #         break
                    if justDoThisRound != -1:
                        if justDoThisRound == -2:
                            break
                        if type(justDoThisRound) is str:
                            if os.path.split(stix_fn)[1] != justDoThisRound:
                                continue
                            else:
                                justDoThisRound = -2 # need to break after this round
                        elif ind != justDoThisRound:
                            continue
                    self.logger.log('info','I\'m working on stix_package #'+str(ind))
                    stix_package = stixFileName2StixPackageObj(stix_fn)

                    if isforeachpackage:
                        worker.clear_graph()

                    worker.doYourWork(stix_package)

                    if isforeachpackage:
                        self.tmp_dict = worker.get_edge_weight_dict()
                        self.tmp_G = worker.get_graph()
                        # worker.ava_degree_conn()
                        if weightCsvFileName is not -1:
                            if issavetablesforeachpackage:
                                twoparts = weightCsvFileName.split('%s')
                                if len(twoparts) is not 2:
                                    self.logger.log('err', 'please include %s (only once) inside the target csv filename, to decide where to write the corresponding stix file name')
                                    exit(-1)
                                if os.path.dirname(twoparts[1]) is not '':
                                    self.logger.log('warn', '%s is in a directory name not a filename, will create many directories.')
                                thisCsvFileName=twoparts[0] + stix_fn.split('/')[-1] + twoparts[1]
                                try:
                                    os.makedirs(os.path.dirname(thisCsvFileName))
                                except OSError as e:
                                    if not e.errno is errno.EEXIST:
                                        self.logger.log('err', 'directory create fail')
                                        raise

                                if isuseexistedtablenames:
                                    ioworker.outputWeightTable(self.tmp_dict, thisCsvFileName, rowlist, collist)
                                else:
                                    ioworker.outputWeightTable(self.tmp_dict, thisCsvFileName)
                        if rowsCsvFileName != -1:
                            if issaverowforeachpackage:
                                if isuseexistedtablenames:
                                    ioworker.outputWeightRow(weights=self.tmp_dict, filename=rowsCsvFileName, allstructure=allstructure)
                                else:
                                    ioworker.outputWeightRow(weights=self.tmp_dict, filename=rowsCsvFileName)
                        if isdrawgraph:
                            stix_name = stix_fn.split('/')[-1] if self.is_dir else ind
                            worker.draw(stix_name, is_width_as_weight=iswidthasweight, is_draw_min_spin_tree=isdrawminspintree)

                if job is JobType.FeedDataAndDrawWeightedGraph and not isforeachpackage:
                    self.tmp_dict = worker.get_edge_weight_dict()
                    self.tmp_G = worker.get_graph()
                    worker.ava_degree_conn()
                    if isdrawgraph:
                        worker.draw("All Stix Packages", is_width_as_weight=iswidthasweight, is_draw_min_spin_tree=isdrawminspintree)

                    if weightCsvFileName is not -1:
                        if issavetablesforeachpackage:
                            twoparts = weightCsvFileName.split('%s')
                            if len(twoparts) > 1:
                                self.logger.log('err', 'remember to remove %s in the target file name')
                                exit(-1)
                            if not os.path.dirname(weightCsvFileName) is not '':
                                self.logger.log('err', 'target file name is a directory, please change to a file name')
                                exit(-1)
                            if isuseexistedtablenames:
                                ioworker.outputWeightTable(self.tmp_dict, weightCsvFileName, rowlist, collist)
                            else:
                                ioworker.outputWeightTable(self.tmp_dict, weightCsvFileName)
                    if rowsCsvFileName != -1:
                        if issaverowforeachpackage:
                            if isuseexistedtablenames:
                                ioworker.outputWeightRow(weights=self.tmp_dict, filename=rowsCsvFileName, allstructure=allstructure)
                            else:
                                ioworker.outputWeightRow(weights=self.tmp_dict, filename=rowsCsvFileName)

                if isdrawgraph:
                    time_end = time.time()
                    worker.draw_show()

            if time_end == -1:
                time_end = time.time()
            self.time_per_job.append(time_end-time_start)

            self.logger.log('info', 'Job', job, 'has done!')

        self.logger.log('info', 'All the jobs have done! Enjoy your data!')

    def print_time_per_job(self):
        for i, j in enumerate(self.jobs):
            self.logger.log('info', 'Time of Job #'+str(i), self.time_per_job[i], 'seconds')

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
