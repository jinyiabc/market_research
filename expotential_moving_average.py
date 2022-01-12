import pandas as pd
import numpy as np

def expotential_moving_average(df, span):
    df = df.sort_index()
    # A[A.notnull()]
    ewm = df['close'][df['close'].notnull()].ewm(span=span, min_periods=20, adjust=False, ignore_na=False).mean()
    # return ewm.iloc[-1]
    ewm.combine_first(df['close'])
    return ewm

if __name__ == '__main__':
    df = pd.read_csv('sample.csv')
    df['custom_ema'] = expotential_moving_average(df, 20)
    # print(df)
    df.to_csv('test_compare.csv')
