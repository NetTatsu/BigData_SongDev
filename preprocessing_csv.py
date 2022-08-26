import csv
from email import header
from re import S
from tkinter.font import names
import numpy as np
import pandas as pd

# pickle로 변경후 사용 안함
class CSV():
    def __init__(self, df):
        self.df = df

    def __del__(self):
        print('CSV DELETE')

    def get_data(self):
        return self.df


class ReadCSV(CSV):
    def __init__(self, DATA_DIR, FILE_NAME, header, index_col = None):
        self.DATA_DIR = DATA_DIR
        self.FILE_NAME = FILE_NAME
        CSV.__init__(self, pd.read_csv(
            f'{self.DATA_DIR}{self.FILE_NAME}', header=header, sep=',', index_col= index_col, encoding='utf-8-sig'))

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

