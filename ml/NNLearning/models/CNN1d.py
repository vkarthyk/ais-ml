import torch.nn as nn
import torch.nn.functional as F
import torch

class CNN1d(nn.Module):

    def __init__(self, D_in, T_out): # T_out: number of types of target values
        super(CNN1d, self).__init__()
        if D_in == 0:
            return
        self.conv1 = nn.Conv1d(1, 5, 5, stride=1)
        self.conv2 = nn.Conv1d(5, 10, 5, stride=1)
        self.pool = nn.MaxPool1d(5)
        # self.fc1 = nn.Linear(10*(D_in-8), (10*(D_in-8)-T_out)*2/3+T_out)
        # self.fc2 = nn.Linear((10*(D_in-8)-T_out)*2/3+T_out, (10*(D_in-8)-T_out)/3+T_out)
        # self.fc3 = nn.Linear((10*(D_in-8)-T_out)/3+T_out, T_out)
        width = ((D_in-4)/5-4)/5
        self.fc1 = nn.Linear(10*width, (10*width-T_out)/2+T_out)
        self.fc2 = nn.Linear((10*width-T_out)/2+T_out, T_out)


    def forward(self, x):
        x = x.view(x.size()[0], 1, -1)
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        x = self.fc2(x)
        return x

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))

    def load_from_gpu(self, path):
        self.load_state_dict(torch.load(path, map_location=lambda storage, loc: storage))
