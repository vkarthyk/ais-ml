import math

'''
Please check IpAdressScoreDemo for more info.

This one demos the aggressive mode.
Implement run_aggr() and output_columns_aggr to support aggressive mode

@output_columns_aggr: output_columns in aggressive mode
@run_aggr(args): optional, this will be called if run_level=1 in config.py, otherwise run(args)

you can name your args and return values as you like

MAKE SURE:
 #of output_columns == #of returen value (#of means number of)
'''

input_columns=['indicators.kill_chain_phases.kill_chain_phases.0.phase_id']
output_columns=['id_len']
output_columns_aggr=['id_len', 'id_len_plus_1', 'id_len_square']

def __is_nan(cell):
    return type(cell) is float and math.isnan(cell)

def run(id):
    id_len = len(id) if not __is_nan(id) else 0
    return id_len

def run_aggr(id):
    id_len = len(id) if not __is_nan(id) else 0
    id_len_2 = len(id)+2 if not __is_nan(id) else 0
    id_len_sq = len(id)*len(id) if not __is_nan(id) else 0
    return id_len, id_len_2, id_len_sq

# get_from_stix_package: this is to extract input_features from stix_package, like the input_columns up there.
# currently we **DON'T NEED** to implement this function,
# this is for further use, so just leave it there or remove this function.
# when we finish the scoring and have a ML model,
# we can implement this function to score incoming stix packages rather than the csv file.
def get_from_stix_package(stix_package):
    pass
