import torch.nn as nn
import torch.nn.functional as F
import torch

class OneTargetClassifier(nn.Module):

    def __init__(self, D_in, T_out): # T_out: number of types of target values
        super(OneTargetClassifier, self).__init__()
        self.linear = nn.Linear(D_in, T_out)

    def forward(self, x):
        return F.log_softmax(self.linear(x))

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))