import visual.plott
import environments.market_db as md
import pandas as pd

if __name__ == '__main__':
    #candlestick_plot = visual.plot.CandlestickPlot("data/14_incontinuous.csv", "data/trader.csv")
    #candlestick_plot.plot()
    candlestick_plot = visual.plott.CandlestickPlot1("data/14_incontinuous.csv", "data/trader.csv")
    candlestick_plot.plot1()

