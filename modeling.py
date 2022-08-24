import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPool2D, GlobalAveragePooling2D, LeakyReLU, AveragePooling2D
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical


def split_xy(dataset, target, time_steps, y_column):  # target = 원본
    x, y = list(), list()
    for i in range(len(dataset)):
        x_end_number = i + time_steps
        y_end_number = x_end_number + y_column
        if y_end_number > len(dataset):
            break
        x_tmp = dataset[i: x_end_number, :]
        y_tmp = target[x_end_number: y_end_number, 3]
        x.append(x_tmp)
        y.append(y_tmp)
    return np.array(x), np.array(y)


if __name__ == '__main__':

    # seed = 3
    # np.random.seed(seed)
    # tf.random.set_seed(seed)
    # df = pd.read_csv('C:/Python/data/SongData.csv',
    #                  header=None, sep=',', encoding='utf-8-sig')
    # df = df.dropna()
    # df_input = df.iloc[:, 1:]
    # df_target = df.iloc[:, 0]
    # # le = LabelEncoder()
    # # labeled_df_target = to_categorical(le.fit_transform(df_target))
    # # print(labeled_df_target)
    # x, y = split_xy(df_input, df_target, 11, 1)
    # print(x.shape(), y.shape())
    # # train_input, test_input, train_target, test_target = train_test_split(
    # #     df_input, df_target, test_size=0.2, random_state=seed)

    # # print(train_target.shape, train_input.shape)
    # # model = Sequential()
    # # model.add()
    import preprocessing_csv as pc
    DIR = '.\\data\\'
    c = pc.ReadCSV(DIR, 'SongData.csv', None)
    df = c.get_data()
    # df_input = df.values[:, 1:].astype('float')
    # df_target = df.values[:, 0]
    # print(df_input.shape(), df_target.shape())
