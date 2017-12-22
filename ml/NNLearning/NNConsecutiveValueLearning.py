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
from abc import abstractmethod

class NNConsecutiveValueLearning(NNLearningBase):
    def __init__(self):
        super(NNConsecutiveValueLearning, self).__init__()
        self.required.append('cell_num')

    def set_cell_num(self, n):
        self.H = n # hidden dimension number
        self.checkbox['cell_num'] = True

    def model_build(self):
        if isinstance(self.x_raw, pd.DataFrame):
            self.x_tensor = utils.get_tensor(self.x_raw)
            self.logger.dbg('type xtensor', type(self.x_tensor))
        elif isinstance(self.x_raw, torch.Tensor):
            self.x_tensor = self.x_raw
        self.x = Variable(self.x_tensor, requires_grad=False)
        self.D_in = len(self.x_tensor[0])

        self.y_tensor = utils.get_tensor(self.y_raw)
        self.y = Variable(self.y_tensor, requires_grad=False)
        self.D_out = len(self.y_tensor[0])

        self.model = torch.nn.Sequential(
            torch.nn.Linear(self.D_in, self.H),
            torch.nn.ReLU(),
            torch.nn.Linear(self.H, self.D_out),
        )
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

        self.loss_fn = torch.nn.MSELoss(size_average=False)

    def df_to_tensor(self, df):
        return utils.get_tensor(df)
