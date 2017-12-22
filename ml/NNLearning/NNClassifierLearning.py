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


class NNClassifierLearning(NNLearningBase):

    def model_build(self):
        if isinstance(self.x_raw, pd.DataFrame):
            self.x_tensor = utils.get_tensor(self.x_raw)
            self.logger.dbg('type xtensor', type(self.x_tensor))
        elif isinstance(self.x_raw, torch.Tensor):
            self.x_tensor = self.x_raw
        self.x = Variable(self.x_tensor, requires_grad=False)
        self.D_in = len(self.x_tensor[0])

        self.y_tensor = utils.get_tensor(self.y_raw, 'long')
        self.y = Variable(self.y_tensor, requires_grad=False).squeeze(1)
        self.D_out = len(self.y_tensor[0])

        self.T_out, _ = np.unique(self.y_tensor.numpy(), return_inverse=True)

        self.model = OneTargetClassifier(self.D_in, len(self.T_out))
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr)
        self.loss_fn = torch.nn.NLLLoss()

    def df_to_tensor(self, df):
        return utils.get_tensor(df, 'long').squeeze(1)

