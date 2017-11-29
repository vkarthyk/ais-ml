import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import torch
from torch.autograd import Variable
from common.Logger import Logger
import utils
from models.OneTargetClassifier import OneTargetClassifier
from models.CNN1d import CNN1d
from abc import ABCMeta, abstractmethod, abstractproperty

class NNLearningBase:
    __metaclass__ = ABCMeta

    # @abstractproperty
    # def model(self):
    #     pass
    #
    # @abstractproperty
    # def loss_fn(self):
    #     pass
    #
    # @abstractproperty
    # def optimizer(self):
    #     pass
    #
    # @abstractproperty
    # def x(self):
    #     pass
    #
    # @abstractproperty
    # def y(self):
    #     pass

    @abstractmethod
    def model_build(self, **kwargs):
        pass

    @abstractmethod
    def data_build(self):
        pass

    @abstractmethod
    def df_to_tensor(self, df):
        pass

    @abstractmethod
    def learning_rate_update(self):
        pass

    @abstractmethod
    def feature_sanitize(self, feature):
        pass

    @abstractmethod
    def target_sanitize(self, target):
        pass

    @abstractmethod
    def test_result_combine(self, this_test_result, total_test_result):
        pass

    @abstractmethod
    def test_result_display(self, test_result):
        pass

    @abstractmethod
    def pred_result_combine(self, this_pred_result, total_pred_result):
        pass

    @abstractmethod
    def pred_result_display(self, pred_result):
        pass

    def __init__(self):
        self.logger = Logger(self)
        self.required = ['features', 'targets', 'learning_rate']
        self.checkbox = {}
        self.is_model_built = False
        self.is_data_built = False
        self.is_lr_changed = False
        for r in self.required:
            self.checkbox[r] = False

    def __check_requirements(self):
        for r in self.required:
            if not self.checkbox[r]:
                self.logger.err(r, 'not set yet.')
                return False
        return True

    def _set_features(self, features):
        self.x_raw = features
        self.checkbox['features'] = True
        self.is_data_built = False

    def _set_targets(self, df):
        self.y_raw = df
        self.checkbox['targets'] = True
        self.is_data_built = False

    def _set_learning_rate(self, lr): # learning rate
        if not hasattr(self, 'lr') or lr is not self.lr:
            self.is_lr_changed = True
        self.lr = lr
        self.checkbox['learning_rate'] = True

    def _build(self):
        if not self.__check_requirements():
            raise

        if not self.is_data_built:
            self.data_build()
        if not self.is_model_built:
            self.model_build()
            self.is_model_built = True
        if self.is_lr_changed:
            self.learning_rate_update()
            self.is_lr_changed = False


    def _learn(self, steps):
        if not self.is_model_built or not self.is_data_built or self.is_lr_changed:
            self._build()

        for t in range(steps):
            y_pred = self.model(self.x)
            # self.logger.dbg('y pred', y_pred)
            # self.logger.dbg('y', self.y)
            # self.logger.dbg('target size', self.y.size())

            loss = self.loss_fn(y_pred, self.y)

            if t%100 == 0:
                self.logger.info('step #'+str(t) + ', loss =', loss.data[0])

            self.optimizer.zero_grad()

            loss.backward()

            self.optimizer.step()

    def _save_model(self, path):
        self.model.save(path)

    def _load_model(self, path, **kwargs):
        if not self.is_model_built:
            self.model_build(**kwargs)
        self.model.load(path)
        self.is_model_built = True

    def _pred(self, x_df, y_df=None, data='confusion_matrix', format='tensor'):
        assert isinstance(x_df, pd.DataFrame)
        if y_df is not None: assert isinstance(y_df, pd.DataFrame)
        x_tensor = utils.get_tensor(x_df)

        y_tensor = self.df_to_tensor(y_df)

        y_pred_prob = self.model(Variable(x_tensor))

        # y_pred = x_tensor.mm(w1).clamp(min=0).mm(w2)
        if data == 'loss':
            loss = self.loss_fn(y_pred_prob, Variable(y_tensor))
            result = loss.data[0]
            return result
        elif data == 'pred':
            data_tensor = y_pred_prob.data
        else:  # data == 'confusion_matrix':
            y_pred, total_type_num = utils.max_ix(y_pred_prob.data)
            # total_type_num = len(self.ix_to_label)
            data_tensor = utils.confusion_matrix(y_pred, y_tensor, total_type_num)

        if format == 'df':
            result = pd.DataFrame(data_tensor.numpy())
        elif format == 'np':
            result = data_tensor.numpy()
        else:  # format == 'tensor':
            result = data_tensor
        return result
