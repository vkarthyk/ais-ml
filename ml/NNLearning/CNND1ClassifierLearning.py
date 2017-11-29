import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import torch
from torch.autograd import Variable
from common.Logger import Logger
import utils
from models.OneTargetClassifier import OneTargetClassifier
from models.CNN1d import CNN1d
from NNLearningBase import NNLearningBase


class CNND1ClassifierLearning(NNLearningBase):
    def __init__(self, args):
        super(CNND1ClassifierLearning, self).__init__()
        self.target_num = args['target_num']
        self.ix_to_label = []

    def data_build(self):
        if isinstance(self.x_raw, pd.DataFrame):
            self.x_tensor = utils.get_tensor(self.x_raw)
        elif isinstance(self.x_raw, torch.Tensor):
            self.x_tensor = self.x_raw
        else:
            self.logger.dbg('type x_raw', type(self.x_raw))
        self.x = Variable(self.x_tensor, requires_grad=False)
        self.D_in = len(self.x_tensor[0])

        self.y_tensor = utils.get_tensor(self.y_raw, 'long')
        self.y = Variable(self.y_tensor, requires_grad=False).squeeze(1)
        self.D_out = len(self.y_tensor[0])

    # def set_target_num(self, target_num):
    #     self.target_num = target_num
    #     self.checkbox['target_num'] = True

    def learning_rate_update(self):
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr, momentum=0.9)

    def model_build(self, **kwargs):
        # self.D_out = len(self.y_tensor[0])
        # self.T_out, _ = np.unique(self.y_tensor.numpy(), return_inverse=True)
        if kwargs.has_key('D_in') and kwargs.has_key('target_num'):
            self.model = CNN1d(kwargs['D_in'], kwargs['target_num'])
        else:
            self.model = CNN1d(self.D_in, self.target_num)
        # self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr, momentum=0.9)
        # self._update_learning_rate(lr)
        self.loss_fn = torch.nn.CrossEntropyLoss()

    def df_to_tensor(self, df):
        return utils.get_tensor(df, 'long').squeeze(1)

    def feature_sanitize(self, feature):
        feature = feature.fillna('None')
        return feature

    def target_sanitize(self, target):
        target = target.fillna('None')
        target, self.ix_to_label = utils.get_series_ids(target, self.ix_to_label)
        self.logger.dbg('ix to label', self.ix_to_label)
        return target

    def test_result_combine(self, this_test_result, total_test_result):
        confusion_matrix = utils.list_element_addition_2d(total_test_result, this_test_result)
        return confusion_matrix

    def test_result_display(self, test_result):
        self.logger.rst('confusion matrix:')
        utils.pprint_ix_to_label(self.ix_to_label)
        utils.pprint_confusion_matrix(test_result, indents=5, len_ix_to_label=len(self.ix_to_label))
        # utils.pprint_confusion_matrix(test_result, indents=5)
        self.logger.info('testing data finished.')

    def pred_result_combine(self, this_pred_result, total_pred_result):
        total_pred_result.append(this_pred_result)
        return total_pred_result

    def pred_result_display(self, pred_result):
        self.logger.rst('Predicted Target Values:')
        self.logger.rst(pred_result)
