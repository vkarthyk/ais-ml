from common.Logger import logger

def intent(stix_package):

    if len(stix_package.stix_header.package_intents)>1:
        logger('warn', 'the length of intents is longer than 1')

    return stix_package.stix_header.package_intents[0].value
    # return len(stix_package.stix_header.package_intents)

def indicator_type(indicator):
    return indicator.indicator_types[0].__str__() if len(indicator.indicator_types) > 0 else ''

def indicator_description(indicator):
    return indicator.description.__str__() if indicator.description is not None else ''
