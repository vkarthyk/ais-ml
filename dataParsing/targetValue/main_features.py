from CsvWorker import CsvWorker
from RawDataWorker import RawDataWorker
from settings import os, DATA_DIR, BIG_DATA_DIR
from common.Logger import Logger
from featureExtractHooks.targetExtract import intent, indicator_type, indicator_description
from nodeIterator.nodeIterators import indicator_iterator

logger = Logger("main")

FREQUENCY_ROWS_CSV_FILE_NAME = os.path.join(BIG_DATA_DIR,'StructureCompactTable.csv')
INDICATOR_COMPACT_CSV_FILE_NAME = os.path.join(BIG_DATA_DIR, 'useful','IndicatorCompactTable.csv')
TARGET_VAR_FILE_NAME = os.path.join(BIG_DATA_DIR,'Intent.csv')
INDICATOR_TARGET_FILE_NAME = os.path.join(BIG_DATA_DIR,'IndicatorTargets.csv')

# init
csv_worker = CsvWorker()
raw_data_worker = RawDataWorker()

# get the stix name order
stix_list = csv_worker.get_column_as_list(INDICATOR_COMPACT_CSV_FILE_NAME, 'stix_name')

# extract features
# result = raw_data_worker.get_feature_column(stix_list, intent)
result = raw_data_worker.get_feature_column_from_node(stix_list, [indicator_type, indicator_description], iter_func=indicator_iterator)

# csv_worker.write_list_as_column(TARGET_VAR_FILE_NAME, 'intent', result)
csv_worker.write_list_of_list_as_column(INDICATOR_TARGET_FILE_NAME, ['indicator_type', 'indicator_description'], result)
