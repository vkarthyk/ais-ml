import parseStixXml as parserUtils
from stix.core import STIXPackage,STIXHeader
import yaml
from stix.indicator.indicator import *

XML_FILE_NAME = '/root/ais/ais/ais_disclosable.xml'

def printStixPackageDetailsWithWalk(stix_package):
    assert isinstance(stix_package, STIXPackage)
    for whatever in stix_package.walk():
        print '-----tpye----',type(whatever)
        print whatever
    print 'after walk'

def printStixPackageDetailsWithEnum(stix_package):
    print 'len: i', len(stix_package.indicators)
    print stix_package.id_
    print stix_package.idref
    print stix_package.timestamp
    print stix_package.stix_header.title
    print stix_package.stix_header.description
    print stix_package.stix_header.package_intents[0]
    print stix_package.stix_header.handling.marking[0].controlled_structure
    print stix_package.stix_header.handling.marking[0].marking_structures[0]
    print stix_package.stix_header.handling.marking[0].marking_structures[0].color
    print stix_package.stix_header.information_source.time.produced_time.to_dict()

def useless():
    for i in stix_package.indicators:
        assert isinstance(i, Indicator)
        print i.to_dict()
        coinex=i.composite_indicator_expression
        assert isinstance(coinex, CompositeIndicatorExpression)
        print 'operator:',coinex.operator
        print coinex.to_json()
        print coinex.indicator
        print len(coinex.indicator)
        for ii in coinex.indicator:
            print ii.idref
        break

def extractHeaderFeatures(stix_package):
    assert isinstance(stix_package, STIXPackage)
    stix_header = stix_package.stix_header
    assert isinstance(stix_header, STIXHeader)
    hfeatures={'----TYPE----':'----HEADER----'}
    hfeatures['Title']=stix_header.title
    hfeatures['Package Intents']= stix_header.package_intents[0].__str__()
    hfeatures['Description']=stix_header.description.__str__()
    hfeatures['Marking Color']=';'.join(ms.color for ms in stix_header.handling.marking[0].marking_structures)
    hfeatures['Information Source Time']=stix_header.information_source.time.produced_time.to_dict()
    return hfeatures

def pprintDict(d):
    # print '--------------'
    print yaml.dump(d, allow_unicode=True, default_flow_style=False)

def extractIndicatorsFeatures(stix_package):
    indicator_features_list = []
    assert isinstance(stix_package, STIXPackage)
    for i in stix_package.indicators:
        if not i.composite_indicator_expression:
            indicator_feature={}
            indicator_feature['----TYPE----']='----INDICATOR----'
            indicator_feature['ID'] = i.id_
            indicator_feature['Description'] = i.description.__str__()
            indicator_feature['Type'] = i.indicator_types[0].__str__()
            indicator_features_list.append(indicator_feature)
    return indicator_features_list




def getIndicatorFieldsList(indicator_list):
    pass

stix_list=parserUtils.xmlFileName2StixPackageObjList(XML_FILE_NAME)
# parseOneStix('/tmp/stix1.xml')
# printStixPackageDetails(stix_list[0])
# printStixPackageDetailsWithWalk(stix_list[0])
for ind,stix_package in enumerate(stix_list):
    print '========== the #',ind,'stix package ==========='
    head_features = extractHeaderFeatures(stix_package)
    pprintDict(head_features)
    indicator_features_list = extractIndicatorsFeatures(stix_package)
    for indicator_feature in indicator_features_list:
        pprintDict(indicator_feature)