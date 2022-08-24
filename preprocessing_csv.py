import csv
from email import header
from re import S
from tkinter.font import names
import numpy as np
import pandas as pd


class CSV():
    def __init__(self, df):
        self.df = df

    def __del__(self):
        print('CSV DELETE')

    def get_data(self):
        return self.df


class ReadCSV(CSV):
    def __init__(self, DATA_DIR, FILE_NAME, header):
        self.DATA_DIR = DATA_DIR
        self.FILE_NAME = FILE_NAME
        CSV.__init__(self, pd.read_csv(
            f'{self.DATA_DIR}{self.FILE_NAME}', header=header, sep=',', encoding='utf-8-sig'))

    def __del__(self):
        print('ReadCSV DELETE')


class SaveCSV(CSV):
    def __init__(self, DATA_DIR, FILE_NAME, df):
        CSV.__init__(self, df)
        self.DATA_DIR = DATA_DIR
        self.FILE_NAME = FILE_NAME

    def __del__(self):
        print('SaveCSV DELETE')

    def save_data(self):
        self.df.to_csv(f'{self.DATA_DIR}{self.FILE_NAME}',
                       sep=',', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    CSV_DIR = '.\\data\\'
    c = ReadCSV(CSV_DIR, 'MFCC_NEW_SongData.csv', None)
    df = c.get_data()
    df = df.dropna()
    pointer = 0
    names = []
    print(df)
    filename = df.iloc[pointer, 0]
    for idx, data in enumerate(range(len(df))):
        if filename != df.iloc[idx, 0]:
            pointer = idx
        filename = df.iloc[pointer, 0]
        names.append(pointer)
    df['song_start'] = names
    s = SaveCSV(CSV_DIR, 'MFCC_NEW_SongData.csv', df).save_data()
