def indicator_iterator(stix_package):
    if stix_package.indicators is None:
        return
    for i in stix_package.indicators:
        yield i
