import math

'''
Only need to care about 3 things:
@input_columns: what columns of csv file you want as input,
@output_columns: the name of your output columns,
@run(args): main function

@run_aggr(args): optional, this will be called if run_level=1 in config.py, otherwise run(args)

you can name your args and return values as you like

MAKE SURE:
 #of input_columns == #of args
 #of output_columns == #of returen value (#of means number of)
'''

input_columns=['indicators.observable.object.properties.address_value.value.0', 'stix_header.description.0']
output_columns=['ip_len', 'description_len']

def run(ip, description):
    # just an example, you can extract date from description and check ip on some website
    # then give it a score or some scores
    ip_len = len(ip) if not __is_nan(ip) else 0
    des_len = len(description) if not __is_nan(description) else 0

    return ip_len, des_len




def __is_nan(cell):
    return type(cell) is float and math.isnan(cell)

# get_from_stix_package: this is to extract input_features from stix_package, like the input_columns up there.
# currently we **DON'T NEED** to implement this function,
# this is for further use, so just leave it there or remove this function.
# when we finish the scoring and have a ML model,
# we can implement this function to score incoming stix packages rather than the csv file.
def get_from_stix_package(stix_package):
    pass
