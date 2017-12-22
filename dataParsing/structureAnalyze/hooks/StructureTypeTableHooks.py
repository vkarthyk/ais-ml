import csv
from settings import os, DATA_DIR, BIG_DATA_DIR
from common.Logger import Logger

logger = Logger("hooks.StructureTypeTableHooks")

FREQUENCY_ROWS_CSV_FILE_NAME = os.path.join(BIG_DATA_DIR,'StructureTypeTable.csv')

# tmpfilename = os.path.join(DATA_DIR,'test.csv')
# tmpfile = None
# tmpcsvwriter=None
class StructureTypeTableHook:
    title_list = []
    structure_str_list = []
    csvfile = None

    def before_all(self):
        self.csvfile = open(FREQUENCY_ROWS_CSV_FILE_NAME, 'wb')
        self.csvwriter = csv.writer(self.csvfile)
        # global title_list, tmpfile, tmpfilename, tmpcsvwriter
        # title_list = ['stix_name']
        # tmpfile = open(tmpfilename, 'wb')
        # tmpcsvwriter = csv.writer(tmpfile)

    def is_same_structure(self, s1, s2):
        k1 = set(s1.keys())
        k2 = set(s2.keys())
        if k1 != k2:
            return False
        for p in s1:
            if set(s1[p].keys()) != set(s2[p].keys()):
                return False
        return True

    def flatten_weights(self, weights):
        result = set()
        for p in weights:
            for c in weights:
                result.add(p+'->'+c)
        return result

    def outputWeightRow(self,**args):
        weights = args['weights']
        stixname = args['stixname']

        assert isinstance(weights, dict)
        assert isinstance(stixname, str)

        # self.logger.log('info', 'writing weight dict to:', filename)

        # if not self.is_titles_wrote:
        # self.logger.log('err', 'please write title row first')
        # self.writeWeightTitle(filename=filename, allstructure=allstructure, weights=weights)

        # stru_str = str(weights)
        stru_keys = self.flatten_weights(weights)

        if stru_keys in self.structure_str_list:
            stru_type = self.structure_str_list.index(stru_keys)
        else:
            stru_type = len(self.structure_str_list)
            self.structure_str_list.append(stru_keys)

        self.csvwriter.writerow([stru_type])
        print stru_type, len(self.structure_str_list)

    def end_of_compact_table(self):
        self.csvfile.close()


structure_type_table_hook = StructureTypeTableHook()
