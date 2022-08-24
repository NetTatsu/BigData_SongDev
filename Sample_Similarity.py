from bdb import effective
from fileinput import filename
import os
import os.path
from unicodedata import name
from unittest import TestProgram
from pydub import AudioSegment
import librosa
import librosa.display
# import IPython.display as dp
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn import preprocessing
import pandas as pd
import csv
from sklearn.model_selection import train_test_split
# from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
# import glob


# df_insert = pd.read_csv('.\SongData\InsertData.csv', index_col='filename')
# df_dataset = pd.read_csv('.\SongData\SongData.csv', index_col='filename')

# df_30 = pd.concat([df_dataset, df_insert])

# filenames = df_30['filename2']
# df_30 = df_30.drop(columns=['length', 'filename2'])


# df_30_scaled = sklearn.preprocessing.scale(df_30)  #평균 0 , 표준편차 1

# df_30 = pd.DataFrame(df_30_scaled, columns=df_30.columns)

# df_30.head()

# from sklearn.metrics.pairwise import cosine_similarity
# similarity = cosine_similarity(df_30)

# sim_df = pd.DataFrame(similarity, index = filenames.index, columns = filenames.index)

# sim_df.head()


def find_similar_songs(name, df, n=5):

    series = df[name].sort_values(ascending=False)

    series = series.drop(name)

    return series.head(n).to_frame()


def get_similar(name):
    df_insert = pd.read_csv('.\SongData\InsertData.csv', index_col='filename')
    df_dataset = pd.read_csv('.\SongData\SongData.csv', index_col='filename')

    df_30 = pd.concat([df_dataset, df_insert])
    filenames = df_30['filename2']
    df_30 = df_30.drop(columns=['length', 'filename2'])

    df_30_scaled = sklearn.preprocessing.scale(df_30)  # 평균 0 , 표준편차 1

    df_30 = pd.DataFrame(df_30_scaled, columns=df_30.columns)

    df_30.head()

    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity(df_30)

    sim_df = pd.DataFrame(
        similarity, index=filenames.index, columns=filenames.index)

    sim_df.head()
    result = find_similar_songs(name, sim_df)
    print(result)

# if __name__ == '__main__' :
    # get_similar()
