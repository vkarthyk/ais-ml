from settings import os, DATA_DIR, BIG_DATA_DIR
from stix.indicator.indicator import Indicator
from stix.incident import Incident
from common.Logger import Logger
from collections import MutableSequence
from stix.core import STIXPackage
from mixbox.typedlist import TypedList
from stix.common.structured_text import StructuredTextList
import csv

FREQUENCY_ROWS_CSV_FILE_NAME = os.path.join(DATA_DIR,'IndicatorTypeDesc.csv')
# INDICATOR_ALL_FIELDS_FILE_NAME = os.path.join(BIG_DATA_DIR,'IndicatorAllFields.csv')
INDICATOR_ALL_FIELDS_FILE_NAME = os.path.join(BIG_DATA_DIR,'IndicatorAllFields_2.0.csv')

tmpfilename = os.path.join(DATA_DIR,'test.csv')
tmpf = None
f=None
logger = Logger("hooks.IndicatorIterAllFieldHooks")

titles = []

delimitor = ';'

def open_file():
    global f, tmpf
    tmpf = open(tmpfilename, 'wb')
    f = csv.writer(tmpf)

# def close_file():
#     global tmpf
#     tmpf.close()

def end_of_indicator_all_fields():
    global tmpf
    tmpf.close()
    # f.write(delimitor.join(titles))
    realfw = open(INDICATOR_ALL_FIELDS_FILE_NAME, 'wb')
    realfwcsv = csv.writer(realfw)
    tmpfr = open(tmpfilename, 'rb')
    tmpfrcsv = csv.reader(tmpfr)

    realfwcsv.writerow(titles)
    for row in tmpfrcsv:
        realfwcsv.writerow(row)
    # close_file()
    realfw.close()
    tmpfr.close()

def __check_title(label):
    # logger.log('warn', label)
    if label not in titles:
        titles.append(label)
        return -1
    return titles.index(label)

def __iter_fields(cur_node, cur_title, rowlist, rowdict):
    if type(cur_node) is str or isinstance(cur_node, StructuredTextList):
        # logger.log('warn', 'BEFORE check_title', cur_node.__str__())
        # if already exist, then no need to append again
        if isinstance(cur_node, StructuredTextList) and cur_node is not None:
            content = cur_node.to_dict()
            if len(content) is 0:
                content = ''
            # logger.log('warn', content)
        else:
            content = cur_node.__str__()

        rst = __check_title(cur_title)
        if rst == -1:
            rowlist.append(content)
        else:
            rowdict[rst] = content
        return

    if hasattr(cur_node, '_fields'):
        fdict = cur_node.__dict__['_fields']
        for f in fdict:
            # if str(f) == 'Description':
                # logger.log('warn', type(f), fdict[f].__str__())
                # logger.log('warn', cur_node.description.__str__())
                # logger.log('warn', fdict[f].to_dict())
            tmp_title = cur_title + '.' + str(f)
            # if str(f) == 'id':
                # logger.log('warn', fdict[f])
                # logger.log('warn', '1111111111111', f, tmp_title)

            if (isinstance(cur_node, MutableSequence) and isinstance(fdict[f], MutableSequence)) or isinstance(fdict[f], TypedList) or isinstance(fdict[f], list):
                # if (isinstance(fdict[f], MutableSequence) or isinstance(fdict[f], TypedList)):
                for ind, item in enumerate(fdict[f]):
                    # i_label = cur_label + '['+str(ind)+']'
                    # i_label = cur_label + '[i]'
                    # i_label = self.__getListObjTreeID(cur_label, ind)
                    # self.iterField(item, i_label, self.__getTreeID(cur_node, i_label), prefix + '--')
                    # i_label = self.__getListObjTreeID(item, str(f), ind)

                    tmp_title = cur_title + '.' + str(f) + '[' + str(ind) + ']'
                    # logger.log('info', 'indicator has list')
                    __iter_fields(item, tmp_title, rowlist, rowdict)
                    # self.iterField(item, cur_label, self.__getTreeID(cur_node, cur_label), prefix + '--')

            elif fdict[f] is not None:
                __iter_fields(fdict[f], tmp_title, rowlist, rowdict)

def __is_indicator(node):
    if not isinstance(node, Indicator):
        return False


    if len(node.indicator_types) == 0:
        # logger.log('warn', 'what??? ==0')
        return False
    return True

def indicator_all_fields(node):
    if not __is_indicator(node):
        return True

    if len(node.indicator_types) > 1:
        logger.log('warn', 'what???')
        raise

    fields = node.__dict__['_fields']
    # for i in fields:
    #     if str(i) == 'Sightings':
    #         logger.log('rst',str(i), type(i),fields[i])
    if node.id_ == 'CISCP:indicator-dabd73da-5d8f-4eef-b396-6243254256b5':
        logger.log('rst', 'type', type(node.observables))

    rowlist = []
    rowdict = {}

    # for t in titles:
    #     try:
    #         tmp = t[9:]
    #         tmpl = tmp.split('.')[1:]
    #         tmp = node
    #         for i in tmpl:
    #             tmpi = i.split('[')
    #             if len(tmpi) > 1:
    #                 i = tmpi[0]
    #                 tti = tmpi[1].split(']')[0]
    #                 tmp = eval('tmp.__dict__[\'_fields\'][\''+i+'\'][\''+tti+'\']')
    #             else:
    #                 tmp = eval('tmp.__dict__[\'_fields\'][\''+i+'\']')
    #         value = eval('node'+t[9:])
            # value = tmp.__str__()
            # logger.log('warn', value)
        # except Exception, err:
        #     value = ''
            # raise err
        #
        # rowlist.append(value)

    __iter_fields(node, 'Indicator', rowlist, rowdict)

    # logger.log('warn', rowdict)
    keys = rowdict.keys()
    if len(keys) is not 0:
        for i in reversed(range(max(keys))):
            if rowdict.has_key(i):
                rowlist.insert(0, rowdict[i])
            else:
                rowlist.insert(0, '')
    # rowlist.append(node.indicator_types[0].__str__())
    # rowlist.append(node.description.__str__())
    # rowlist.append(node.description.__str__())

    # row = delimitor.join(rowlist) + '\n'

    # logger.log('info', row[:391])
    # logger.log('info', row[:392])
    # testchr1 = row[392].encode('latin-1')
    # logger.log('info', testchr1)
    # logger.log('info', row[:393])

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
    return False


