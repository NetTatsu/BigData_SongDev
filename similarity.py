import csv
import numpy as np
import pandas as pd

class DatasetName() :
    def __init__ (self, df_name) :
        self.df_name = df_name

    def __del__(self):
        print('DatasetName DELETE')

    def get_name(self):
        return self.df_name
class UserDatasetName(DatasetName) :
    def __init__(self):
        user_df_name = ['Test_SongData.csv','Test_Bandwidth_SongData.csv', 'Test_Centroid_SongData.csv',
                        'Test_Fourier_SongData.csv', 'Test_Harm_SongData.csv',
                        'Test_Mfcc_SongData.csv', 'Test_Perc_SongData.csv',
                        'Test_RMS_SongData.csv', 'Test_Rolloff_SongData.csv',
                        ]
        DatasetName.__init__(self, user_df_name)

    def __del__(self):
        print('UserDatasetName DELETE')

class DbDatasetName(DatasetName) :
    def __init__(self):
        db_df_name = ['SongData.csv', 'Bandwidth_SongData.csv', 'Centroid_SongData.csv',
                      'Fourier_SongData.csv', 'Harm_SongData.csv',
                      'Mfcc_SongData.csv', 'Perc_SongData.csv',
                      'RMS_SongData.csv', 'Rolloff_SongData.csv',
                      ]
        DatasetName.__init__(self, db_df_name)

    def __del__(self):
        print('DbDatasetName DELETE')


def get_dataset(DATA_DIR, FILE_NAME, header) :
    import preprocessing_csv as pc
    r = pc.ReadCSV(DATA_DIR, FILE_NAME, header)
    df = r.get_data()
    del r
    return df

def change_columns(df) :
    column_lst = []

    for idx, i in enumerate(range(len(df.columns))) :
        column_lst.append(f'a{idx}')

    df.columns = column_lst
    return df


def concat_df(df1, df2) :
    new_df = pd.concat([df1, df2], ignore_index=True)
    return new_df

def merge_df(df1, df2) :
    new_df = pd.merge(df1, df2, on = 'a0')
    return new_df

if __name__ == '__main__' :
    # macos = / , windows = \\
    DATA_DIR = './data/'

    r1 = UserDatasetName(); r2 = DbDatasetName()

    user_df_names = r1.get_name()
    db_df_names = r2.get_name()

    # SongData.csv로 데이터 병합 테스트
    user_df = get_dataset(DATA_DIR, user_df_names[0], 0)
    db_df = get_dataset(DATA_DIR, db_df_names[0], 0)
    df = concat_df(db_df, user_df)
    df = change_columns(df)
    print(df.head())
