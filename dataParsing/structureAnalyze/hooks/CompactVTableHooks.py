import csv
from settings import os, DATA_DIR, BIG_DATA_DIR
from common.Logger import Logger

class CompactVTableHooks:
    def __init__(self):
        self.logger = Logger(self)

    FREQUENCY_ROWS_CSV_FILE_NAME = os.path.join(BIG_DATA_DIR,'IndicatorCompactTable.csv')

    tmpfilename = os.path.join(DATA_DIR,'test.csv')
    tmpfile = None
    tmpcsvwriter=None

    title_list = []

    def __get_column_name(self, p, c):
        return p + '->' + c

    def before_all(self):
        self.title_list = ['stix_name']
        self.tmpfile = open(self.tmpfilename, 'wb')
        self.tmpcsvwriter = csv.writer(self.tmpfile)

    def outputWeightRow(self, **args):
        weights = args['weights']
        stixname = args['stixname']

        assert isinstance(weights, dict)
        assert isinstance(stixname, str)

        # self.logger.log('info', 'writing weight dict to:', filename)

        # if not self.is_titles_wrote:
        # self.logger.log('err', 'please write title row first')
        # self.writeWeightTitle(filename=filename, allstructure=allstructure, weights=weights)

        this_row = [''] * len(self.title_list)
        this_row[0] = stixname
        for p in weights:
            for c in weights[p]:
                column_name = self.__get_column_name(p, c)
                if column_name not in self.title_list:
                    self.title_list.append(column_name)
                    this_row.append(weights[p][c])
                else:
                    this_row[self.title_list.index(column_name)] = weights[p][c]

        self.tmpcsvwriter.writerow(this_row)

    def end_of_compact_table(self):
        self.tmpfile.close()

        title_list_len = len(self.title_list)
        # f.write(delimitor.join(titles))
        realfw = open(self.FREQUENCY_ROWS_CSV_FILE_NAME, 'wb')
        realfwcsv = csv.writer(realfw)
        tmpfr = open(self.tmpfilename, 'rb')
        tmpfrcsv = csv.reader(tmpfr)

        realfwcsv.writerow(self.title_list)
        for row in tmpfrcsv:
            # replace '' with 0
            for i, x in enumerate(row):
                if len(row[i]) < 1:
                    row[i] = 0
            row += [0]*(title_list_len - len(row))
            realfwcsv.writerow(row)

        realfw.close()
        tmpfr.close()

compactVTableHooks = CompactVTableHooks()
