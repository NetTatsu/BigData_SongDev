import pandas as pd
import numpy as np
import os
import os.path
from glob import glob


class Test():
    def __init__(self):
        self.lst = []

    def set_lst(self):
        for i in range(10):
            self.lst.append(i)

    def get_lst(self):
        return self.lst

    def print_lst(self):
        print(self.lst)


class Test1(Test):
    def __init__(self):
        Test.__init__(self)


if __name__ == '__main__':
    t1 = Test()
    t1.set_lst()
    t1.print_lst()
    t2 = Test1()
    t2.print_lst()
