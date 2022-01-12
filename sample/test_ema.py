import pandas as pd

df = pd.read_csv('intc_data.txt', parse_dates=['Date'], index_col=['Date'])
df['backward_ewm'] = df['Close'].ewm(span=20,min_periods=0,adjust=False,ignore_na=False).mean()
df = df.sort_index()
df['ewm'] = df['Close'].ewm(span=20,min_periods=0,adjust=False,ignore_na=False).mean()
print(df[['ewm', 'backward_ewm']].tail())

"""
https://stackoverflow.com/questions/48775841/pandas-ema-not-matching-the-stocks-ema
"""