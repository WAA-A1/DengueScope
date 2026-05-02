import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold, SelectKBest, mutual_info_classif
from sklearn.decomposition import PCA


NSL_COLUMNS = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
    "root_shell","su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
    "count","srv_count","serror_rate","srv_serror_rate","rerror_rate",
    "srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate",
    "dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label","difficulty"
]


def normalize_binary_target(series):
    def convert(v):
        if isinstance(v, bytes):
            v = v.decode("utf-8", errors="ignore")
        if str(v).lower() in ["normal", "normal.", "benign", "0"]:
            return 0
        return 1
    return series.map(convert).astype(int)


def cleanup(df):
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].map(lambda x: x.decode("utf-8", "ignore") if isinstance(x, bytes) else x)
    return df


def infer_xy(df, dataset_name):

    df = cleanup(df)

    if dataset_name == "NSL-KDD":
        if df.shape[1] == len(NSL_COLUMNS):
            df.columns = NSL_COLUMNS

        y = normalize_binary_target(df["label"])
        X = df.drop(columns=["label", "difficulty"], errors="ignore")
        return X, y

    target_col = None
    for c in ["label", "attack_cat", "class", "target"]:
        if c in df.columns:
            target_col = c
            break

    if target_col is None:
        target_col = df.columns[-1]

    y = normalize_binary_target(df[target_col])
    X = df.drop(columns=[target_col], errors="ignore")

    return X, y


def split_data(X, y):
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )

    return X_train, X_val, X_test, y_train, y_val, y_test


def build_preprocessor(X):
    cat = X.select_dtypes(include=["object", "category", "bool"]).columns
    num = [c for c in X.columns if c not in cat]

    return ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                          ("sc", StandardScaler())]), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), cat),
    ])