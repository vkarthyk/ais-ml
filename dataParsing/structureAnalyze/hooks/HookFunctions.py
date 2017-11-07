from settings import os, DATA_DIR, BIG_DATA_DIR
from stix.indicator.indicator import Indicator
from stix.incident import Incident
from common.Logger import Logger
from collections import MutableSequence
from stix.core import STIXPackage
from mixbox.typedlist import TypedList

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

def __is_indicator(node):
    if not isinstance(node, Indicator):
        return False

    if len(node.indicator_types) == 0:
        # logger.log('warn', 'what??? ==0')
        return False
    return True

def indicator_type_desc(node):
    if not __is_indicator(node):
        return

    if len(node.indicator_types) > 1:
        logger.log('warn', 'what???')
        raise

    f.write(node.indicator_types[0].__str__() + ';' + node.description.__str__() + '\n')

def test_field(node):
    if not isinstance(node, STIXPackage) or node.incidents is None:
        return
    print node.incidents

