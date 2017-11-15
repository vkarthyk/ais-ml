from common.Logger import Logger
from dataParsing.structureAnalyze.parseStixXml import stixFileName2StixPackageObj
from settings import os, BIG_DATA_DIR

class RawDataWorker:
    def __init__(self):
        self.logger = Logger(self)

    def get_feature_column(self, stix_name_list, feature_select_func_list):
        if isinstance(feature_select_func_list, list):
            result_list_of_list = []
            for i in range(len(feature_select_func_list)):
                result_list_of_list.append([])
            for fn in stix_name_list:
                stix_package = stixFileName2StixPackageObj(os.path.join(BIG_DATA_DIR, 'ais_201710', fn))
                for i, func in enumerate(feature_select_func_list):
                    result_list_of_list[i].append(func(stix_package))
            return result_list_of_list
        else:
            result_list = []
            for fn in stix_name_list:
                stix_package = stixFileName2StixPackageObj(os.path.join(BIG_DATA_DIR, 'ais_201710', fn))
                result_list.append(feature_select_func_list(stix_package))
            return result_list

    def __default_iter_node(self, node):
        yield node

    def get_feature_column_from_node(self, stix_name_list, feature_select_func_list, iter_func=__default_iter_node):
        if isinstance(feature_select_func_list, list):
            result_list_of_list = []
            for i in range(len(feature_select_func_list)):
                result_list_of_list.append([])
            old_stix = ''
            for fn in stix_name_list:
                if old_stix == fn:
                    continue
                old_stix = fn
                stix_package = stixFileName2StixPackageObj(os.path.join(BIG_DATA_DIR, 'ais_201710', fn))
                for node in iter_func(stix_package):
                    for i, func in enumerate(feature_select_func_list):
                        result_list_of_list[i].append(func(node))
            return result_list_of_list
        else:
            result_list = []
            old_stix = ''
            for fn in stix_name_list:
                if old_stix == fn:
                    continue
                old_stix = fn
                stix_package = stixFileName2StixPackageObj(os.path.join(BIG_DATA_DIR, 'ais_201710', fn))
                for node in iter_func(stix_package):
                    result_list.append(feature_select_func_list(node))
            return result_list
