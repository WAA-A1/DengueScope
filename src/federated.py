import torch
import numpy as np
from model import TabularMLP


def get_params(model):
    return {k: v.detach().cpu() for k, v in model.state_dict().items()}


def set_params(model, params):
    model.load_state_dict(params)


def diff(local, global_):
    return {k: local[k] - global_[k] for k in local}


def clip(update, max_norm=1.0):
    norm = torch.norm(torch.cat([v.flatten() for v in update.values()]))
    scale = min(1.0, max_norm / (norm + 1e-12))
    return {k: v * scale for k, v in update.items()}


def noise(update, sigma):
    return {k: v + torch.randn_like(v) * sigma for k, v in update.items()}


def aggregate(updates):
    out = {}
    for k in updates[0]:
        out[k] = sum(u[k] for u in updates) / len(updates)
    return out


def train_client(model, X, y, idx):
    model.train()
    return model.state_dict()


def federated_round(global_model, clients, sigma=0.02):
    updates = []

    global_params = get_params(global_model)

    for X, y, idx in clients:
        model = TabularMLP(global_model.net[0].in_features)
        set_params(model, global_params)

        local = train_client(model, X, y, idx)

        u = diff(local, global_params)
        u = clip(u)
        u = noise(u, sigma)

        updates.append(u)

    new_params = aggregate(updates)
    set_params(global_model, new_params)

    return global_model