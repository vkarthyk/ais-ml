from settings import os, DATA_DIR, BIG_DATA_DIR
from stix.indicator.indicator import Indicator
from common.Logger import Logger

FREQUENCY_ROWS_CSV_FILE_NAME = os.path.join(DATA_DIR,'IndicatorTypeDesc.csv')

f=None
logger = Logger("hooks.HookFunctions")

def open_file():
    global f
    f = open(FREQUENCY_ROWS_CSV_FILE_NAME, 'wb')

def close_file():
    f.close()

def indicator_type_desc_start():
    open_file()
    f.write('Indicator_Type;Indicator_Description\n')

def indicator_type_desc(node):
    if not isinstance(node, Indicator):
        return

    if len(node.indicator_types) == 0:
        return
        # logger.log('warn', 'what??? ==0')

    if len(node.indicator_types) > 1:
        logger.log('warn', 'what???')
        raise
    f.write(node.indicator_types[0].__str__() + ';' + node.description.__str__() + '\n')
