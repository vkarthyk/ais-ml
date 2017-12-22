import pickle

import yaml

from common.Logger import logger


def pprintDict(dictionary):
    # print '--------------'
    logger.log('rst',yaml.dump(dictionary, allow_unicode=True, default_flow_style=False))

def saveObjToFile(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def loadObjFrFile(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)