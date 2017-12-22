from settings import os, DATA_DIR, BIG_DATA_DIR
from stix.indicator.indicator import Indicator
from stix.incident import Incident
from common.Logger import Logger
from collections import MutableSequence
from stix.core import STIXPackage
from mixbox.typedlist import TypedList
import csv

FREQUENCY_ROWS_CSV_FILE_NAME = os.path.join(DATA_DIR,'IndicatorTypeDesc.csv')

f=None
logger = Logger("hooks.HookFunctions")
tmpf = None

def __open_file():
    global f, tmpf
    tmpf = open(FREQUENCY_ROWS_CSV_FILE_NAME, 'wb')
    f = csv.writer(tmpf)

def __close_file():
    global f, tmpf
    tmpf.close()

def indicator_type_desc_start():
    __open_file()
    f.writerow(['Indicator_Type', 'Indicator_Description'])

def indicator_type_desc_end():
    __close_file()

def __is_indicator(node):
    if not isinstance(node, Indicator):
        return False

    if len(node.indicator_types) == 0:
        # logger.log('warn', 'what??? ==0')
        return False
    return True

def indicator_type_desc(node):
    if not __is_indicator(node):
        return False

    if len(node.indicator_types) > 1:
        logger.log('warn', 'what???')
        raise

    rowlist = [node.indicator_types[0].__str__(), node.description.__str__()]

    try:
        f.writerow(rowlist)
    except Exception, err:
        try:
            f.writerow([s.encode('utf-8') for s in rowlist])
        except Exception, err1:
            f.writerow([s.encode('latin-1', 'replace') for s in rowlist])
            # tmp=row[5820:5838]
            # tmp1=tmp.encode('utf-32')
            # logger.log('info', row[5820:5836])
            # logger.log('info', tmp1)
            # logger.log('info', tmp)
    return True

def test_field(node):
    if not isinstance(node, STIXPackage) or node.incidents is None:
        return
    print node.incidents

