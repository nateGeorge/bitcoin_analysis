# from here:
# https://medium.com/burgercrypto-com/forecasting-bitcoin-returns-with-prophet-in-python-part-ii-b3e44b3de95

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas_profiling as pp
import matplotlib.pyplot as plt
from fbprophet import Prophet

m = Prophet()

df_fullset = pd.read_csv('https://raw.githubusercontent.com/MarcelBurger/Bitcoin-Data-Analysis/master/bitcoindataset.csv')
# save a local copy in case original is lost
df_fullset.to_csv('bitcoindataset.csv')

df_model = pd.DataFrame()
df_model['y'] = df_fullset['Ret']
df_model['ds'] = df_fullset['timestamp']

#Adding Regressors
df_model['S2F'] = df_fullset['S2F']
df_model['S2F'] = df_model['S2F'].fillna(method='bfill')
df_model['S2F'] = pd.to_numeric(df_model['S2F'], errors='coerce')
m.add_regressor('S2F')


#Creating future data for S2F
prediction_interval = 360
blocks_per_day = 1440/9.45
last_blockheight = df_fullset['blockheight'].tail(1).values[0]
df_futuredata = pd.DataFrame(index=range(prediction_interval), columns=range(1))
df_futuredata['blocksperday'] = pd.to_numeric(blocks_per_day)
df_futuredata['blockheight'] = pd.to_numeric(last_blockheight) + df_futuredata['blocksperday'].cumsum(axis=0)
df_futuredata['supply'] = df_futuredata['blockheight'].apply(lambda x: 50*(210000*(1-math.pow(0.5, math.floor(x/210000)))/(1-0.5)+math.pow(0.5, math.floor(x/210000))*math.fmod(x,210000)))
df_futuredata['S2F'] = df_futuredata['supply'].shift(1)/(365*(df_futuredata['supply'] - df_futuredata['supply'].shift(1)))
df_futuredata['S2F'] = df_futuredata['S2F'].fillna(method='bfill')

# Prepare model and future time series
m.fit(df_model)

future = m.make_future_dataframe(periods=prediction_interval, freq='D')
len_future = len(future.index)
len_dfmodel = len(df_model.index)
future['S2F'] = np.nan

for i in range(0, len_dfmodel):
    future['S2F'].iloc[i] = df_model['S2F'].iloc[i]

for i in range(0, len_future - len_dfmodel - 1):
    future['S2F'].iloc[len_dfmodel + i] = df_futuredata['S2F'].iloc[i]


future['S2F'].bfill(inplace=True)
future['S2F'].ffill(inplace=True)
future['S2F'] = future['S2F'].astype(float)

# Needed to solve an issue with dataformat
pd.plotting.register_matplotlib_converters()

#Forecast with Prophet
forecast = m.predict(future)

fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)

plt.show()