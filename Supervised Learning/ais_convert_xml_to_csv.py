from stix.core import STIXPackage, STIXHeader, ttps
import stix.extensions.marking.ais
from stix.indicator.indicator import *
from lxml import etree
import re
import pandas as pd
from pandas.io.json import json_normalize
from glob import glob
import json
import yaml
from tqdm import tqdm

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ais_path = '/Users/vkarthyk/Projects/AIS-ML/ais_201710'


class MultilevelJsonParser:
    """
    Gets all possible key, value pairs from a multilevel json object.
    The Json object can handle values which may be of type 'list' and parse
    them to get key, value pairs from the list as well.

    Args:
        param1 json_obj (dict): a dictionary object
    """
    def __init__(self, json_obj):
        self.loaded_json = json_obj
        self.feature_set = {}

    def get_json_data(self):
        """Open file and load the json into dictionary.

        Returns:
            param1 feature_set (dictionary): A hashmap of all keys with values
        """
        self._get_keys(self.loaded_json, '')
        return self.feature_set

    def _get_list_keys(self, val, prefix):
        """try getting the keys from the list.

        Args:
            param1 val (dictionary): dictionary or a list to extract keys from.
            param2 prefix (string): prefix string/key from parent.
        """
        for each_dict in val:
            self._get_keys(each_dict, prefix)

    def _get_keys(self, dictionary, prefix):
        """Get root key, try to get subkeys.

        Args:
            param1 val (dictionary): A dictionary to extract keys from.
            param2 prefix (string): prefix string/key from parent.

        Returns:
        """
        try:
            count = 0
            for key, val in dictionary.items():
                if key in self.feature_set:
                    self.feature_set[key].append(val)
                    
                if key == 'related_objects':
                    key = key
                else:
                    if prefix != "":
                        key = prefix+"."+key
                # check if object to be parsed is dict or list
                if isinstance(val, list):
                    self._get_list_keys(val, key)
                elif isinstance(val, dict):
                    self._get_keys(val, key)
                else:
                    # utils.log(key)
                    self.feature_set[key] = val
        except:
            pass


def get_dict(dictionary):
    for key, val in dictionary.items():
        
        # If the value is again a dict, then run the function on this value
        if isinstance(val, dict):
            get_dict(val)
        
        # If the value is in unicode, then change the value of the same key to plaintext
        elif isinstance(val, unicode):
            dictionary[key] = yaml.safe_load(json.dumps(val))  
    
        # If the value is in form of list, then extract only the element in the list
        elif isinstance(val, list):
            dictionary[key] = val[0]

    return dictionary


def parseOneStix(stixfn):
    return STIXPackage.from_xml(stixfn)


def flatten_stix(stix_package):
    if isinstance(stix_package, STIXPackage):
        json_data = json.loads(stix_package.to_json())
        multiLevelJsonParser = MultilevelJsonParser(json_data)
        final_dict = multiLevelJsonParser.get_json_data()
        df = pd.DataFrame(json_normalize(final_dict))
        return df
        
    else:
        logger.info(stix_package)


stix_packages = []
final_df = pd.DataFrame()
frames = [final_df]
count = 0

for stix_xml in tqdm(glob(ais_path+'/*.xml')):
    try:
        stix_package = parseOneStix(stix_xml)
        stix_df = flatten_stix(stix_package)
        stix_df['filename'] = stix_xml
        frames.append(stix_df)
        stix_packages.append(stix_xml)
    except:
        continue
final_df = pd.concat(frames)

final_df['filename'] = final_df['filename'].apply(lambda x: x.lstrip('/Users/vkarthyk/Projects/AIS-ML/ais_201710/'))
final_df.to_csv('large_ais_data.csv', encoding='utf-8', index=False)

with open('features.txt', 'w') as f:
    for feature in final_df.columns:
        f.write(feature+'\n')
f.close()




