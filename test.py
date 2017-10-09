import visual.plot
import environments.market_db as md
import pandas as pd

if __name__ == '__main__':

    candlestick_plot = visual.plot.CandlestickPlot("data/kline_20170714.csv", "data/trader.csv")
    candlestick_plot.plot()

