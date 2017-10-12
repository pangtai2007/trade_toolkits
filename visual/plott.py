# -- coding: utf-8 --
#现在incontinuous里面是不连续的数据

import datetime
from dateutil.parser import parse
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz


class CandlestickPlot1:

    def __init__(self, market_file, trade_file):

        self.market_file = market_file
        self.trade_file = trade_file

    def plot1(self):

        #print(self.market_file)
        ohlc_data = pd.read_csv(self.market_file, sep = ',', parse_dates = True, index_col = ['time'])
        trade_data = pd.read_csv(self.trade_file, sep = ',', index_col = ['time'])

        #print(ohlc_data)

        ohlc_data = ohlc_data.reset_index()
        #print(ohlc_data)
        trade_data = trade_data.reset_index()
        timezone = "Etc/GMT+8"
        #print(ohlc_data['time'][100])
        #print(int(ohlc_data['time'][100] // 1000000000))
        #for i in range(0,374):
        #    print(datetime.datetime.fromtimestamp(int(ohlc_data['time'][i] // 1000000000)).replace(
        #        tzinfo=pytz.timezone(timezone)))
        print(datetime.datetime.fromtimestamp(int(ohlc_data['time'][0] // 1000000000)))
        print(datetime.datetime.fromtimestamp(int(ohlc_data['time'][0] // 1000000000)).replace(
                    tzinfo=pytz.timezone(timezone)))
        ohlc_data['time'] = ohlc_data['time'].apply(lambda x: mdates.date2num(datetime.datetime.fromtimestamp(int(x // 1000000000)).replace(tzinfo = pytz.timezone(timezone))))
        #print(ohlc_data['time'])
        trade_data['time'] = trade_data['time'].apply(lambda x: mdates.date2num(parse(x).replace(tzinfo = pytz.timezone(timezone))))


        start_time = mdates.date2num(parse("2017-07-13 21:00:00+08:00").replace(tzinfo = pytz.timezone(timezone)))
        #print(start_time)
        #print(parse("2017-07-13 21:00:00+08:00"))
        #print(parse("2017-07-13 21:00:00+08:00").replace(tzinfo = pytz.timezone(timezone)))
        end_time = mdates.date2num(parse("2017-07-14 09:00:00+08:00").replace(tzinfo = pytz.timezone(timezone)))

        trade_data = trade_data[trade_data["time"] < end_time]
        #print(trade_data)
        trade_data = trade_data[trade_data["time"] >= start_time]

        ohlc_data = ohlc_data[ohlc_data["time"] < end_time]
        ohlc_data = ohlc_data[ohlc_data["time"] >= start_time]

        #print(ohlc_data)
        ohlc_data = ohlc_data[["time", "open", "high", "low", "close"]]
        #ohlc_data有不连续的数据，希望用一些指针来分离他
        #print(trade_data)
        #print(ohlc_data)
        #print('llll',ohlc_data.shape[0])
        count_incontinuous=[]
        print('kkkk',ohlc_data['time'][1]-ohlc_data['time'][0])
        #print('kkkk', ohlc_data['time'][2] - ohlc_data['time'][1])
        for i in range(1, ohlc_data.shape[0]):
            #print(i, ' ', ohlc_data['time'][i]-ohlc_data['time'][i-1])
            if ohlc_data['time'][i]-ohlc_data['time'][i-1]>=0.0007:   #incontinuous
                count_incontinuous.append(i)
                print("++")

        #print('hhhh',count_incontinuous)
        len_count_incontinuous = len(count_incontinuous)

        #plot
        # 分开绘制，应该画到不同的子图去
        plt.close('all')
        #fig = plt.figure()
        #ax = plt.subplot2grid((1,1), (0,0))
        # 要建立len_count_incontinuous+1个子图
        # 应该考虑如何设置每个子图的格式
        fig, ax_l = plt.subplots(1, 3, sharey=True)
        for ax in ax_l:
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))
            #ax.xticks(rotation=45)
            #plt.xticks(rotation=45)
            #plt.xlabel("Date")
            #plt.ylabel("Price")
            #plt.title("EURUSD")

        #plt.xticks(rotation=45)
        #plt.xlabel("Date")
        #plt.ylabel("Price")
        #plt.title("EURUSD")
        # width should in terms of fraction of day, here i choose width of 0.25 min
        #test
        p1=0
        p2=0
        d = .015  # how big to make the diagonal lines in axes coordinates
        for i in range(0,len_count_incontinuous):
            p1=p2
            p2=count_incontinuous[i]
            #print("ppp ",p1,' ', p2)
            kwargs = dict(transform=ax_l[i].transAxes, color='k', clip_on=False)
            #plt.xticks(rotation=45, **kwargs)
            candlestick_ohlc(ax_l[i], ohlc_data[p1:p2].values, width=0.5 / (24 * 60), colorup='#53c156', colordown='#ff1717')
            if i==0:
                ax_l[i].spines['right'].set_visible(False)
                ax_l[i].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # top-left diagonal
                ax_l[i].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
                #ax.xaxis.tick_top()
                #ax_l[i].yaxis.tick_right()
            if i>0:
                #ax.xaxis.tick_top()
                ax_l[i].spines['right'].set_visible(False)
                ax_l[i].spines['left'].set_visible(False)
                #ax_l[i].yaxis.tick_right()
                ax_l[i].yaxis.tick_left()
                ax_l[i].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # top-left diagonal
                ax_l[i].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
                ax_l[i].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                ax_l[i].plot((- d, d), (-d, d), **kwargs)  # bottom-right diagonal



                #candlestick_ohlc(ax, ohlc_data2.values, width = 0.5/(24*60), colorup='#53c156', colordown='#ff1717')
        kwargs = dict(transform=ax_l[len_count_incontinuous].transAxes, color='k', clip_on=False)
        candlestick_ohlc(ax, ohlc_data[p2:ohlc_data.shape[0]].values, width=0.5 / (24 * 60), colorup='#53c156', colordown='#ff1717')
        #ax_l[len_count_incontinuous].spines['right'].set_visible(False)
        ax_l[len_count_incontinuous].spines['left'].set_visible(False)
        #ax.xaxis.tick_top()
        #ax_l[len_count_incontinuous].yaxis.tick_right()
        ax_l[len_count_incontinuous].yaxis.tick_left()
        ax_l[len_count_incontinuous].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
        ax_l[len_count_incontinuous].plot((- d, d), (-d, d), **kwargs)  # bottom-right diagonal
        '''
        for index, trade in trade_data.iterrows():
            if trade["direction"] == "BULL":
                direction = "^"
            else:
                direction = "v"
            plt.plot(trade["time"], trade["price"], direction)
        '''
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Price")
        #plt.title("EURUSD")
        #fig.xlabel("Date")
        fig.suptitle("EURUSD")

        plt.show()


