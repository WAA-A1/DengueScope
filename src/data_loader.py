from pathlib import Path
import pandas as pd
import kagglehub

DATA_ROOT = Path("./external_ids_datasets")
DATA_ROOT.mkdir(exist_ok=True, parents=True)

KAGGLE_DATASETS = {
    "NSL-KDD": ["hassan06/nslkdd"],
    "UNSW-NB15": ["dhoogla/unswnb15", "mrwellsdavid/unsw-nb15", "ucimachinelearning/unsw-nb15-dataset"],
    "CIC-DDoS2019": ["dhoogla/cicddos2019"],
}

READABLE_EXTS = {".csv", ".txt", ".data", ".parquet", ".feather", ".arff"}


def download_dataset(dataset_name: str):
    dataset_dir = DATA_ROOT / dataset_name
    dataset_dir.mkdir(exist_ok=True, parents=True)

    if not any(dataset_dir.rglob("*")):
        handles = KAGGLE_DATASETS[dataset_name]
        for h in handles:
            try:
                return Path(kagglehub.dataset_download(h))
            except:
                continue
    return dataset_dir


def find_files(root: Path):
    return sorted([p for p in root.rglob("*") if p.suffix.lower() in READABLE_EXTS])


def read_table(path: Path):
    if path.suffix == ".csv":
        return pd.read_csv(path, low_memory=False)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    if path.suffix == ".feather":
        return pd.read_feather(path)
    if path.suffix in [".txt", ".data"]:
        return pd.read_csv(path, header=None)
    return pd.read_csv(path)