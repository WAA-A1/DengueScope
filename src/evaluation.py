import numpy as np
from sklearn.metrics import *
from scipy.stats import wilcoxon, friedmanchisquare


def metrics(y_true, probs, t=0.5):
    pred = (probs >= t).astype(int)

    return {
        "Accuracy": accuracy_score(y_true, pred),
        "Precision": precision_score(y_true, pred, zero_division=0),
        "Recall": recall_score(y_true, pred),
        "F1": f1_score(y_true, pred),
        "ROC-AUC": roc_auc_score(y_true, probs)
    }


def best_threshold(y, p):
    best_t, best_f = 0.5, 0
    for t in np.linspace(0.1, 0.9, 50):
        f = f1_score(y, (p >= t).astype(int))
        if f > best_f:
            best_f, best_t = f, t
    return best_t


def wilcoxon_test(x, y):
    return wilcoxon(x, y)