#%%
#Importing relevant libraries.
import pandas as pd
import numpy as np
from itertools import permutations
import matplotlib.pyplot as plt



#Loading the data with the closing prices of individual assets.
asset_prices = pd.read_csv('asset_prices.csv')



#Function for generating portfolios/combinations of assets.
def portfolios_generator(assets_prices_df):
    
    #Function for calculating the expected returns of the assets and the covariance matrix between the assets.
    def asset_metrics(assets_prices):
        
        #Storing the logs of price changes and the expected returns of assets.
        log_change_prices = {}
        exp_returns = []

        #For each asset calculate the logs of asset' price changes and its expected return.
        for asset in assets_prices.columns:
            
            #Natural logarithm of asset price change as an approximation of relative price change (between the price at time t and the price at time t-1 - hence shift(1)).
            log_change_price = np.log(assets_prices[asset]/assets_prices[asset].shift(1))
            log_change_prices[asset] = log_change_price

            #Deriving expected return as average of the relative price changes with further annualization (250 trading days) using the compounded interest.
            exp_returns.append((1 + log_change_price.mean())**250 - 1)

        #Removing the first observations from the logs of price changes (which contain NA's).
        stacked_logs = np.array([logs[1:] for _, logs in log_change_prices.items()])

        #Covariance matrix with further annualization.
        covar_matrix = np.cov(stacked_logs)*250

        return (exp_returns, covar_matrix)


    #Assets' expected returns and covariance matrix.
    exp_returns, covar_matrix = asset_metrics(assets_prices_df)


    #Function for retrieving the all possible weights' combinations of assets within a portfolio, using permutation.
    def weights_combinations(assets_prices):

        #Creating an array containing generated combinations of of numbers ranging from 0 to 100, where the length of each combination corresponds to the number of assets. using permutation.
        combinations = np.array(list(permutations(range(0, 100 + 1), len(assets_prices.columns))))

        #Extracting the weights by filtering the combinations equal to 100 (since the weights have to sum up to 100).
        weights_list = [combo for combo in combinations if np.sum(combo) == 100]

        #Converting the weights into a data frame.
        weights_df = pd.DataFrame(weights_list, columns = assets_prices.columns) / 100

        return weights_df


    #Portfolio weights combinations.
    weights_df = weights_combinations(assets_prices_df)


    #Function for calculating the portfolio's expected return for particular combination of weights.
    def portfolio_returns(row, exp_returns):
        
        #Convert the row (the weights) into a numpy array.
        weights = row.to_numpy()

        #Vector multuplication as a weighted sum of the assets' expected returns.
        portf_er = np.dot(weights, exp_returns)

        return portf_er


    #Portfolio expected returns.
    port_er = pd.DataFrame(weights_df.apply(lambda row:
                                            portfolio_returns(row, exp_returns),
                                            axis = 1),
                           columns = ['port_er'])


    #Function for calculating the portfolio's standard deviation/risk/volatility for particular combination of weights.
    def portfolio_risks(row, covar_matrix):
        
        #Convert the row (the weights) into a numpy array.
        weights = row.to_numpy()

        #Vector/matrix multiplication of transposed weights, covariance matrix and the weights themselves.
        portf_std = np.sqrt(np.dot(weights.T,np.dot(covar_matrix, weights)))

        return portf_std

    
    #Portfolio risks.
    port_std = pd.DataFrame(weights_df.apply(lambda row:
                                             portfolio_risks(row, covar_matrix),
                                             axis = 1),
                            columns = ['port_std'])

    #Joining the portfolio weights, expected returns and risks.
    efficient_portfolios = pd.concat((weights_df, port_er, port_std), axis = 1)

    
    #Function for calculating the Sharpe ratio for particular combination of weights.
    def sharpe_ratio(row):

        sharpe = row['port_er']/row['port_std']

        return sharpe


    #Sharpe ratio.
    efficient_portfolios['sharpe'] = efficient_portfolios.apply(sharpe_ratio, axis = 1)
    

    return efficient_portfolios



#Generated portfolios.
portfolios = portfolios_generator(asset_prices)



#Function for retrieving the efficient portfolios.
def efficient_frontier(portfolios, approximation_order = 3):

    #The minimum portfolio risk.
    min_risk = portfolios['port_std'].min()
    
    #The portfolio expected return corresponding to the minimum portfolio risk.
    er_min_risk = portfolios.query("port_std == @min_risk")['port_er'].values[0]

    #Filtering such portfolios having expected return at least the on the level of the expected return corresponding to the minimum portfolio risk.
    filtered_portfolios = portfolios.query("port_er >= @er_min_risk").copy()

    #Rounding the portfolio expected returns based on the approximation order.
    filtered_portfolios['port_er_rounded'] = (
                                              filtered_portfolios['port_er']
                                              .round(approximation_order)
                                             )

    #Aggregation on the rounded portfolio expected returns level in order to retrieve the minimum portfolio risks. (i.e., the efficient portfolios).
    efficient_portfolios = (
                            filtered_portfolios
                            .groupby('port_er_rounded')
                            [['port_std']].min()
                            .reset_index()
                           )

    #Final output of efficient portfolios.
    efficient_portfolios_final = (
                                  filtered_portfolios
                                  .merge(efficient_portfolios,
                                         on = ['port_er_rounded','port_std'])
                                  .drop('port_er_rounded', axis = 1)
                                 )

    return efficient_portfolios_final



#Portfolios lying on the efficient frontier
efficient_portfolios = efficient_frontier(portfolios)



#Function for plotting the portfolios including the efficient frontier.
def portfolios_plot(portfolios, efficient_portfolios):

    plt.figure(figsize = (17,10))

    plt.scatter(portfolios['port_std'],portfolios['port_er'], c = portfolios['sharpe'])

    plt.plot(efficient_portfolios['port_std'], efficient_portfolios['port_er'], '-', linewidth=3.5, color = 'grey')

    plt.colorbar(label = 'Sharpe Ratio')

    plt.xlabel('Portfolio Volatility')
    plt.ylabel('Portfolio Expected Return')
    
    plt.show()



#Plotting the portfolios including the efficient frontier.
portfolios_plot(portfolios, efficient_portfolios)
# %%
