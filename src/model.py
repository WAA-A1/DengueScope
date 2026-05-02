import torch
import torch.nn as nn
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


class TabularMLP(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 2),
        )

    def forward(self, x):
        return self.net(x)


def get_xgb(spw):
    return XGBClassifier(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        scale_pos_weight=spw,
        tree_method="hist"
    )


def get_lgbm(spw):
    return LGBMClassifier(
        n_estimators=400,
        learning_rate=0.05,
        scale_pos_weight=spw
    )