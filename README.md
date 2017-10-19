# ais-ml
Automated Indicator Sharing - Machine Learning

# Notice
In order to parse ciscp namespace, need to edit the source code:
sudo vim /usr/local/lib/python*/dist-packages/stix/extensions/marking/ais.py
**Original**
```
Namespace('http://www.us-cert.gov/STIXMarkingStructure#AISConsentMarki    ng-2', 'AIS', 'http://www.us-cert.gov/sites/default/files/STIX_Namespace/A    IS_Bundle_Marking_1.1.1_v1.0.xsd')
```
**Modified**
```
Namespace('http://www.us-cert.gov/STIXMarkingStructure#AISConsentMarki    ng-2', 'AIS', 'http://www.us-cert.gov/sites/default/files/STIX_Namespace/A    IS_Bundle_Marking_1.1.1_v1.0.xsd'),
Namespace('http://us-cert.gov/ciscp', 'AIS_CISCP', 'http://www.us-cert    .gov/sites/default/files/STIX_Namespace/ciscp_vocab_v1.1.1.xsd')
```
**Original**
```
    nsparser.STIX_NAMESPACES.add_namespace(NAMESPACES[0])
    mixbox.namespaces.register_namespace(NAMESPACES[0])
```
**Modified**
```
    nsparser.STIX_NAMESPACES.add_namespace(NAMESPACES[0])
    mixbox.namespaces.register_namespace(NAMESPACES[0])
    
    nsparser.STIX_NAMESPACES.add_namespace(NAMESPACES[1])
    mixbox.namespaces.register_namespace(NAMESPACES[1])
```
