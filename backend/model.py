import torch
import torch.nn as nn
import torch.nn.functional as F

class DQNNetwork(nn.Model):
    """
    Пример простой fully-connected сети для Q-функции:
    Вход: вектор состояния (3 фичи: [кол-во непроверенных клеток, кол-во оставшихся палуб, id_текущей_стратегии])
    Выход: Q-значения для 5 действий (остаться, 4 паттерна).
    """
    def __init__(self, state_dim = 3, action_dim = 5):
        super(DQNNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_dim)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x