import random
import sys
import os
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from sklearn.preprocessing import quantile_transform
from scipy.stats import zscore
from sklearn.model_selection import StratifiedKFold


def download_data():
    # Download data from GitHub repository
    os.system('wget -nc -q https://github.com/henryRDlab/ElectricityTheftDetection/raw/master/data.z01')
    os.system('wget -nc -q https://github.com/henryRDlab/ElectricityTheftDetection/raw/master/data.z02')
    os.system('wget -nc -q https://github.com/henryRDlab/ElectricityTheftDetection/raw/master/data.zip')

    # Unzip downloaded data
    os.system('cat data.z01 data.z02 data.zip > data_compress.zip')
    os.system('unzip -n -q data_compress')


def get_dataset(filepath):
    """## Saving "flags" """

    df_raw = pd.read_csv(filepath, index_col=0)
    flags = df_raw.FLAG.copy()
    df_raw.drop(['FLAG'], axis=1, inplace=True)

    """## Sorting"""

    df_raw = df_raw.T.copy()
    df_raw.index = pd.to_datetime(df_raw.index)
    df_raw.sort_index(inplace=True, axis=0)
    df_raw = df_raw.T.copy()
    df_raw['FLAG'] = flags
    return df_raw


"""# Processing dataset"""


def get_processed_dataset(filepath):
    df_raw = get_dataset(filepath)
    flags = df_raw['FLAG']

    df_raw.drop(['FLAG'], axis=1, inplace=True)

    """## Quantile transform"""
    # df_raw = pd.read_csv(filepath)
    # df_raw.drop(['2016-11-01'], axis=1, inplace=True)
    # flags = pd.read_csv('data/label.csv')

    quantile = quantile_transform(df_raw.values, n_quantiles=10, random_state=0, copy=True,
                                  output_distribution='uniform')
    df__ = pd.DataFrame(data=quantile, columns=df_raw.columns, index=df_raw.index)
    df__['flags'] = flags
    # print(df__.head(10))

    return df__.iloc[:, 5:]


def GetDataSet(filepath):
    data = pd.read_csv(filepath)
    label = data.iloc[:, -1].to_numpy()
    data.drop('1029', axis=1, inplace=True)
    data = data.to_numpy()

    return data, label


def getPredictData(filepath):
    data = pd.read_csv(filepath)
    print(data)
    print(len(data))
    user_id = data.iloc[:, 0].to_numpy()
    user_area = data.iloc[:, 1].to_numpy()
    user_court = data.iloc[:, 2].to_numpy()
    label = data.iloc[:, -1].to_numpy()
    data.drop(['0', '1', '2', '1032'], axis=1, inplace=True)
    data = data.to_numpy()

    return user_id, user_area, user_court, data, label


def Split_data(filepath, n):
    data = pd.read_csv(filepath)
    numbers1 = []
    while len(numbers1) < n:
        i = random.randint(0, 38134)
        if i not in numbers1:
            numbers1.append(i)
    data1 = data.iloc[numbers1, :]
    data1.to_csv('data/data_train_{}.csv'.format(n), index=False)
    num = []
    while len(num) < 14000:
        i = random.randint(0, 38134)
        if i not in numbers1 and i not in num:
            num.append(i)
    data2 = data.iloc[num, :]
    data2.to_csv('data/data_train_{}.csv'.format(14000), index=False)
    data3 = data.drop(numbers1 + num)
    data3.to_csv('data/data_train_16135.csv', index=False)
    pass
