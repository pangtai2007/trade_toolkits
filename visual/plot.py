import datetime
from dateutil.parser import parse
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz


class CandlestickPlot:

    def __init__(self, market_file, trade_file):

        self.market_file = market_file
        self.trade_file = trade_file

    def plot(self):

        print(self.market_file)
        ohlc_data = pd.read_csv(self.market_file, sep = ',', parse_dates = True, index_col = ['time'])
        trade_data = pd.read_csv(self.trade_file, sep = ',', index_col = ['time'])

        print(ohlc_data)

        ohlc_data = ohlc_data.reset_index()
        trade_data = trade_data.reset_index()
        timezone = "Etc/GMT+8"
        ohlc_data['time'] = ohlc_data['time'].apply(lambda x: mdates.date2num(datetime.datetime.fromtimestamp(int(x // 1000000000)).replace(tzinfo = pytz.timezone(timezone))))
        trade_data['time'] = trade_data['time'].apply(lambda x: mdates.date2num(parse(x).replace(tzinfo = pytz.timezone(timezone))))


        start_time = mdates.date2num(parse("2017-07-13 21:00:00+08:00").replace(tzinfo = pytz.timezone(timezone)))
        end_time = mdates.date2num(parse("2017-07-14 09:00:00+08:00").replace(tzinfo = pytz.timezone(timezone)))

        trade_data = trade_data[trade_data["time"] < end_time]
        trade_data = trade_data[trade_data["time"] >= start_time]

        ohlc_data = ohlc_data[ohlc_data["time"] < end_time]
        ohlc_data = ohlc_data[ohlc_data["time"] >= start_time]

        ohlc_data = ohlc_data[["time", "open", "high", "low", "close"]]

        print(trade_data)
        print(ohlc_data)

        #plot
        plt.close('all')
        fig = plt.figure()
        ax = plt.subplot2grid((1,1), (0,0))
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("EURUSD")
        # width should in terms of fraction of day, here i choose width of 0.25 min
        candlestick_ohlc(ax, ohlc_data.values, width = 0.5/(24*60), colorup='#53c156', colordown='#ff1717')
        for index, trade in trade_data.iterrows():
            if trade["direction"] == "BULL":
                direction = "^"
            else:
                direction = "v"
            plt.plot(trade["time"], trade["price"], direction)
        plt.show()
