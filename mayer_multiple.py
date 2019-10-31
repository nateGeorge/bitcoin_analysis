import os
import sys
sys.path.append('../')

import pytz
import pandas as pd
import cufflinks as cf
cf.go_offline()

from bitfinex_ohlc_import import load_candle_data as lcd


def load_data():
    df = lcd.load_data(pair='btcusd', candle_size='1m')
    df_1d = lcd.resample_data(df, '1D')

    col = 'close'
    df_1d['mayer_multiple'] = df_1d[col] / df_1d[col].rolling(window=200).mean()

    return df, df_1d


if __name__=="__main__":
    # quick and  dirty histogram
    df_1d['mayer_multiple'].iplot(kind='hist', asPlot=True)
        


    # more polished histogram
    todays_date = pd.datetime.now(tz=pytz.timezone('US/Eastern'))
    filename = os.path.join(os.getcwd(),'current_mayer_multiple_{}.png'.format(todays_date.strftime('%m-%d-%Y')))
    todays_date = todays_date.strftime('%B %d, %Y')

    latest_mm = df_1d.iloc[-1]['mayer_multiple']
    avg_mm = df_1d['mayer_multiple'].mean()
    med_mm = df_1d['mayer_multiple'].median()

    fig = df_1d['mayer_multiple'].iplot(kind='hist',
                            vline=[{'x':latest_mm, 'color':'orange', 'width':5},
                                    {'x':avg_mm, 'color':'red', 'width':5},
                                    {'x':med_mm, 'color':'red', 'width':5}],
                            color='blue',
                            title=todays_date,
                            xTitle='BTC Mayer Multiple',
                            yTitle='binned frequency',
                            width=3,
                            bins=100,
                            asFigure=True)
    fig.update_layout(
        annotations=[dict(
            showarrow=False,
            x=latest_mm,
            y=270,
            text="current Mayer Multiple",
            xanchor="right",
            xshift=-1
        ),
        dict(
            showarrow=False,
            x=avg_mm,
            y=250,
            text="average Mayer Multiple",
            xanchor="left",
            xshift=1
        ),
        dict(
            showarrow=False,
            x=med_mm,
            y=270,
            text="median Mayer Multiple",
            xanchor="left",
            xshift=1
        )]
    )
    fig.write_image(filename, scale=3)

    # todo: plot z-score of MM over time
    # add 'mm has been above this value x% of time' to plot subtitle