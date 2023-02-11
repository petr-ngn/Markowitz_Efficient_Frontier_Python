# Markowitz Efficient Frontier using Python
This Python script is dedicated to the portfolio optimization using Markowitz's theory about the efficient frontier within a modern portfolio theory (MPT), i.e., optimal portfolios offering higher expected returns for a defined portfolio volatility level and/or optimal portfolios offering lower portfolio volatilities for a defined portfolio expected return level, both thanks to the portfolio diversification.

As an input, I have used closing prices of 3 assets: S&P500, gold and IYR ETF tracking a market-cap-weighted index of US real estate equities. Such combination was selected in belief due to the low correlation between the assets' prices movements, thus this would result in a portfolio diversification.

## Approach

Let us build portfolios comprising of several assets. Based on assets' closed prices, let us calculate a price change at time $t$ for each asset as:

$$\Delta P_{t} = \ln\left(\frac{P_{t}}{P_{t-1}}\right) \approx \frac{P_{t}-P_{t-1}}{P_{t-1}}$$

Based on the assets' price changes, let us calculate an average daily return for each asset as:

$$\overline{r}_{Daily} = \frac{1}{n} \sum_{i=1}^{n} \Delta P_{i}$$

Based on the assets' the average daily returns, let us calculate an expected return using compounded interest (with 250 trading days) for each asset as:

$$E(r) = {\left(1 + \overline{r}_{Daily}\right)}^{250}-1$$

Based on the assets' price changes, let us calculate the variance of price changes for each asset as:

$$\sigma^{2} = \frac{1}{n} \sum_{i=1}^{n} \left(\Delta P_{i} - \overline{r}_{Daily}\right)^{2}$$

Further, let us calculate a covariance between the price changes of asset $j$ and the price changes of asset $l$ as:

$$C_{a_j,a_l} = \frac{1}{n} \sum_{i=1}^{n} \left(\Delta P_{a_j,i} - \overline{r}_{Daily,a_j}\right) \left(\Delta P_{a_l,i} - \overline{r}_{Daily,a_l}\right)$$

Based on the assets' variances of price changes and the covariances between the assets' price changes, let us construct a covariance matrix as $k \times k$ matrix (where $k$ is a number of assets) as:

$$V = 
     \begin{bmatrix}
               \sigma_{a_1}^{2} & C_{a_1, a_2} & \dots & C_{a_1, a_{k-1}} & C_{a_1, a_k} \\
               C_{a_2, a_1} &\sigma_{a_2}^{2} & \dots & C_{a_2, a_{k-1}} & C_{a_2, a_k} \\
               \vdots & \ddots & \ddots & \ddots & \vdots\\
               C_{a_{k-1}, a_1} & C_{a_{k-1}, a_2} & \dots & \sigma_{a_{k-1}}^{2} & C_{a_{k-1}, a_k} \\
               C_{a_k, a_1} & C_{a_k, a_2} & \dots & C_{a_k, a_{k-1}} & \sigma_{a_k}^{2} \\
     \end{bmatrix}$$
     
 - The diagonal of given matrix contains variances of assets' price changes, whereas the covariances between the assets' price changes are located outside the diagonal.

Next, let us create combinations of assets' weights within a portfolio, i.e., portfolio combinations, using permutations with iterables ranging from 0 to 100 (i.e., the weights) and the length of $k$ (where $k$ is a number of assets). From such generated combinations, we then filter such combinations which sum up to 100 (i.e., the sum of all assets' weights should equal to 100%).


Then for each portfolio (combination of assets' weights), we calculate a portfolio expected return as a weighted sum of the assets' expected returns as:

$$E(r)_{P} = \sum_{i=1}^{k} w_i \times E(r)_{i}$$


Pertaining to the portfolio volatility (portfolio risk), let us first denote a vector of assets' weights (for a single combination) as:

$$a = 
      \begin{bmatrix}
      w_{a_1} \\
      w_{a_2} \\
      \vdots \\
      w_{a_{k-1}} \\
      w_{a_k} \\
      \end{bmatrix}$$

Thus, using the covariance matrix of the assets' price changes and the assets' weights' vector, we then calculate a portfolio volatility for each portfolio (i.e., combination of assets' weights) using the matrix multiplication as:

$$\sigma_{P} = \sqrt{a^{T} \times V \times a}$$

In order to obtain the efficient portfolios (i.e., portfolios lying on the efficient frontier), the approach is following:
  1) Find a minimum portfolio volatility within the generated portfolios. 
  2) Find a portfolio expected return corresponding to the minimum portfolio volatility.
  3) Find such portfolios which have a portfolio expected return higher or equal to the portfolio expected return corresponding to the minimum portfolio volatility.
  4) Aggregated such portfolios on a portfolio expected return level by looking for a minimum portfolio volatility. In other words, for each portfolio expected return level, retrieve minimum portfolio volatility corresponding to the minimum portfolio volatility for the respective portfolio expected return level.

Thus, by looking for such portfolios which are dominant in terms of both maximizing portfolio expected return or minimizing portfolio volatility, we are then able to construct an efficient frontier.


![alt_text](https://raw.githubusercontent.com/petr-ngn/Markowitz_Efficient_Frontier_Python/main/portfolios_plot.jpg)
