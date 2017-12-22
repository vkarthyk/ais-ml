import glob
import os
import inspect
import pandas as pd
import config
from modules import FEATURE_MODULE_DIR
from common.Logger import Logger

'''
author: xhyumiracle
'''
class FeatureBuilder:
    def __init__(self, csv_file_name):
        self.df = None
        self.new_df = pd.DataFrame()
        self.read_data(csv_file_name)
        self.logger = Logger(self)

    def read_data(self, csv_file_name):
        self.df = pd.read_csv(csv_file_name)

    def hasattributes(self, obj, attr_list, filename):
        for attr in attr_list:
            if not hasattr(obj, attr):
                self.logger.log('warn', 'module [',filename, '] doesn\'t have [', attr, '], skip.')
                return False
        return True

    def build_new_features(self):
        mod = None
        for filename in glob.glob(FEATURE_MODULE_DIR+"/*.py"):
            if mod is not None:
                del mod
                mod = None
            module_name = os.path.splitext(os.path.basename(filename))[0]

            if module_name.startswith('__'):
                continue

            if config.black_white_list_use_mode == 'disabled':
                pass
            elif config.black_white_list_use_mode == 'black':
                if module_name in config.black_list:
                    continue
            elif config.black_white_list_use_mode == 'white':
                if module_name not in config.white_list:
                    continue
            elif config.black_white_list_use_mode == 'both':
                if module_name not in config.white_list or module_name in config.black_list:
                    continue

            self.logger.log('info', 'applying module [', module_name, ']')
            mod = __import__('modules.'+module_name)
            mod = getattr(mod, module_name)

            if not self.hasattributes(mod, ['input_columns', 'output_columns', 'run'], filename):
                continue
            input_columns = mod.input_columns
            output_columns = mod.output_columns
            run = mod.run

            if config.run_level is 1 and hasattr(mod, 'run_aggr'):
                if hasattr(mod, 'output_columns_aggr'):
                    run = mod.run_aggr
                    output_columns = mod.output_columns_aggr
                else:
                    self.logger.log('warn', 'module [', module_name, '] has run_aggr() but no output_columns_aggr, downgrade to run().')

            try:
                tuple_df = self.df.apply(lambda row: run(*row[input_columns]), axis=1)
                tmp_df = tuple_df.apply(pd.Series)
                tmp_df.columns = output_columns
            except ValueError, err:
                print err
                self.logger.log('warn', 'module [', module_name, '] has incorrect columns define, skip.')
                continue

            self.new_df = pd.concat([self.new_df,tmp_df], axis=1)

    def run(self):
        self.build_new_features()

    def get_new_feature_df(self):
        return self.new_df
