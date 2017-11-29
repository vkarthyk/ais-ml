import pandas as pd
import matplotlib.pylab as plt
from common.Logger import Logger
from ml.NNLearning import utils
import csv
import time

class IndicatorStructureNN:
    def __init__(self, max_row_per_time=1000):
        self.logger = Logger(self)
        self.max_row_per_time = max_row_per_time
        self.time_start = time.time()

    def set_learning_class(self, NN, **args):
        self.nn = NN(args)

    def __set_data_sets(self, featurepath, targetpath='', targetcol='', featurecollist=[], featurecolblacklist=[], rowlist=[]):
        self.logger.info('setting data set')
        self.logger.info(rowlist)
        # Read data
        self.featurepath = featurepath
        self.targetpath = targetpath
        self.targetcol = targetcol
        self.featurecollist = featurecollist
        self.featurecolblacklist = featurecolblacklist
        self.rowlist = rowlist

        # adjust columns
        if len(featurecollist) is 0:
            featurecollist = self.__read_header(featurepath)
        featurecollist = list(set(featurecollist)-set(featurecolblacklist))

        self.df_feature_itr = pd.read_csv(self.featurepath, usecols=featurecollist, iterator=True, chunksize=self.max_row_per_time)
        if len(targetpath) is not 0:
            self.df_target_itr = pd.read_csv(self.targetpath, usecols=[targetcol], iterator=True, chunksize=self.max_row_per_time)

        self.logger.info('setting data finished.')

    def __read_header(self, csvpath):
        with open(csvpath, 'rb') as f:
            csvin = csv.reader(f)
            headers = next(csvin, [])
        return headers

    def __df_feature_target_iterator(self, is_need_target=True):
        # for chunk_feature, chunk_target in zip(self.df_feature_itr, self.df_target_itr):
        for i, chunk_feature in enumerate(self.df_feature_itr):
            if is_need_target:
                chunk_target = next(self.df_target_itr)

            if len(self.rowlist) > 0:
                if self.rowlist[-1] < i * self.max_row_per_time:
                    return

            chunk_feature_clean = self.nn.feature_sanitize(chunk_feature)

            if len(self.rowlist) > 0:
                real_index_list = list(set(chunk_feature_clean.index.values)&set(self.rowlist))
                if len(real_index_list) is 0:
                    continue
                if is_need_target:
                    chunk_target_clean = self.nn.target_sanitize(chunk_target)
                    yield chunk_feature_clean.loc[real_index_list], chunk_target_clean.loc[real_index_list]
                else:
                    yield chunk_feature_clean.loc[real_index_list]
            else:
                if is_need_target:
                    chunk_target_clean = self.nn.target_sanitize(chunk_target)
                    yield chunk_feature_clean, chunk_target_clean
                else:
                    yield chunk_feature_clean

    def train(self, lr, steps, featurepath, targetpath, targetcol, featurecollist=[], featurecolblacklist=[], rowlist=[]):
        self.__set_data_sets(featurepath, targetpath, targetcol, featurecollist, featurecolblacklist, rowlist)

        self.logger.info('start training data with lr='+str(lr), 'steps='+str(steps))
        self.nn._set_learning_rate(lr)

        # time_start = time.time()
        for i, (df_feature, df_target) in enumerate(self.__df_feature_target_iterator()):

            self.logger.info('trainning data chunk #'+str(i*self.max_row_per_time)+'-'+str((i+1)*self.max_row_per_time-1))
            # Set up
            self.nn._set_features(df_feature)
            self.nn._set_targets(df_target)

            self.nn._build()
            self.nn._learn(steps)
            # utils.print_time_consuming(time.time() - time_start)
            utils.print_time_consumed(time.time() - self.time_start)

        # self.logger.info('trainning data finished.')
        self.logger.info('finished training data with lr='+str(lr), 'steps='+str(steps))
        utils.print_time_consumed(time.time() - self.time_start)


    def test(self, featurepath, targetpath, targetcol, featurecollist=[], featurecolblacklist=[], rowlist=[]):
        self.logger.info('testing data.')
        self.__set_data_sets(featurepath, targetpath, targetcol, featurecollist, featurecolblacklist, rowlist)
        # confusion_matrix = []
        total_test_resut = []
        for df_test_feature, df_test_target in self.__df_feature_target_iterator():
            this_test_result = self.nn._pred(df_test_feature, df_test_target, data='confusion_matrix', format='tensor')
            total_test_resut = self.nn.test_result_combine(this_test_result, total_test_resut)
        self.nn.test_result_display(total_test_resut)

        return total_test_resut


    def predict(self, featurepath, featurecollist=[], featurecolblacklist=[], rowlist=[]):
        self.logger.info('testing data.')
        self.__set_data_sets(featurepath, featurecollist=featurecollist, featurecolblacklist=featurecolblacklist, rowlist=rowlist)
        total_pred_resut = []
        for df_test_feature in self.__df_feature_target_iterator(is_need_target=False):
            this_pred_result = self.nn._pred(df_test_feature, data='pred', format='df')
            total_pred_resut = self.nn.pred_result_combine(this_pred_result, total_pred_resut)
        self.nn.pred_result_display(total_pred_resut)

        return total_pred_resut

    def predict_list(self, data_list):
        pass

    def save(self, path):
        self.nn._save_model(path)
        self.logger.info('saved to', path)

    def load(self, path, **kwargs):
        self.nn._load_model(path, **kwargs)
        self.logger.info('load from', path)

'''
select_model(model)
set_data_sets(featurepath, featurecollist=[0,1], featurecolblacklist=[], rowlist=[], targetpath, targetcol)
train(lr, step)
train(lr, step)

save(path)
load(path)
train(lr, step)

test(featurepath, featurecollist=[0,1], featurecolblacklist=[], rowlist=[], targetpath, targetcol)

predict(featurepath, featurecollist=[0,1], featurecolblacklist=[], rowli)
'''