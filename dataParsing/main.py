from stixParseWorker import StixParseWorker
from parseStixXml import *
from printUtils import pprintDict

XML_FILE_NAME = '/root/ais/ais/ais_disclosable.xml'

worker = StixParseWorker()
for ind, stix_fn in enumerate(xmlFileName2EnumStixFileName(XML_FILE_NAME)):
    # if ind is not 9:
    #     continue
    if ind > 19:
        break
    print '#'+str(ind)
    stix_package = stixFileName2StixPackageObj(stix_fn)
    worker.consumeStix(stix_package)

stix_fields_list_of_list = worker.getStixFieldsList()

stix_fields_dict_of_list = worker.getStixFieldsDict()

pprintDict(stix_fields_dict_of_list)