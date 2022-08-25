import csv
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

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


def get_dataset(DATA_DIR, FILE_NAME, header, index_col = None) :
    import preprocessing_csv as pc
    r = pc.ReadCSV(DATA_DIR, FILE_NAME, header, index_col)
    df = r.get_data()
    del r
    return df

def change_columns(df) :
    column_lst = []

    for idx, i in enumerate(range(len(df.columns))) :
        column_lst.append(f'a{idx}')

    df.columns = column_lst
    return df

def change_index_col(df) :
    index_col = np.array(range(len(df)))
    df.index = index_col

    return df

def change_index_col(df, df2) :
    index_col = np.array(range(len(df)))
    index_col2 = np.array(range((len(df)), len(df) + len(df2)))
    df.index = index_col
    df2.index = index_col2
    return df, df2

def concat_df(df1, df2) :
    new_df = pd.concat([df1, df2], ignore_index=False, axis= 0, sort=False)
    return new_df

def merge_df(df1, df2) :
    new_df = pd.merge(df1, df2, on = 'a0')
    return new_df

def concat_merge_process(DATA_DIR, df):
    r1 = UserDatasetName(); r2 = DbDatasetName()
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

# def add_song_num(df, df2) :
#     numbers = np.array(range(len(df) + len(df2)))
#
#     for i in range(len(numbers)) :
#         if i < len(df) :
#             df['song_number'] = i
#         else :
#             df2['song_number'] =
def get_songnames(DATA_DIR, SAVE_DIR):
    r1 = UserDatasetName()
    r2 = DbDatasetName()
    user_df_names = r1.get_name()
    db_df_names = r2.get_name()
    user_df = get_dataset(DATA_DIR, user_df_names[0], None)
    db_df = get_dataset(SAVE_DIR, db_df_names[0], None)

    user_songnames = user_df[0]
    db_songnames = db_df[0]

    return user_songnames, db_songnames
def concat_padding_df(DATA_DIR, SAVE_DIR, df) :
    r1 = UserDatasetName()
    r2 = DbDatasetName()
    user_df_names = r1.get_name()
    db_df_names = r2.get_name()

    tmp = df

    for i in range(len(db_df_names)) :
        user_df = get_dataset(DATA_DIR, user_df_names[i], None, 0)
        db_df = get_dataset(SAVE_DIR, db_df_names[i], None, 0)

        db_df, user_df = change_index_col(db_df, user_df)
        db_df, user_df = db_df.to_numpy().flatten(), user_df.to_numpy().flatten()
        db_df, user_df = pd.DataFrame(db_df), pd.DataFrame(user_df)
        feature_df = concat_df(db_df, user_df)

        if i == 1 :
            df = concat_df(tmp, feature_df)
        elif i > 1 :
            df = concat_df(df, feature_df)

        tmp = feature_df
    df = df.fillna(0)
    return df
    #
if __name__ == '__main__' :
    # macos = / , windows = \\
    # 5168
    # filename, index_number 제외
    DATA_DIR = './data/'
    SAVE_DIR = './db_data/'
    df = pd.DataFrame({'A': [1, 2],
                       'B': [3, 4]}, index=[1, 2])
    # df = concat_merge_process(DATA_DIR, df)


    # padding test
    # ============
    df = concat_padding_df(DATA_DIR, SAVE_DIR, df)
    user_songnames, db_songnames = get_songnames(DATA_DIR, SAVE_DIR)
    # print(df.tail(), user_songnames, db_songnames)
    # for i in range(len(df)) :
    #     print(df[0, i])
    sim = cosine_similarity(df)
    sim_df = pd.DataFrame(sim)
    print(sim_df.head())


