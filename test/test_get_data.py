import os
import shutil

from helper import get_data
from helper.wind import read_wind_excel, read_wind_csv


def test_get_data():
    get_data.get_module_1('survivorship_free')
    assert os.path.isdir("survivorship_free")
    shutil.rmtree("survivorship_free")
    os.remove("survivorship_free.zip")

def test_read_wind_excel():
    dir = os.path.join('..', '../quant/_notebooks')
    df = read_wind_excel(f'{dir}/csi300.xlsx', '2015-6-18', '2018-6-18',
                                 skiprows=0,   # false
                                 header=0,)    # start from 1st line
    print(df)
    pass

def test_read_wind_csv():
    dir = os.path.join('..', '../quant/CSI/wind_csi300')
    df = read_wind_csv(f'{dir}/600602.SH.CSV', '2015-6-18', '2018-6-18',
                                skiprows=0,
                                 header=0,)
    print(df)
    pass

def test_get_data1():
    get_data.get_module_3('300072.csv')
    # assert os.path.isdir("survivorship_free")
    # shutil.rmtree("survivorship_free")
    # os.remove("survivorship_free.zip")