import csv
from operator import index
from unicodedata import name
import numpy as np
import pandas as pd
import pickle
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import scale


class DatasetName():
    def __init__(self, df_name):
        self.df_name = df_name

    def __del__(self):
        print('DatasetName DELETE')

    def get_name(self):
        return self.df_name


class UserDatasetName(DatasetName):
    def __init__(self):
        user_df_name = ['Test_SongData.pickle', 'Test_Bandwidth_SongData.pickle', 'Test_Centroid_SongData.pickle',

                        'Test_Mfcc_SongData.pickle',
                        'Test_Rolloff_SongData.pickle'
                        ]
        # rms, tempo 제외
        # 'Test_RMS_SongData.pickle', 'Test_Fourier_SongData.pickle', 'Test_Harm_SongData.pickle', 'Test_Perc_SongData.pickle'
        DatasetName.__init__(self, user_df_name)

    def __del__(self):
        print('UserDatasetName DELETE')


class DbDatasetName(DatasetName):
    def __init__(self):
        db_df_name = ['SongData.pickle', 'Bandwidth_SongData.pickle', 'Centroid_SongData.pickle',

                      'Mfcc_SongData.pickle',
                      'Rolloff_SongData.pickle'
                      ]
        DatasetName.__init__(self, db_df_name)
        # 'RMS_SongData.pickle', 'Fourier_SongData.pickle', 'Harm_SongData.pickle', 'Perc_SongData.pickle'

    def __del__(self):
        print('DbDatasetName DELETE')


def get_dataset(DATA_DIR, FILE_NAME):
    with open(f'{DATA_DIR}{FILE_NAME}', 'rb') as f:
        df = pickle.load(f)
    return df


def change_columns(df):
    column_lst = []

    for idx, i in enumerate(range(len(df.columns))):
        column_lst.append(f'a{idx}')

    df.columns = column_lst
    return df


def change_index_col(df):
    index_col = np.array(range(len(df)))
    df.index = index_col

    return df


# def change_index_col(df, df2):
#     index_col = np.array(range(len(df)))
#     index_col2 = np.array(range((len(df)), len(df) + len(df2)))
#     df.index = index_col
#     df2.index = index_col2
#     return df, df2


def concat_df(df1, df2):
    new_df = pd.concat([df1, df2], ignore_index=False, axis=0, sort=False)
    return new_df


def merge_df(df1, df2):
    new_df = pd.merge(df1, df2, on='a0')
    return new_df


def concat_merge_process(DATA_DIR, df):
    r1 = UserDatasetName()
    r2 = DbDatasetName()
    user_df_names = r1.get_name()
    db_df_names = r2.get_name()

    tmp = df

    for i in range(len(db_df_names)):
        user_df = get_dataset(DATA_DIR, user_df_names[i], 0)
        db_df = get_dataset(DATA_DIR, db_df_names[i], 0)
        concated_df = concat_df(db_df, user_df)
        changed_df = change_columns(concated_df)

        if i == 0:
            tmp = changed_df
        else:
            if i == 1:
                df = merge_df(tmp, changed_df)
            else:
                df = merge_df(df, changed_df)
                df = change_columns(df)
    return df


def get_songnames(DATA_DIR, SAVE_DIR):
    r1 = UserDatasetName()
    r2 = DbDatasetName()
    user_df_names = r1.get_name()
    db_df_names = r2.get_name()
    user_df = get_dataset(DATA_DIR, user_df_names[0])
    db_df = get_dataset(SAVE_DIR, db_df_names[0])
    user_df_names = []
    db_df_names = []
    # print(user_df.keys())
    for i in range(len(user_df.keys())):
        user_df_names.append((user_df.get(f'{i}')[0]))

    for i in range(len(db_df.keys())):
        db_df_names.append((db_df.get(f'{i}')[0]))

    # print(user_df_names)
    return user_df_names, db_df_names


def preprocessing_df(DATA_DIR, SAVE_DIR, df):
    r1 = UserDatasetName()
    r2 = DbDatasetName()
    user_df_names = r1.get_name()
    db_df_names = r2.get_name()

    tmp = df

    for i in range(len(db_df_names)):
        user_df = get_dataset(DATA_DIR, user_df_names[i])
        db_df = get_dataset(SAVE_DIR, db_df_names[i])
        user_df = pd.DataFrame(user_df).transpose()
        db_df = pd.DataFrame(db_df).transpose()
        feature_df = concat_df(db_df, user_df)
        feature_df = feature_df.drop(0, axis=1)
        temp = []
        if i != 0:
            feature_df = feature_df.to_numpy().flatten()
            feature_df.astype(object)
            for j in range(len(feature_df)):
                temp.append(feature_df[j].flatten())
            feature_df = pd.DataFrame(temp).transpose()
        feature_df = change_index_col(feature_df)

        if i == 1:
            df = concat_df(tmp, feature_df)
        elif i > 1:
            df = concat_df(df, feature_df)

        tmp = feature_df

    df = df.fillna(0)
    return df


def find_similarity_song(sim_df, index_col, n=5):
    sim_series = sim_df[index_col].sort_values(ascending=False)
    sim_series = sim_series.drop(index_col)
    return sim_series.head(n).to_frame()


def get_similarity_result(DATA_DIR, SAVE_DIR):
    result = []
    df = pd.DataFrame({'A': [1, 2],
                       'B': [3, 4]}, index=[1, 2])
    df = preprocessing_df(DATA_DIR, SAVE_DIR, df)
    user_songnames, db_songnames = get_songnames(DATA_DIR, SAVE_DIR)
    df_scaled = sklearn.preprocessing.scale(df)
    df = pd.DataFrame(df_scaled, columns=df.columns)

    similarity = cosine_similarity(df)
    sim_df = pd.DataFrame(similarity)

    for idx, i in enumerate(range(len(user_songnames))):
        index_col = len(db_songnames) + idx
        for j in range(len(user_songnames)):
            lst = find_similarity_song(sim_df, index_col)

    return lst


if __name__ == '__main__' :
    DATA_DIR = './data/'
    SAVE_DIR = './db_data/'

    # dictionary index_col rename
    # Generator
    #