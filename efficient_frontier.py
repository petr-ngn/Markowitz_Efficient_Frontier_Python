#%%
import pandas as pd
import numpy as np
from itertools import permutations
import matplotlib.pyplot as plt

asset_prices = pd.read_csv('asset_prices.csv')

def portfolios_generator(assets_prices_df):
    
    def asset_metrics(assets_prices):
    
        log_returns = {}
        exp_returns = []

        for asset in assets_prices.columns:

            asset_metric = {}
            log_return = np.log(assets_prices[asset]/assets_prices[asset].shift(1))
            log_returns[asset] = log_return
            exp_returns.append(log_return.mean()*250)
 
        stacked_logs = np.array([logs[1:] for k,logs in log_returns.items()])

        covar_matrix = np.cov(stacked_logs)*250

        return (exp_returns, covar_matrix)


    exp_returns, covar_matrix = asset_metrics(assets_prices_df)


    def weights_combinations(assets_prices):

        combinations =  np.array(list(permutations(range(0,101),len(assets_prices.columns))))

        weights_list = [combo for combo in combinations if np.sum(combo) == 100]

        weights_df = pd.DataFrame(weights_list, columns = [assets_prices.columns]) / 100

        return weights_df


    weights_df = weights_combinations(assets_prices_df)


    def portfolio_returns(row, exp_returns):

        weights = row.to_numpy()

        return np.dot(weights, exp_returns)


    port_er = pd.DataFrame(weights_df.apply(lambda row: portfolio_returns(row, exp_returns), axis = 1), columns = ['port_er'])


    def portfolio_risks(row, covar_matrix):

        weights = row.to_numpy()

        portf_std = np.sqrt(np.dot(weights.T,np.dot(covar_matrix, weights)))

        return portf_std


    port_std = pd.DataFrame(weights_df.apply(lambda row: portfolio_risks(row, covar_matrix), axis = 1), columns = ['port_std'])

    efficient_portfolios = pd.concat((weights_df, port_er, port_std), axis = 1)


    def sharpe_ratio(row):

        sharpe = row['port_er']/row['port_std']

        return sharpe


    efficient_portfolios['sharpe'] = efficient_portfolios.apply(sharpe_ratio, axis = 1)
    

    return efficient_portfolios

def portfolios_plot(efficient_portfolios):

    plt.figure(figsize = (17,10))

    plt.scatter(efficient_portfolios['port_std'],efficient_portfolios['port_er'], c = efficient_portfolios['sharpe'])
    plt.colorbar(label = 'Sharpe Ratio')

    plt.ylabel('Portfolio Volatility')
    plt.xlabel('Portfolio Expected Return')

    plt.scatter(efficient_portfolios['port_std'][efficient_portfolios['sharpe']== efficient_portfolios['sharpe'].max()],
                efficient_portfolios['port_er'][efficient_portfolios['sharpe']== efficient_portfolios['sharpe'].max()],
                c = 'red', s = 50)
            
    plt.show()


portfolios = portfolios_generator(asset_prices)

portfolios_plot(portfolios)
# %%
