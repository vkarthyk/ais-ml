from common.Logger import Logger
import csv

class CsvWorker:
    def __init__(self):
        self.logger = Logger(self)

    def get_column_as_list(self, filename, column_name):
        with open(filename, 'rb') as rfile:
            rfilereader = csv.reader(rfile)
            titles = rfilereader.next()
            ind = titles.index(column_name)
            result = []
            for row in rfilereader:
                result.append(row[ind])
        return result

    def write_list_as_column(self, filename, label, data_list):
        with open(filename, 'wb') as wfile:
            wfilewriter = csv.writer(wfile)
            wfilewriter.writerow([label])
            for d in data_list:
                wfilewriter.writerow([d])

    def write_list_of_list_as_column(self, filename, label_list, data_list_list):
        with open(filename, 'wb') as wfile:
            wfilewriter = csv.writer(wfile)
            wfilewriter.writerow(label_list)
            for i in range(len(data_list_list[0])):
                this_row = []
                for j in range(len(data_list_list)):
                    this_row.append(data_list_list[j][i])
                wfilewriter.writerow(this_row)
