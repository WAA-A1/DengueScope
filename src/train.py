from data_loader import download_dataset, read_table, find_files
from preprocessing import infer_xy, split_data, build_preprocessor
from model import get_xgb, get_lgbm, TabularMLP
from evaluation import metrics, best_threshold


def run(dataset_name):

    root = download_dataset(dataset_name)
    files = find_files(root)

    dfs = []
    for f in files:
        dfs.append(read_table(f))

    df = dfs[0]

    X, y = infer_xy(df, dataset_name)

    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)

    model = get_xgb(1)

    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:,1]

    return metrics(y_test, probs)


if __name__ == "__main__":
    print(run("NSL-KDD"))