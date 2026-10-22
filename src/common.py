"""Même jeu v1 et même découpage externe pour tous les essais."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)
TRACKING_URI = os.environ.get('MLFLOW_TRACKING_URI', 'http://127.0.0.1:5001')


def split_data():
    df = pd.read_csv(ROOT / 'data/transactions.csv')
    assert len(df) == 5000 and int(df.fraude.sum()) == 568
    return train_test_split(df.drop(columns='fraude'), df['fraude'],
                            test_size=0.25, random_state=42)


def setup_tracking():
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment('tp4-automl')


def trace_tags():
    commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'],
                                     cwd=ROOT, text=True).strip()
    return {'auteurs': 'Zakaria Abdelbaki; Amine Khabot; Ismail Lahlou; Rayane Hafidi',
            'groupe': 'AI-G6', 'commit': commit, 'donnees': 'transactions v1',
            'donnees_sha256': hashlib.sha256((ROOT/'data/transactions.csv').read_bytes()).hexdigest(),
            'split': 'train_test_split(test_size=0.25, random_state=42)'}


def save_json(filename, value):
    (REPORTS/filename).write_text(json.dumps(value, indent=2, ensure_ascii=False,
                                           default=str), encoding='utf-8')
