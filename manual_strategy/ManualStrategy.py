

import pandas as pd
import datetime as dt
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


from util import get_data
from marketsimcode import compute_portvals

class ManualStrategy(object):
    def __init__(self):
        pass

    def testPolicy(self, symbol, sd, ed, sv=100000):
        ## this policy is like this: buy when the price will go up the next day, sell when the price will do down the next day
        # get price data
        dates = pd.date_range(sd, ed)
        prices_all = get_data([symbol], dates, addSPY=True, colname='Adj Close')
        prices = prices_all[symbol]  # only portfolio symbols

        position = np.sign(prices_diff.shift(-1)) * 1000
        trades = position.diff()
        trades.iloc[0] = position[0]
        trades.iloc[-1] = 0
        trades.columns = 'Trades'


        # buy and sell happens when the difference change direction
        df_trades = pd.DataFrame(data=trades.values, index = trades.index, columns = ['Trades'])

        return df_trades


def plot_manual_strategy():

    ms = ManualStrategy()

    # in sample
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    # dates = pd.date_range(start_date, end_date)
    symbol = 'JPM'

    df_trades = ms.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv = 100000)

    df_orders = df_trades.copy()

    df_orders = df_orders.loc[(df_orders.Trades != 0)]

    #df_orders = df_trades[['Trades']][df_trades['Trades'] != 0]

    df_orders['Symbol'] = symbol
    df_orders['Order'] = np.where(df_orders['Trades']>0, 'BUY', 'SELL')
    df_orders['Shares'] = np.abs(df_orders['Trades'])

    port_vals = compute_portvals(df_orders, start_val=100000, commission=0.0, impact=0.0)

    benchmark_orders = pd.DataFrame(data={'Symbol': ["JPM","JPM"], 'Order': ["BUY","BUY"],'Shares': [1000,0]},index={df_trades.index.min(),df_trades.index.max()})

    #benchmark_orders.loc[benchmark_orders.index[1], 'Shares'] = 0

    benchmark_vals = compute_portvals(benchmark_orders, start_val=100000, commission=0.0, impact=0.0)

    normed_port = port_vals / port_vals.ix[0]
    normed_bench = benchmark_vals / benchmark_vals.ix[0]


    """fig = plt.figure(figsize=(12,6.5))
    ax1 = fig.add_subplot(111)
    normed_port.plot(ax=ax1, color='red', lw=2)
    normed_bench.plot(ax=ax1, color='green', lw=1.2)
    ax1.set_ylabel('Normalized Portfolio Value')
    ax1.set_xlabel('Date')
    plt.grid(True)

    plt.legend()
    plt.title('Theoretically Optimal Strategy (%s)' % symbol)
    #plt.show()
    plt.savefig('04_TOS.png')
    """

    plt.figure(figsize=(12,6.5))
    plt.plot(normed_port, label="Portfolio", color='red', lw=2)
    plt.plot(normed_bench, label="Benchmark",color='green', lw=1.2)

    plt.xlabel('Date')
    plt.ylabel('Normalized Value')
    plt.legend()
    plt.grid(True)
    plt.title('Theoretically Optimal Strategy (%s)' % symbol)
    plt.savefig('04_TOS.png')
    plt.close()





if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    plot_optimal_strategy()
