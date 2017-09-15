from stix.core import STIXPackage
# import xml.etree.ElementTree as ET
# from xml.dom import minidom
from stix.extensions.marking.ais import AISMarkingStructure, AISConsentType

from lxml import etree

def xmlFileName2EnumStixFileName(fn):
    stixfn='/tmp/stixtmp.xml'
    tree = etree.parse(fn)
    root = tree.getroot()
    for child in root:
        etree.ElementTree(child).write(stixfn, pretty_print=True)
        yield stixfn
    print '===== Parse xml file done'

def xmlFileName2StixPackageObjList(fn):
    stix_list=[]
    for stixfn in xmlFileName2EnumStixFileName(fn):
        stix_list.append(stixFileName2StixPackageObj(stixfn))
        break
    print '===== stixParser done'
    return stix_list

def stixFileName2StixPackageObj(stixfn):
    return STIXPackage.from_xml(stixfn)

