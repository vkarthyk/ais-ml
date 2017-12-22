from stix.core import STIXPackage
# import xml.etree.ElementTree as ET
# from xml.dom import minidom
from stix.extensions.marking.ais import AISMarkingStructure, AISConsentType
from lxml import etree
from common.Logger import logger
import glob
import os


def stixFileNameInDirectory(dir_name, stopafter=-1, onlyuse=None):
    path = os.path.join(dir_name,"*.xml")
    logger.log('info', 'Reading files in', dir_name)
    for ind, filename in enumerate(glob.glob(path)):
        if onlyuse is not None:
            if filename == onlyuse:
                yield filename
                return
            continue
        if stopafter is not -1 and ind > stopafter:
            break

        yield filename
    logger.log('info','===== Parse xml file done =====')


def xmlFileName2EnumStixFileName(fn, stopafter=-1):
    stixfn='/tmp/stixtmp.xml'
    tree = etree.parse(fn)
    root = tree.getroot()
    for ind, child in enumerate(root):
        if stopafter is not -1 and ind > stopafter:
            break
        etree.ElementTree(child).write(stixfn, pretty_print=True)
        yield stixfn
    logger.log('info','===== Parse xml file done =====')

def xmlFileName2StixPackageObjList(fn):
    stix_list=[]
    i = 0
    for stixfn in xmlFileName2EnumStixFileName(fn):
        i+=1
        stix_list.append(stixFileName2StixPackageObj(stixfn))
        # if i is 20:
        #     break
    print '===== stixParser done'
    return stix_list

def stixFileName2StixPackageObj(stixfn):
    logger.log('info', stixfn)
    return STIXPackage.from_xml(stixfn)

