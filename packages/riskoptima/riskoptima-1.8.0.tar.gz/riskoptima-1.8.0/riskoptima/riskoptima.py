"""
Author: Jordi Corbilla
Version: 1.8.0

Date: 05/01/2024

This module provides various financial functions and tools for analyzing and handling portfolio data learned from EDHEC Business School, 
computing statistical metrics, and optimizing portfolios based on different criteria. The main features include:
- Loading and formatting financial datasets (Fama-French, EDHEC Hedge Fund Index, etc.)
- Computing portfolio statistics (returns, volatility, Sharpe ratio, etc.)
- Running backtests on different portfolio strategies
- Efficient Frontier plotting
- Value at Risk (VaR) and Conditional Value at Risk (CVaR) computations
- Portfolio optimization based on different risk metrics
- Mean Variance Optimization
- Machine learning strategies (Linear Regression, XGBoost, SVR, etc.)
- Black litterman adjusted returns
- Market correlation and financial ratios

Dependencies: pandas, numpy, scipy, statsmodels, yfinance, datetime, scikit-learn
"""


import pandas as pd
import numpy as np
import scipy.stats
import statsmodels.api as sm
import math
import yfinance as yf
from scipy.stats import norm
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from xgboost import XGBRegressor
from sklearn.svm import SVR
from datetime import date, datetime, timedelta
import seaborn as sns
from matplotlib.ticker import MultipleLocator
from matplotlib.dates import DateFormatter
from matplotlib.dates import AutoDateLocator
import matplotlib.patches as patches

class RiskOptima:
    TRADING_DAYS = 260
    
    @staticmethod
    def get_trading_days():
        """
        Returns the number of trading days for a given year, by default 260
    
        Returns
        -------
        TRADING_DAYS : TYPE
            DESCRIPTION.
    
        """
        return RiskOptima.TRADING_DAYS
    
    @staticmethod
    def download_data_yfinance(assets, start_date, end_date):
        """
        Downloads the adjusted close price data from Yahoo Finance for the given assets
        between the specified date range.
    
        :param assets: List of asset tickers.
        :param start_date: Start date for data in 'YYYY-MM-DD' format.
        :param end_date: End date for data in 'YYYY-MM-DD' format.
        :return: A pandas DataFrame of adjusted close prices.
        """
        data = yf.download(assets, start=start_date, end=end_date, progress=False)
        return data['Close']
    
    @staticmethod
    def get_ffme_returns(file_path):
        """
        Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
        """
        me_m = pd.read_csv(file_path, header=0, index_col=0, na_values=-99.99)
        returns = me_m[['Lo 10', 'Hi 10']]
        returns.columns = ['SmallCap', 'LargeCap']
        returns = returns / 100
        returns.index = pd.to_datetime(returns.index, format="%Y%m").to_period('M')
        return returns
    
    
    @staticmethod
    def get_fff_returns(file_path):
        """
        Load the Fama-French Research Factor Monthly Dataset
        """
        returns = pd.read_csv(file_path, header=0, index_col=0, na_values=-99.99) / 100
        returns.index = pd.to_datetime(returns.index, format="%Y%m").to_period('M')
        return returns
    
    
    @staticmethod
    def get_hfi_returns(file_path):
        """
        Load and format the EDHEC Hedge Fund Index Returns
        """
        hfi = pd.read_csv(file_path, header=0, index_col=0, parse_dates=True)
        hfi = hfi / 100
        hfi.index = hfi.index.to_period('M')
        return hfi
    
    
    @staticmethod
    def get_ind_file(file_path, filetype, weighting="vw", n_inds=30):
        """
        Load and format the Ken French Industry Portfolios files
        Variant is a tuple of (weighting, size) where:
            weighting is one of "ew", "vw"
            number of inds is 30 or 49
        """    
        if filetype == "returns":
            divisor = 100
        elif filetype == "nfirms":
            divisor = 1
        elif filetype == "size":
            divisor = 1
        else:
            raise ValueError("filetype must be one of: returns, nfirms, size")
    
        ind = pd.read_csv(file_path, header=0, index_col=0, na_values=-99.99) / divisor
        ind.index = pd.to_datetime(ind.index, format="%Y%m").to_period('M')
        ind.columns = ind.columns.str.strip()
        return ind
    
    
    @staticmethod
    def get_ind_returns(file_path, weighting="vw", n_inds=30):
        """
        Load and format the Ken French Industry Portfolios Monthly Returns
        """
        return RiskOptima.get_ind_file(file_path, "returns", weighting=weighting, n_inds=n_inds)
    
    
    @staticmethod
    def get_ind_nfirms(file_path, n_inds=30):
        """
        Load and format the Ken French 30 Industry Portfolios Average number of Firms
        """
        return RiskOptima.get_ind_file(file_path, "nfirms", n_inds=n_inds)
    
    
    @staticmethod
    def get_ind_size(file_path, n_inds=30):
        """
        Load and format the Ken French 30 Industry Portfolios Average size (market cap)
        """
        return RiskOptima.get_ind_file(file_path, "size", n_inds=n_inds)
    
    
    @staticmethod
    def get_ind_market_caps(nfirms_file_path, size_file_path, n_inds=30, weights=False):
        """
        Load the industry portfolio data and derive the market caps
        """
        ind_nfirms = RiskOptima.get_ind_nfirms(nfirms_file_path, n_inds=n_inds)
        ind_size = RiskOptima.get_ind_size(size_file_path, n_inds=n_inds)
        ind_mktcap = ind_nfirms * ind_size
        if weights:
            total_mktcap = ind_mktcap.sum(axis=1)
            ind_capweight = ind_mktcap.divide(total_mktcap, axis="rows")
            return ind_capweight
        return ind_mktcap
    
    
    @staticmethod
    def get_total_market_index_returns(nfirms_file_path, size_file_path, returns_file_path, n_inds=30):
        """
        Load the 30 industry portfolio data and derive the returns of a capweighted total market index
        """
        ind_capweight = RiskOptima.get_ind_market_caps(nfirms_file_path, size_file_path, n_inds=n_inds)
        ind_return = RiskOptima.get_ind_returns(returns_file_path, weighting="vw", n_inds=n_inds)
        total_market_return = (ind_capweight * ind_return).sum(axis="columns")
        return total_market_return
    
    
    @staticmethod
    def skewness(returns):
        """
        Alternative to scipy.stats.skew()
        Computes the skewness of the supplied Series or DataFrame
        Returns a float or a Series
        """
        demeaned_returns = returns - returns.mean()
        sigma_returns = returns.std(ddof=0)
        exp = (demeaned_returns**3).mean()
        return exp / sigma_returns**3
    
    
    @staticmethod
    def kurtosis(returns):
        """
        Alternative to scipy.stats.kurtosis()
        Computes the kurtosis of the supplied Series or DataFrame
        Returns a float or a Series
        """
        demeaned_returns = returns - returns.mean()
        sigma_returns = returns.std(ddof=0)
        exp = (demeaned_returns**4).mean()
        return exp / sigma_returns**4
    
    
    @staticmethod
    def compound(returns):
        """
        Returns the result of compounding the set of returns
        """
        return np.expm1(np.log1p(returns).sum())
    
    
    @staticmethod
    def annualize_returns(returns, periods_per_year):
        """
        Annualizes a set of returns
        """
        compounded_growth = (1 + returns).prod()
        n_periods = returns.shape[0]
        return compounded_growth**(periods_per_year / n_periods) - 1
    
    
    @staticmethod
    def annualize_volatility(returns, periods_per_year):
        """
        Annualizes the volatility of a set of returns
        """
        return returns.std(axis=0) * (periods_per_year**0.5)
    
    
    @staticmethod
    def sharpe_ratio(returns, risk_free_rate, periods_per_year=None):
        """
        Calculate the Sharpe Ratio for a given set of investment returns.
    
        :param returns: pandas Series or numpy array of investment returns.
        :param float risk_free_rate: Annualized risk-free rate (e.g., yield on government bonds).
        :param int periods_per_year: Number of periods per year (e.g., 12 for monthly, 252 for daily). 
                                     Defaults to RiskOptima.get_trading_days() for daily data.
        :return: float Sharpe Ratio.
        """
        if periods_per_year is None:
            periods_per_year = RiskOptima.get_trading_days()
    
        rf_per_period = (1 + risk_free_rate)**(1 / periods_per_year) - 1
        excess_returns = returns - rf_per_period
    
        # Use helper methods for annualization
        ann_excess_returns = RiskOptima.annualize_returns(excess_returns, periods_per_year)
        ann_volatility = RiskOptima.annualize_volatility(returns, periods_per_year)
    
        return ann_excess_returns / ann_volatility
    
    @staticmethod
    def is_normal(returns, level=0.01):
        """
        Applies the Jarque-Bera test to determine if a Series is normal or not
        Test is applied at the 1% level by default
        Returns True if the hypothesis of normality is accepted, False otherwise
        """
        if isinstance(returns, pd.DataFrame):
            return returns.aggregate(RiskOptima.is_normal)
        else:
            statistic, p_value = scipy.stats.jarque_bera(returns)
            return p_value > level
    
    
    @staticmethod
    def drawdown(return_series: pd.Series):
        """
        Takes a time series of asset returns.
        Returns a DataFrame with columns for
        the wealth index, 
        the previous peaks, and 
        the percentage drawdown
        """
        wealth_index = 1000 * (1 + return_series).cumprod()
        previous_peaks = wealth_index.cummax()
        drawdowns = (wealth_index - previous_peaks) / previous_peaks
        return pd.DataFrame({
            "Wealth": wealth_index, 
            "Previous Peak": previous_peaks, 
            "Drawdown": drawdowns
        })
    
    
    @staticmethod
    def semideviation(returns):
        """
        Returns the semideviation aka negative semideviation of returns
        returns must be a Series or a DataFrame, else raises a TypeError
        """
        if isinstance(returns, pd.Series):
            is_negative = returns < 0
            return returns[is_negative].std(ddof=0)
        elif isinstance(returns, pd.DataFrame):
            return returns.aggregate(RiskOptima.semideviation)
        else:
            raise TypeError("Expected returns to be a Series or DataFrame")
    
    
    @staticmethod
    def var_historic(returns, level=5):
        """
        Returns the historic Value at Risk at a specified level
        i.e. returns the number such that "level" percent of the returns
        fall below that number, and the (100-level) percent are above
        """
        if isinstance(returns, pd.DataFrame):
            return returns.aggregate(RiskOptima.var_historic, level=level)
        elif isinstance(returns, pd.Series):
            return -np.percentile(returns, level)
        else:
            raise TypeError("Expected returns to be a Series or DataFrame")
    
    
    @staticmethod
    def cvar_historic(returns, level=5):
        """
        Computes the Conditional VaR of Series or DataFrame
        """
        if isinstance(returns, pd.Series):
            is_beyond = returns <= -RiskOptima.var_historic(returns, level=level)
            return -returns[is_beyond].mean()
        elif isinstance(returns, pd.DataFrame):
            return returns.aggregate(RiskOptima.cvar_historic, level=level)
        else:
            raise TypeError("Expected returns to be a Series or DataFrame")
    
    
    @staticmethod
    def var_gaussian(returns, level=5, modified=False):
        """
        Returns the Parametric Gaussian VaR of a Series or DataFrame
        If "modified" is True, then the modified VaR is returned,
        using the Cornish-Fisher modification
        """
        z = norm.ppf(level / 100)
        if modified:
            s = RiskOptima.skewness(returns)
            k = RiskOptima.kurtosis(returns)
            z = (z +
                 (z**2 - 1) * s / 6 +
                 (z**3 - 3 * z) * (k - 3) / 24 -
                 (2 * z**3 - 5 * z) * (s**2) / 36)
        return -(returns.mean() + z * returns.std(ddof=0))
    
    
    @staticmethod
    def portfolio_return(weights, returns):
        """
        Computes the return on a portfolio from constituent returns and weights
        weights are a numpy array or Nx1 matrix and returns are a numpy array or Nx1 matrix
        """
        return weights.T @ returns
    
    
    @staticmethod
    def portfolio_volatility(weights, covmat):
        """
        Computes the volatility of a portfolio from a covariance matrix and constituent weights
        weights are a numpy array or N x 1 maxtrix and covmat is an N x N matrix
        """
        volatility = (weights.T @ covmat @ weights)**0.5
        return volatility
    
    
    @staticmethod
    def plot_ef2(n_points, expected_returns, cov, style):
        """
        Plots the 2-asset efficient frontier
        """
        if expected_returns.shape[0] != 2:
            raise ValueError("plot_ef2 can only plot 2-asset frontiers")
        weights = [np.array([w, 1 - w]) for w in np.linspace(0, 1, n_points)]
        rets = [RiskOptima.portfolio_return(w, expected_returns) for w in weights]
        volatilities = [RiskOptima.portfolio_volatility(w, cov) for w in weights]
        ef = pd.DataFrame({
            "Returns": rets, 
            "Volatility": volatilities
        })
        return ef.plot.line(x="Volatility", y="Returns", style=style)
    
    
    @staticmethod
    def minimize_volatility(target_return, expected_returns, cov):
        """
        Returns the optimal weights that achieve the target return
        given a set of expected returns and a covariance matrix
        """
        n = expected_returns.shape[0]
        init_guess = np.repeat(1 / n, n)
        bounds = ((0.0, 1.0),) * n
        weights_sum_to_1 = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
        return_is_target = {'type': 'eq', 'args': (expected_returns,), 'fun': lambda weights, expected_returns: target_return - RiskOptima.portfolio_return(weights, expected_returns)}
        weights = minimize(RiskOptima.portfolio_volatility, init_guess, args=(cov,), method='SLSQP', options={'disp': False}, constraints=(weights_sum_to_1, return_is_target), bounds=bounds)
        return weights.x
    
    
    @staticmethod
    def tracking_error(returns_a, returns_b):
        """
        Returns the Tracking Error between the two return series
        """
        return np.sqrt(((returns_a - returns_b)**2).sum())
    
    
    @staticmethod
    def max_sharpe_ratio(riskfree_rate, expected_returns, cov):
        """
        Returns the weights of the portfolio that gives you the maximum Sharpe ratio
        given the riskfree rate and expected returns and a covariance matrix
        """
        n = expected_returns.shape[0]
        init_guess = np.repeat(1 / n, n)
        bounds = ((0.0, 1.0),) * n
        weights_sum_to_1 = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
        def neg_sharpe(weights, riskfree_rate, expected_returns, cov):
            r = RiskOptima.portfolio_return(weights, expected_returns)
            vol = RiskOptima.portfolio_volatility(weights, cov)
            return -(r - riskfree_rate) / vol
        weights = minimize(neg_sharpe, init_guess, args=(riskfree_rate, expected_returns, cov), method='SLSQP', options={'disp': False}, constraints=(weights_sum_to_1,), bounds=bounds)
        return weights.x
    
    
    @staticmethod
    def global_minimum_volatility(cov):
        """
        Returns the weights of the Global Minimum Volatility portfolio
        given a covariance matrix
        """
        n = cov.shape[0]
        return RiskOptima.max_sharpe_ratio(0, np.repeat(1, n), cov)
    
    
    @staticmethod
    def optimal_weights(n_points, expected_returns, cov):
        """
        Returns a list of weights that represent a grid of n_points on the efficient frontier
        """
        target_returns = np.linspace(expected_returns.min(), expected_returns.max(), n_points)
        weights = [RiskOptima.minimize_volatility(target_return, expected_returns, cov) for target_return in target_returns]
        return weights
    
    
    @staticmethod
    def plot_ef(n_points, expected_returns, cov, style='.-', legend=False, show_cml=False, riskfree_rate=0, show_ew=False, show_gmv=False):
        """
        Plots the multi-asset efficient frontier
        """
        weights = RiskOptima.optimal_weights(n_points, expected_returns, cov)
        rets = [RiskOptima.portfolio_return(w, expected_returns) for w in weights]
        volatilities = [RiskOptima.portfolio_volatility(w, cov) for w in weights]
        ef = pd.DataFrame({
            "Returns": rets, 
            "Volatility": volatilities
        })
        ax = ef.plot.line(x="Volatility", y="Returns", style=style, legend=legend)
        if show_cml:
            ax.set_xlim(left=0)
            w_msr = RiskOptima.max_sharpe_ratio(riskfree_rate, expected_returns, cov)
            r_msr = RiskOptima.portfolio_return(w_msr, expected_returns)
            vol_msr = RiskOptima.portfolio_volatility(w_msr, cov)
            cml_x = [0, vol_msr]
            cml_y = [riskfree_rate, r_msr]
            ax.plot(cml_x, cml_y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=10)
        if show_ew:
            n = expected_returns.shape[0]
            w_ew = np.repeat(1 / n, n)
            r_ew = RiskOptima.portfolio_return(w_ew, expected_returns)
            vol_ew = RiskOptima.portfolio_volatility(w_ew, cov)
            ax.plot([vol_ew], [r_ew], color='goldenrod', marker='o', markersize=10)
        if show_gmv:
            w_gmv = RiskOptima.global_minimum_volatility(cov)
            r_gmv = RiskOptima.portfolio_return(w_gmv, expected_returns)
            vol_gmv = RiskOptima.portfolio_volatility(w_gmv, cov)
            ax.plot([vol_gmv], [r_gmv], color='midnightblue', marker='o', markersize=10)
        return ax
    
    @staticmethod
    def plot_ef_ax(n_points, expected_returns, cov, style='.-', legend=False, show_cml=False, riskfree_rate=0, show_ew=False, show_gmv=False, ax=None):
        """
        Plots the multi-asset efficient frontier
        """
        
        weights = RiskOptima.optimal_weights(n_points, expected_returns, cov)
        rets = [RiskOptima.portfolio_return(w, expected_returns) for w in weights]
        volatilities = [RiskOptima.portfolio_volatility(w, cov) for w in weights]
        ef = pd.DataFrame({
            "Returns": rets, 
            "Volatility": volatilities
        })
        ef.plot.line(x="Volatility", y="Returns", style=style, legend=legend, ax=ax)
        if show_cml:
            ax.set_xlim(left=0)
            w_msr = RiskOptima.max_sharpe_ratio(riskfree_rate, expected_returns, cov)
            r_msr = RiskOptima.portfolio_return(w_msr, expected_returns)
            vol_msr = RiskOptima.portfolio_volatility(w_msr, cov)
            cml_x = [0, vol_msr]
            cml_y = [riskfree_rate, r_msr]
            ax.plot(cml_x, cml_y, color='blue', marker='o', linestyle='dashed', linewidth=2, markersize=10, label='Capital Market Line')
        if show_ew:
            n = expected_returns.shape[0]
            w_ew = np.repeat(1 / n, n)
            r_ew = RiskOptima.portfolio_return(w_ew, expected_returns)
            vol_ew = RiskOptima.portfolio_volatility(w_ew, cov)
            ax.plot([vol_ew], [r_ew], color='goldenrod', marker='o', markersize=10, label='Naive portfolio')
        if show_gmv:
            w_gmv = RiskOptima.global_minimum_volatility(cov)
            r_gmv = RiskOptima.portfolio_return(w_gmv, expected_returns)
            vol_gmv = RiskOptima.portfolio_volatility(w_gmv, cov)
            ax.plot([vol_gmv], [r_gmv], color='midnightblue', marker='o', markersize=10, label='Global Minimum-variance Portfolio')
        return ax
    
    @staticmethod
    def run_cppi(risky_returns, safe_returns=None, m=3, start=1000, floor=0.8, riskfree_rate=0.03, drawdown=None):
        """
        Run a backtest of the CPPI strategy, given a set of returns for the risky asset
        Returns a dictionary containing: Asset Value History, Risk Budget History, Risky Weight History
        """
        dates = risky_returns.index
        n_steps = len(dates)
        account_value = start
        floor_value = start * floor
        peak = account_value
        if isinstance(risky_returns, pd.Series): 
            risky_returns = pd.DataFrame(risky_returns, columns=["R"])
    
        if safe_returns is None:
            safe_returns = pd.DataFrame().reindex_like(risky_returns)
            safe_returns.values[:] = riskfree_rate / 12
        account_history = pd.DataFrame().reindex_like(risky_returns)
        risky_w_history = pd.DataFrame().reindex_like(risky_returns)
        cushion_history = pd.DataFrame().reindex_like(risky_returns)
        floorval_history = pd.DataFrame().reindex_like(risky_returns)
        peak_history = pd.DataFrame().reindex_like(risky_returns)
    
        for step in range(n_steps):
            if drawdown is not None:
                peak = np.maximum(peak, account_value)
                floor_value = peak * (1 - drawdown)
            cushion = (account_value - floor_value) / account_value
            risky_w = m * cushion
            risky_w = np.minimum(risky_w, 1)
            risky_w = np.maximum(risky_w, 0)
            safe_w = 1 - risky_w
            risky_alloc = account_value * risky_w
            safe_alloc = account_value * safe_w
            account_value = risky_alloc * (1 + risky_returns.iloc[step]) + safe_alloc * (1 + safe_returns.iloc[step])
            cushion_history.iloc[step] = cushion
            risky_w_history.iloc[step] = risky_w
            account_history.iloc[step] = account_value
            floorval_history.iloc[step] = floor_value
            peak_history.iloc[step] = peak
        risky_wealth = start * (1 + risky_returns).cumprod()
        backtest_result = {
            "Wealth": account_history,
            "Risky Wealth": risky_wealth, 
            "Risk Budget": cushion_history,
            "Risky Allocation": risky_w_history,
            "m": m,
            "start": start,
            "floor": floor,
            "risky_returns": risky_returns,
            "safe_returns": safe_returns,
            "drawdown": drawdown,
            "peak": peak_history,
            "floorval_history": floorval_history
        }
        return backtest_result
    
    @staticmethod
    def summary_stats(returns, riskfree_rate=0.03):
        """
        Return a DataFrame that contains aggregated summary stats for the returns in the columns of returns
        """
        ann_returns = returns.aggregate(RiskOptima.annualize_returns, periods_per_year=12)
        ann_volatility = returns.aggregate(RiskOptima.annualize_volatility, periods_per_year=12)
        ann_sr = returns.aggregate(RiskOptima.sharpe_ratio, riskfree_rate=riskfree_rate, periods_per_year=12)
        dd = returns.aggregate(lambda returns: RiskOptima.drawdown(returns).Drawdown.min())
        skew = returns.aggregate(RiskOptima.skewness)
        kurt = returns.aggregate(RiskOptima.kurtosis)
        cf_var5 = returns.aggregate(RiskOptima.var_gaussian, modified=True)
        hist_cvar5 = returns.aggregate(RiskOptima.cvar_historic)
        return pd.DataFrame({
            "Annualized Return": ann_returns,
            "Annualized Volatility": ann_volatility,
            "Skewness": skew,
            "Kurtosis": kurt,
            "Cornish-Fisher VaR (5%)": cf_var5,
            "Historic CVaR (5%)": hist_cvar5,
            "Sharpe Ratio": ann_sr,
            "Max Drawdown": dd
        })
    
    @staticmethod
    def gbm(n_years=10, n_scenarios=1000, mu=0.07, sigma=0.15, steps_per_year=12, s_0=100.0, prices=True):
        """
        Evolution of Geometric Brownian Motion trajectories, such as for Stock Prices through Monte Carlo
        :param n_years:  The number of years to generate data for
        :param n_paths: The number of scenarios/trajectories
        :param mu: Annualized Drift, e.g. Market Return
        :param sigma: Annualized Volatility
        :param steps_per_year: granularity of the simulation
        :param s_0: initial value
        :return: a numpy array of n_paths columns and n_years*steps_per_year rows
        """
        dt = 1 / steps_per_year
        n_steps = int(n_years * steps_per_year) + 1
        rets_plus_1 = np.random.normal(loc=(1 + mu)**dt, scale=(sigma * np.sqrt(dt)), size=(n_steps, n_scenarios))
        rets_plus_1[0] = 1
        ret_val = s_0 * pd.DataFrame(rets_plus_1).cumprod() if prices else rets_plus_1 - 1
        return ret_val
    
    @staticmethod
    def regress(dependent_variable, explanatory_variables, alpha=True):
        """
        Runs a linear regression to decompose the dependent variable into the explanatory variables
        returns an object of type statsmodel's RegressionResults on which you can call
           .summary() to print a full summary
           .params for the coefficients
           .tvalues and .pvalues for the significance levels
           .rsquared_adj and .rsquared for quality of fit
        """
        if alpha:
            explanatory_variables = explanatory_variables.copy()
            explanatory_variables["Alpha"] = 1
        
        lm = sm.OLS(dependent_variable, explanatory_variables).fit()
        return lm
    
    @staticmethod
    def portfolio_tracking_error(weights, ref_returns, bb_returns):
        """
        Returns the tracking error between the reference returns
        and a portfolio of building block returns held with given weights
        """
        return RiskOptima.tracking_error(ref_returns, (weights * bb_returns).sum(axis=1))
    
    @staticmethod
    def style_analysis(dependent_variable, explanatory_variables):
        """
        Returns the optimal weights that minimizes the tracking error between
        a portfolio of the explanatory variables and the dependent variable
        """
        n = explanatory_variables.shape[1]
        init_guess = np.repeat(1 / n, n)
        bounds = ((0.0, 1.0),) * n
        weights_sum_to_1 = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
        solution = minimize(RiskOptima.portfolio_tracking_error, init_guess, args=(dependent_variable, explanatory_variables,), method='SLSQP', options={'disp': False}, constraints=(weights_sum_to_1,), bounds=bounds)
        weights = pd.Series(solution.x, index=explanatory_variables.columns)
        return weights
    
    @staticmethod
    def ff_analysis(returns, factors):
        """
        Returns the loadings of returns on the Fama French Factors
        which can be read in using get_fff_returns()
        the index of returns must be a (not necessarily proper) subset of the index of factors
        returns is either a Series or a DataFrame
        """
        if isinstance(returns, pd.Series):
            dependent_variable = returns
            explanatory_variables = factors.loc[returns.index]
            tilts = RiskOptima.regress(dependent_variable, explanatory_variables).params
        elif isinstance(returns, pd.DataFrame):
            tilts = pd.DataFrame({col: RiskOptima.ff_analysis(returns[col], factors) for col in returns.columns})
        else:
            raise TypeError("returns must be a Series or a DataFrame")
        return tilts
    
    @staticmethod
    def weight_ew(returns, cap_weights=None, max_cw_mult=None, microcap_threshold=None, **kwargs):
        """
        Returns the weights of the EW portfolio based on the asset returns "returns" as a DataFrame
        If supplied a set of capweights and a capweight tether, it is applied and reweighted 
        """
        n = len(returns.columns)
        ew = pd.Series(1 / n, index=returns.columns)
        if cap_weights is not None:
            cw = cap_weights.loc[returns.index[0]]
            if microcap_threshold is not None and microcap_threshold > 0:
                microcap = cw < microcap_threshold
                ew[microcap] = 0
                ew = ew / ew.sum()
            if max_cw_mult is not None and max_cw_mult > 0:
                ew = np.minimum(ew, cw * max_cw_mult)
                ew = ew / ew.sum()
        return ew
    
    @staticmethod
    def weight_cw(returns, cap_weights, **kwargs):
        """
        Returns the weights of the CW portfolio based on the time series of capweights
        """
        w = cap_weights.loc[returns.index[0]]
        return w / w.sum()
    
    @staticmethod
    def backtest_ws(returns, estimation_window=60, weighting=weight_ew, verbose=False, **kwargs):
        """
        Backtests a given weighting scheme, given some parameters:
        returns : asset returns to use to build the portfolio
        estimation_window: the window to use to estimate parameters
        weighting: the weighting scheme to use, must be a function that takes "returns", and a variable number of keyword-value arguments
        """
        n_periods = returns.shape[0]
        windows = [(start, start + estimation_window) for start in range(n_periods - estimation_window)]
        weights = [weighting(returns.iloc[win[0]:win[1]], **kwargs) for win in windows]
        weights = pd.DataFrame(weights, index=returns.iloc[estimation_window:].index, columns=returns.columns)
        portfolio_returns = (weights * returns).sum(axis="columns", min_count=1)
        return portfolio_returns
    
    @staticmethod
    def sample_covariance(returns, **kwargs):
        """
        Returns the sample covariance of the supplied returns
        """
        return returns.cov()
    
    @staticmethod
    def weight_gmv(returns, cov_estimator=sample_covariance, **kwargs):
        """
        Produces the weights of the GMV portfolio given a covariance matrix of the returns 
        """
        est_cov = cov_estimator(returns, **kwargs)
        return RiskOptima.global_minimum_volatility(est_cov)
    
    @staticmethod
    def cc_covariance(returns, **kwargs):
        """
        Estimates a covariance matrix by using the Elton/Gruber Constant Correlation model
        """
        rhos = returns.corr()
        n = rhos.shape[0]
        rho_bar = (rhos.values.sum() - n) / (n * (n - 1))
        ccor = np.full_like(rhos, rho_bar)
        np.fill_diagonal(ccor, 1.)
        sd = returns.std(axis=0)
        return pd.DataFrame(ccor * np.outer(sd, sd), index=returns.columns, columns=returns.columns)
    
    @staticmethod
    def shrinkage_covariance(returns, delta=0.5, **kwargs):
        """
        Covariance estimator that shrinks between the Sample Covariance and the Constant Correlation Estimators
        """
        prior = RiskOptima.cc_covariance(returns, **kwargs)
        sample = RiskOptima.sample_covariance(returns, **kwargs)
        return delta * prior + (1 - delta) * sample
    
    @staticmethod
    def risk_contribution(weights, cov):
        """
        Compute the contributions to risk of the constituents of a portfolio, given a set of portfolio weights and a covariance matrix
        """
        total_portfolio_var = RiskOptima.portfolio_volatility(weights, cov)**2
        marginal_contrib = cov @ weights
        risk_contrib = np.multiply(marginal_contrib, weights.T) / total_portfolio_var
        return risk_contrib
    
    @staticmethod
    def target_risk_contributions(target_risk, cov):
        """
        Returns the weights of the portfolio that gives you the weights such
        that the contributions to portfolio risk are as close as possible to
        the target_risk, given the covariance matrix
        """
        n = cov.shape[0]
        init_guess = np.repeat(1 / n, n)
        bounds = ((0.0, 1.0),) * n
        weights_sum_to_1 = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
        def msd_risk(weights, target_risk, cov):
            w_contribs = RiskOptima.risk_contribution(weights, cov)
            return ((w_contribs - target_risk)**2).sum()
        weights = minimize(msd_risk, init_guess, args=(target_risk, cov), method='SLSQP', options={'disp': False}, constraints=(weights_sum_to_1,), bounds=bounds)
        return weights.x
    
    @staticmethod
    def equal_risk_contributions(cov):
        """
        Returns the weights of the portfolio that equalizes the contributions
        of the constituents based on the given covariance matrix
        """
        n = cov.shape[0]
        return RiskOptima.target_risk_contributions(target_risk=np.repeat(1 / n, n), cov=cov)
    
    @staticmethod
    def weight_erc(returns, cov_estimator=sample_covariance, **kwargs):
        """
        Produces the weights of the ERC portfolio given a covariance matrix of the returns 
        """
        est_cov = cov_estimator(returns, **kwargs)
        return RiskOptima.equal_risk_contributions(est_cov)
    
    @staticmethod
    def discount(t, r):
        """
        Compute the price of a pure discount bond that pays a dollar at time period t
        and r is the per-period interest rate
        returns a |t| x |r| Series or DataFrame
        r can be a float, Series or DataFrame
        returns a DataFrame indexed by t
        """
        discounts = pd.DataFrame([(r+1)**-i for i in t])
        discounts.index = t
        return discounts
    
    @staticmethod
    def pv(flows, r):
        """
        Compute the present value of a sequence of cash flows given by the time (as an index) and amounts
        r can be a scalar, or a Series or DataFrame with the number of rows matching the num of rows in flows
        """
        dates = flows.index
        discounts = RiskOptima.discount(dates, r)
        return discounts.multiply(flows, axis='rows').sum()
    
    @staticmethod
    def funding_ratio(assets, liabilities, r):
        """
        Computes the funding ratio of a series of liabilities, based on an interest rate and current value of assets
        """
        return RiskOptima.pv(assets, r)/RiskOptima.pv(liabilities, r)
    
    @staticmethod
    def inst_to_ann(r):
        """
        Convert an instantaneous interest rate to an annual interest rate
        """
        return np.expm1(r)
    
    @staticmethod
    def ann_to_inst(r):
        """
        Convert an instantaneous interest rate to an annual interest rate
        """
        return np.log1p(r)
    
    @staticmethod
    def cir(n_years = 10, n_scenarios=1, a=0.05, b=0.03, sigma=0.05, steps_per_year=12, r_0=None):
        """
        Generate random interest rate evolution over time using the CIR model
        b and r_0 are assumed to be the annualized rates, not the short rate
        and the returned values are the annualized rates as well
        """
        if r_0 is None: r_0 = b 
        r_0 = RiskOptima.ann_to_inst(r_0)
        dt = 1/steps_per_year
        num_steps = int(n_years*steps_per_year) + 1 # because n_years might be a float
        
        shock = np.random.normal(0, scale=np.sqrt(dt), size=(num_steps, n_scenarios))
        rates = np.empty_like(shock)
        rates[0] = r_0
    
        ## For Price Generation
        h = math.sqrt(a**2 + 2*sigma**2)
        prices = np.empty_like(shock)
        ####
    
        def price(ttm, r):
            _A = ((2*h*math.exp((h+a)*ttm/2))/(2*h+(h+a)*(math.exp(h*ttm)-1)))**(2*a*b/sigma**2)
            _B = (2*(math.exp(h*ttm)-1))/(2*h + (h+a)*(math.exp(h*ttm)-1))
            _P = _A*np.exp(-_B*r)
            return _P
        prices[0] = price(n_years, r_0)
        ####
        
        for step in range(1, num_steps):
            r_t = rates[step-1]
            d_r_t = a*(b-r_t)*dt + sigma*np.sqrt(r_t)*shock[step]
            rates[step] = abs(r_t + d_r_t)
            # generate prices at time t as well ...
            prices[step] = price(n_years-step*dt, rates[step])
    
        rates = pd.DataFrame(data=RiskOptima.inst_to_ann(rates), index=range(num_steps))
        ### for prices
        prices = pd.DataFrame(data=prices, index=range(num_steps))
        ###
        return rates, prices
    
    @staticmethod
    def bond_cash_flows(maturity, principal=100, coupon_rate=0.03, coupons_per_year=12):
        """
        Returns the series of cash flows generated by a bond,
        indexed by the payment/coupon number
        """
        n_coupons = round(maturity*coupons_per_year)
        coupon_amt = principal*coupon_rate/coupons_per_year
        coupon_times = np.arange(1, n_coupons+1)
        cash_flows = pd.Series(data=coupon_amt, index=coupon_times)
        cash_flows.iloc[-1] += principal
        return cash_flows
        
    @staticmethod
    def bond_price(maturity, principal=100, coupon_rate=0.03, coupons_per_year=12, discount_rate=0.03):
        """
        Computes the price of a bond that pays regular coupons until maturity
        at which time the principal and the final coupon is returned
        This is not designed to be efficient, rather,
        it is to illustrate the underlying principle behind bond pricing!
        If discount_rate is a DataFrame, then this is assumed to be the rate on each coupon date
        and the bond value is computed over time.
        i.e. The index of the discount_rate DataFrame is assumed to be the coupon number
        """
        if isinstance(discount_rate, pd.DataFrame):
            pricing_dates = discount_rate.index
            prices = pd.DataFrame(index=pricing_dates, columns=discount_rate.columns)
            for t in pricing_dates:
                prices.loc[t] = RiskOptima.bond_price(maturity-t/coupons_per_year, principal, coupon_rate, coupons_per_year,
                                          discount_rate.loc[t])
            return prices
        else: # base case ... single time period
            if maturity <= 0: return principal+principal*coupon_rate/coupons_per_year
            cash_flows = RiskOptima.bond_cash_flows(maturity, principal, coupon_rate, coupons_per_year)
            return RiskOptima.pv(cash_flows, discount_rate/coupons_per_year)
    
    @staticmethod
    def macaulay_duration(flows, discount_rate):
        """
        Computes the Macaulay Duration of a sequence of cash flows, given a per-period discount rate
        """
        discounted_flows = RiskOptima.discount(flows.index, discount_rate)*flows
        weights = discounted_flows/discounted_flows.sum()
        return np.average(flows.index, weights=weights)
    
    @staticmethod
    def match_durations(cf_t, cf_s, cf_l, discount_rate):
        """
        Returns the weight W in cf_s that, along with (1-W) in cf_l will have an effective
        duration that matches cf_t
        """
        d_t = RiskOptima.macaulay_duration(cf_t, discount_rate)
        d_s = RiskOptima.macaulay_duration(cf_s, discount_rate)
        d_l = RiskOptima.macaulay_duration(cf_l, discount_rate)
        return (d_l - d_t)/(d_l - d_s)
    
    @staticmethod
    def bond_total_return(monthly_prices, principal, coupon_rate, coupons_per_year):
        """
        Computes the total return of a Bond based on monthly bond prices and coupon payments
        Assumes that dividends (coupons) are paid out at the end of the period (e.g. end of 3 months for quarterly div)
        and that dividends are reinvested in the bond
        """
        coupons = pd.DataFrame(data = 0, index=monthly_prices.index, columns=monthly_prices.columns)
        t_max = monthly_prices.index.max()
        pay_date = np.linspace(12/coupons_per_year, t_max, int(coupons_per_year*t_max/12), dtype=int)
        coupons.iloc[pay_date] = principal*coupon_rate/coupons_per_year
        total_returns = (monthly_prices + coupons)/monthly_prices.shift()-1
        return total_returns.dropna()
    
    @staticmethod
    def bt_mix(r1, r2, allocator, **kwargs):
        """
        Runs a back test (simulation) of allocating between a two sets of returns
        r1 and r2 are T x N DataFrames or returns where T is the time step index and N is the number of scenarios.
        allocator is a function that takes two sets of returns and allocator specific parameters, and produces
        an allocation to the first portfolio (the rest of the money is invested in the GHP) as a T x 1 DataFrame
        Returns a T x N DataFrame of the resulting N portfolio scenarios
        """
        if not r1.shape == r2.shape:
            raise ValueError("r1 and r2 should have the same shape")
        weights = allocator(r1, r2, **kwargs)
        if not weights.shape == r1.shape:
            raise ValueError("Allocator returned weights with a different shape than the returns")
        r_mix = weights*r1 + (1-weights)*r2
        return r_mix
    
    @staticmethod
    def fixedmix_allocator(r1, r2, w1, **kwargs):
        """
        Produces a time series over T steps of allocations between the PSP and GHP across N scenarios
        PSP and GHP are T x N DataFrames that represent the returns of the PSP and GHP such that:
         each column is a scenario
         each row is the price for a timestep
        Returns an T x N DataFrame of PSP Weights
        """
        return pd.DataFrame(data = w1, index=r1.index, columns=r1.columns)
    
    @staticmethod
    def terminal_values(rets):
        """
        Computes the terminal values from a set of returns supplied as a T x N DataFrame
        Return a Series of length N indexed by the columns of rets
        """
        return (rets+1).prod()
    
    @staticmethod
    def terminal_stats(rets, floor = 0.8, cap=np.inf, name="Stats"):
        """
        Produce Summary Statistics on the terminal values per invested dollar
        across a range of N scenarios
        rets is a T x N DataFrame of returns, where T is the time-step (we assume rets is sorted by time)
        Returns a 1 column DataFrame of Summary Stats indexed by the stat name 
        """
        terminal_wealth = (rets+1).prod()
        breach = terminal_wealth < floor
        reach = terminal_wealth >= cap
        p_breach = breach.mean() if breach.sum() > 0 else np.nan
        p_reach = breach.mean() if reach.sum() > 0 else np.nan
        e_short = (floor-terminal_wealth[breach]).mean() if breach.sum() > 0 else np.nan
        e_surplus = (cap-terminal_wealth[reach]).mean() if reach.sum() > 0 else np.nan
        sum_stats = pd.DataFrame.from_dict({
            "mean": terminal_wealth.mean(),
            "std" : terminal_wealth.std(axis=0),
            "p_breach": p_breach,
            "e_short":e_short,
            "p_reach": p_reach,
            "e_surplus": e_surplus
        }, orient="index", columns=[name])
        return sum_stats
    
    @staticmethod
    def glidepath_allocator(r1, r2, start_glide=1, end_glide=0.0):
        """
        Allocates weights to r1 starting at start_glide and ends at end_glide
        by gradually moving from start_glide to end_glide over time
        """
        n_points = r1.shape[0]
        n_col = r1.shape[1]
        path = pd.Series(data=np.linspace(start_glide, end_glide, num=n_points))
        paths = pd.concat([path]*n_col, axis=1)
        paths.index = r1.index
        paths.columns = r1.columns
        return paths
    
    @staticmethod
    def floor_allocator(psp_r, ghp_r, floor, zc_prices, m=3):
        """
        Allocate between PSP and GHP with the goal to provide exposure to the upside
        of the PSP without going violating the floor.
        Uses a CPPI-style dynamic risk budgeting algorithm by investing a multiple
        of the cushion in the PSP
        Returns a DataFrame with the same shape as the psp/ghp representing the weights in the PSP
        """
        if zc_prices.shape != psp_r.shape:
            raise ValueError("PSP and ZC Prices must have the same shape")
        n_steps, n_scenarios = psp_r.shape
        account_value = np.repeat(1, n_scenarios)
        floor_value = np.repeat(1, n_scenarios)
        w_history = pd.DataFrame(index=psp_r.index, columns=psp_r.columns)
        for step in range(n_steps):
            floor_value = floor*zc_prices.iloc[step] ## PV of Floor assuming today's rates and flat YC
            cushion = (account_value - floor_value)/account_value
            psp_w = (m*cushion).clip(0, 1) # same as applying min and max
            ghp_w = 1-psp_w
            psp_alloc = account_value*psp_w
            ghp_alloc = account_value*ghp_w
            # recompute the new account value at the end of this step
            account_value = psp_alloc*(1+psp_r.iloc[step]) + ghp_alloc*(1+ghp_r.iloc[step])
            w_history.iloc[step] = psp_w
        return w_history
    
    @staticmethod
    def drawdown_allocator(psp_r, ghp_r, maxdd, m=3):
        """
        Allocate between PSP and GHP with the goal to provide exposure to the upside
        of the PSP without going violating the floor.
        Uses a CPPI-style dynamic risk budgeting algorithm by investing a multiple
        of the cushion in the PSP
        Returns a DataFrame with the same shape as the psp/ghp representing the weights in the PSP
        """
        n_steps, n_scenarios = psp_r.shape
        account_value = np.repeat(1, n_scenarios)
        floor_value = np.repeat(1, n_scenarios)
        ### For MaxDD
        peak_value = np.repeat(1, n_scenarios)
        w_history = pd.DataFrame(index=psp_r.index, columns=psp_r.columns)
        for step in range(n_steps):
            ### For MaxDD
            floor_value = (1-maxdd)*peak_value ### Floor is based on Prev Peak
            cushion = (account_value - floor_value)/account_value
            psp_w = (m*cushion).clip(0, 1) # same as applying min and max
            ghp_w = 1-psp_w
            psp_alloc = account_value*psp_w
            ghp_alloc = account_value*ghp_w
            # recompute the new account value at the end of this step
            account_value = psp_alloc*(1+psp_r.iloc[step]) + ghp_alloc*(1+ghp_r.iloc[step])
            ### For MaxDD
            peak_value = np.maximum(peak_value, account_value) ### For MaxDD
            w_history.iloc[step] = psp_w
        return w_history
    
    @staticmethod
    def discount_v2(t, r, freq):
        """
        Compute the price of a pure discount bond that pays a dollar at time period t
        and r is the per-period interest rate
        returns a DataFrame indexed by t
        """
        discounts = pd.DataFrame([(1 + r / freq) ** -(t * freq) for t in t], index=t, columns=['df'])
        return discounts
    
    @staticmethod
    def bond_cash_flows_v2(n_periods, par, coupon_rate, freq):
        """Generate bond cash flows"""
        coupon = par * coupon_rate / freq
        cash_flows = np.full(n_periods, coupon)
        cash_flows[-1] += par
        return cash_flows
    
    @staticmethod
    def bond_price_v2(cash_flows, yield_rate, freq):
        """Calculate the price of the bond"""
        n = len(cash_flows)
        times = np.arange(1, n + 1) / freq
        discount_factors = RiskOptima.discount(times, yield_rate).values.flatten()
        present_values = cash_flows * discount_factors
        return sum(present_values)
    
    @staticmethod
    def macaulay_duration_v2(cash_flows, yield_rate, freq):
        """Calculate the Macaulay Duration"""
        n = len(cash_flows)
        times = np.arange(1, n + 1) / freq
        discount_factors = RiskOptima.discount(times, yield_rate).values.flatten()
        present_values = cash_flows * discount_factors
        
        weighted_sum = sum(times * present_values)
        total_present_value = sum(present_values)
        
        return weighted_sum / total_present_value
    
    @staticmethod
    def macaulay_duration_v3(cash_flows, yield_rate, freq):
        """Calculate the Macaulay Duration and output the detailed table"""
        n = len(cash_flows)
        times = np.arange(1, n + 1) / freq
        discount_factors = RiskOptima.discount_v2(times, yield_rate, freq).values.flatten()
        present_values = cash_flows * discount_factors
        total_present_value = sum(present_values)
        weights = present_values / total_present_value
        weighted_average_times = times * weights
        
        # Create the DataFrame
        df = pd.DataFrame({
            't': times,
            'df': discount_factors,
            'cf': cash_flows,
            'pv': present_values,
            'weight': weights,
            'wat': weighted_average_times
        })
        
        # Add the totals row
        totals = pd.DataFrame({
            't': ['Total'],
            'df': [''],
            'cf': [sum(cash_flows)],
            'pv': [total_present_value],
            'weight': [sum(weights)],
            'wat': [sum(weighted_average_times)]
        })
        
        df = pd.concat([df, totals], ignore_index=True)
        
        return df
    
    @staticmethod
    def calculate_statistics(data, risk_free_rate=0.0):
        """
        Calculates daily returns, covariance matrix, mean daily returns, 
        annualized returns, annualized volatility, and Sharpe ratio 
        for the entire dataset.
    
        :param data: A pandas DataFrame of adjusted close prices.
        :param risk_free_rate: The risk-free rate, default is 0.0 (for simplicity).
        :return: daily_returns (DataFrame), cov_matrix (DataFrame)
        """
        daily_returns = data.pct_change(fill_method=None).dropna()
        
        cov_matrix = daily_returns.cov()
        
        return daily_returns, cov_matrix
    
    @staticmethod
    def run_monte_carlo_simulation(daily_returns, cov_matrix, num_portfolios=100_000, 
                                   risk_free_rate=0.0):
        """
        Runs the Monte Carlo simulation to generate a large number of random portfolios,
        calculates their performance metrics (annualized return, volatility, Sharpe ratio),
        and returns a DataFrame of results as well as an array of the weight vectors.
    
        :param daily_returns: DataFrame of asset daily returns.
        :param cov_matrix: Covariance matrix of asset daily returns.
        :param num_portfolios: Number of random portfolios to simulate.
        :param risk_free_rate: Risk-free rate to be used in Sharpe ratio calculation.
        :return: (simulated_portfolios, weights_record)
        """
        
        results = np.zeros((4, num_portfolios))
        weights_record = np.zeros((len(daily_returns.columns), num_portfolios))
        
        for i in range(num_portfolios):
            weights = np.random.random(len(daily_returns.columns))
            weights /= np.sum(weights)
            weights_record[:, i] = weights
    
            portfolio_return = np.sum(weights * daily_returns.mean()) * RiskOptima.TRADING_DAYS
    
            portfolio_stddev = np.sqrt(
                np.dot(weights.T, np.dot(cov_matrix, weights))
            ) * np.sqrt(RiskOptima.TRADING_DAYS)
    
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_stddev
    
            results[0, i] = portfolio_return
            results[1, i] = portfolio_stddev
            results[2, i] = sharpe_ratio
            results[3, i] = i
    
        columns = ['Return', 'Volatility', 'Sharpe Ratio', 'Simulation']
        simulated_portfolios = pd.DataFrame(results.T, columns=columns)
        
        return simulated_portfolios, weights_record
    
    @staticmethod
    def get_market_statistics(market_ticker, start_date, end_date, risk_free_rate=0.0):
        """
        Downloads data for a market index (e.g., SPY), then calculates its
        annualized return, annualized volatility, and Sharpe ratio.
        """
        market_data = yf.download([market_ticker], start=start_date, end=end_date, progress=False)['Close']
        
        if isinstance(market_data, pd.DataFrame):
            market_data = market_data[market_ticker] 
        
        market_daily_returns = market_data.pct_change(fill_method=None).dropna()
    
        market_return = market_daily_returns.mean() * RiskOptima.TRADING_DAYS
        market_volatility = market_daily_returns.std(axis=0) * np.sqrt(RiskOptima.TRADING_DAYS)
        market_sharpe_ratio = (market_return - risk_free_rate) / market_volatility
    
        if hasattr(market_return, 'iloc'):
            market_return = market_return.iloc[0]
        if hasattr(market_volatility, 'iloc'):
            market_volatility = market_volatility.iloc[0]
        if hasattr(market_sharpe_ratio, 'iloc'):
            market_sharpe_ratio = market_sharpe_ratio.iloc[0]
    
        return market_return, market_volatility, market_sharpe_ratio
    
    @staticmethod
    def portfolio_performance(weights, mean_returns, cov_matrix, trading_days=252):
        """
        Given weights, return annualized portfolio return and volatility.
        """
        returns = np.sum(mean_returns * weights) * trading_days
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(trading_days)
        return returns, volatility
    
    @staticmethod
    def min_volatility(weights, mean_returns, cov_matrix):
        """
        Objective function: we want to minimize volatility.
        """
        return RiskOptima.portfolio_performance(weights, mean_returns, cov_matrix)[1]
    
    @staticmethod
    def efficient_frontier(mean_returns, cov_matrix, num_points=50):
        """
        Calculates the Efficient Frontier by iterating over possible target returns
        and finding the portfolio with minimum volatility for each target return.
        Returns arrays of frontier volatilities, returns, and the corresponding weights.
        """
        results = []
        target_returns = np.linspace(mean_returns.min(), mean_returns.max(), num_points)
        
        num_assets = len(mean_returns)
        init_guess = num_assets * [1. / num_assets,]
        bounds = tuple((0,1) for _ in range(num_assets))
        
        for ret in target_returns:
            constraints = (
                {'type':'eq', 'fun': lambda w: np.sum(w) - 1}, 
                {'type':'eq', 'fun': lambda w: RiskOptima.portfolio_performance(w, mean_returns, cov_matrix)[0] - ret}
            )
            
            result = minimize(RiskOptima.min_volatility, 
                              init_guess, 
                              args=(mean_returns, cov_matrix),
                              method='SLSQP',
                              bounds=bounds,
                              constraints=constraints)
            if result.success:
                vol = RiskOptima.portfolio_performance(result.x, mean_returns, cov_matrix)[1]
                results.append((vol, ret, result.x))
        
        results = sorted(results, key=lambda x: x[0])
        
        frontier_volatility = [res[0] for res in results]
        frontier_returns = [res[1] for res in results]
        frontier_weights = [res[2] for res in results]
        
        return frontier_volatility, frontier_returns, frontier_weights
    
    @staticmethod
    def get_previous_working_day():
        """
        Returns the most recent weekday date in 'YYYY-MM-DD' format.
        If today is Monday-Friday, returns today.
        If today is Saturday, returns Friday.
        If today is Sunday, returns Friday.
        """
        today = date.today()
        # Monday=0, Tuesday=1, ..., Saturday=5, Sunday=6
        if today.weekday() == 5:      # Saturday
            today -= timedelta(days=1)
        elif today.weekday() == 6:    # Sunday
            today -= timedelta(days=2)
        return today.strftime('%Y-%m-%d')
    
    @staticmethod
    def calculate_portfolio_allocation(investment_allocation):
        """
        Normalize portfolio allocations based on the investment amounts provided.
    
        :param dict investment_allocation: A dictionary mapping stock tickers to their investment amounts (e.g., {'AAPL': 1000, 'MSFT': 2000}).
        :return: List of stock tickers and a numpy array of normalized weights.
        """
        total_investment = sum(investment_allocation.values())
        normalized_weights = np.array([amount / total_investment for amount in investment_allocation.values()])
        tickers = list(investment_allocation.keys())
        return tickers, normalized_weights
    
    @staticmethod
    def fetch_historical_stock_prices(tickers, start_date, end_date):
        """
        Retrieve historical stock price data for a list of tickers using Yahoo Finance.
    
        :param list tickers: List of stock ticker symbols.
        :param str start_date: Start date for historical data in 'YYYY-MM-DD' format.
        :param str end_date: End date for historical data in 'YYYY-MM-DD' format.
        :return: pandas DataFrame containing the adjusted closing prices for the specified tickers.
        """
        stock_data = yf.download(tickers, start=start_date, end=end_date, progress=False)
        return stock_data
    
    @staticmethod
    def perform_mean_variance_optimization(tickers, start_date, end_date, max_acceptable_volatility, predefined_returns=None, min_allocation=0.01, max_allocation=0.35, num_simulations=100000):
        """
        Execute mean-variance optimization using Monte Carlo simulation with weight constraints.
    
        :param list tickers: List of stock ticker symbols to optimize.
        :param str start_date: Start date for the historical data in 'YYYY-MM-DD' format.
        :param str end_date: End date for the historical data in 'YYYY-MM-DD' format.
        :param float max_acceptable_volatility: Maximum allowable annualized volatility for the portfolio.
        :param ndarray predefined_returns: (Optional) Predefined annualized returns for the tickers.
        :param float min_allocation: Minimum weight allocation for each stock.
        :param float max_allocation: Maximum weight allocation for each stock.
        :param int num_simulations: Number of Monte Carlo simulations to run.
        :return: Optimal portfolio weights as a numpy array.
        """
        # Fetch historical stock price data
        price_data = RiskOptima.fetch_historical_stock_prices(tickers, start_date, end_date)['Close']
        if price_data.empty:
            raise ValueError("No historical data retrieved. Verify the tickers and date range.")
    
        # Calculate daily returns
        daily_returns = price_data.pct_change(fill_method=None).dropna()
    
        # Calculate expected annualized returns if not provided
        if predefined_returns is None:
            predefined_returns = daily_returns.mean() * RiskOptima.TRADING_DAYS
    
        # Compute the annualized covariance matrix
        covariance_matrix = daily_returns.cov() * RiskOptima.TRADING_DAYS
    
        simulation_results = np.zeros((4, num_simulations))
        weight_matrix = np.zeros((len(tickers), num_simulations))
    
        # Perform Monte Carlo simulations
        for i in range(num_simulations):
            random_weights = np.random.uniform(min_allocation, max_allocation, len(tickers))
            random_weights /= np.sum(random_weights)
    
            weight_matrix[:, i] = random_weights
    
            portfolio_return = np.sum(random_weights * predefined_returns)
            portfolio_volatility = np.sqrt(np.dot(random_weights.T, np.dot(covariance_matrix, random_weights)))
            sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
    
            simulation_results[:, i] = [portfolio_return, portfolio_volatility, sharpe_ratio, i]
    
        result_columns = ['Annualized Return', 'Annualized Volatility', 'Sharpe Ratio', 'Simulation Index']
        simulation_results_df = pd.DataFrame(simulation_results.T, columns=result_columns)
    
        feasible_portfolios = simulation_results_df[simulation_results_df['Annualized Volatility'] <= max_acceptable_volatility]
    
        if feasible_portfolios.empty:
            raise ValueError("No portfolio satisfies the maximum volatility constraint.")
    
        optimal_index = feasible_portfolios['Sharpe Ratio'].idxmax()
    
        return weight_matrix[:, int(optimal_index)]
  
    @staticmethod
    def add_features(stock_prices):
        """
        Add technical indicators like moving averages to the stock data.
        :param stock_prices: DataFrame of stock prices.
        :return: DataFrame with additional feature columns.
        """
        features = pd.DataFrame(stock_prices)
        features['5_day_avg'] = stock_prices.rolling(window=5).mean()
        features['10_day_avg'] = stock_prices.rolling(window=10).mean()
        features['Close'] = stock_prices
        return features
    
    
    @staticmethod
    def create_lagged_features(data, lag_days=5):
        """
        Create lagged features for machine learning models.
        :param data: DataFrame containing the stock prices.
        :param lag_days: Number of lag days to include.
        :return: DataFrame with lagged features and target variable.
        """
        lagged_data = data.copy()
        for lag in range(1, lag_days + 1):
            lagged_data[f'lag_{lag}'] = lagged_data['Close'].shift(lag)
        lagged_data.dropna(inplace=True)
        return lagged_data
    
    @staticmethod
    def evaluate_model(model, X, y):
        """
        Evaluate the model using cross-validation and calculate the average performance metrics.
        :param model: The machine learning model to evaluate.
        :param X: Feature matrix.
        :param y: Target variable.
        :return: Cross-validation score and mean squared error.
        """
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
        model.fit(X, y)
        predictions = model.predict(X)
        mse = mean_squared_error(y, predictions)
        return np.mean(cv_scores), mse
    
    @staticmethod
    def predict_with_model(model, feature_data):
        """
        Predict stock returns using the trained model.
        :param model: Trained machine learning model.
        :param feature_data: DataFrame of features for prediction.
        :return: Predicted stock return.
        """
        scaler = StandardScaler()
        feature_data_scaled = scaler.fit_transform(feature_data)
        predictions = model.predict(feature_data_scaled)
        return predictions[-1]  # Return the last prediction as the future return
    
    
    @staticmethod
    def generate_stock_predictions(ticker, start_date, end_date, model_type='Linear Regression'):
        """
        Generate stock return predictions and model confidence using a specified model type.
        :param ticker: Stock ticker symbol.
        :param start_date: Start date for the historical data (YYYY-MM-DD).
        :param end_date: End date for the historical data (YYYY-MM-DD).
        :param model_type: Choice of machine learning model ('Linear Regression', 'Random Forest', 'Gradient Boosting').
        :return: Tuple of predicted return and model confidence.
        """
        # Fetch and preprocess stock data
        stock_prices = RiskOptima.download_data_yfinance(ticker, start_date, end_date)
        enriched_data = RiskOptima.add_features(stock_prices)
        prepared_data = RiskOptima.create_lagged_features(enriched_data)
    
        # Separate features and target variable
        X = prepared_data.drop('Close', axis=1)
        y = prepared_data['Close']
    
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
        # Impute missing values
        imputer = SimpleImputer(strategy='mean')
        X_train = imputer.fit_transform(X_train)
        X_test = imputer.transform(X_test)
    
        # Select machine learning model
        if model_type == 'Random Forest':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_type == 'Gradient Boosting':
            model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        elif model_type == 'Linear Regression':
            model = LinearRegression()
        elif model_type == 'XGBoost':
            model = XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=3)
        elif model_type == 'SVR':
            model = SVR(kernel='rbf', C=1.0, epsilon=0.1)
        else:
            raise ValueError("Invalid model type. Choose from 'Linear Regression', 'Random Forest', or 'Gradient Boosting'.")
    
        # Train and evaluate the model
        avg_cv_score, mse = RiskOptima.evaluate_model(model, X_train, y_train)
    
        # Predict future returns
        predicted_return = RiskOptima.predict_with_model(model, X_test)
        
        return predicted_return, avg_cv_score
    
    @staticmethod
    def black_litterman_adjust_returns(market_returns, investor_views, view_confidences, historical_prices, tau=0.025):
        """
        Adjust market returns based on investor views and their confidences using the Black-Litterman model.
    
        :param dict market_returns: Expected market returns for each asset.
        :param dict investor_views: Investor's views on the expected returns of assets.
        :param dict view_confidences: Confidence levels for each investor view.
        :param pandas.DataFrame historical_prices: Historical price data for calculating covariance matrix.
        :param float tau: Market equilibrium uncertainty factor (default 0.025).
        :return: Numpy array of adjusted returns for each asset.
        """
        num_assets = len(market_returns)
    
        # Create proportion matrix P and views vector Q
        proportion_matrix = np.eye(num_assets)  # Identity matrix for simplicity
        views_vector = np.array(list(investor_views.values())).reshape(-1, 1)
    
        # Compute the covariance matrix from historical prices
        covariance_matrix = historical_prices['Close'].pct_change(fill_method=None).dropna().cov()
    
        # Compute Omega (diagonal matrix of view confidences)
        omega_matrix = np.diag([tau / confidence for confidence in view_confidences.values()])
    
        # Apply the Black-Litterman formula
        inv_tau_cov = np.linalg.inv(tau * covariance_matrix)
        inv_omega = np.linalg.inv(omega_matrix)
    
        adjusted_returns = np.linalg.inv(inv_tau_cov + proportion_matrix.T @ inv_omega @ proportion_matrix)
        adjusted_returns = adjusted_returns @ (
            inv_tau_cov @ np.array(list(market_returns.values())).reshape(-1, 1) + proportion_matrix.T @ inv_omega @ views_vector
        )
    
        return adjusted_returns.flatten()
    
    @staticmethod
    def compute_market_returns(market_capitalizations, market_index_return):
        """
        Calculate market returns for individual assets based on market capitalizations and index return.
    
        :param dict market_capitalizations: Market capitalizations of assets.
        :param float market_index_return: Return of the overall market index.
        :return: Dictionary mapping tickers to their computed market returns.
        """
        total_market_cap = sum(market_capitalizations.values())
        return {
            ticker: (cap / total_market_cap) * market_index_return
            for ticker, cap in market_capitalizations.items()
        }
    
    @staticmethod
    def sortino_ratio(returns, risk_free_rate):
        """
        Calculate the Sortino Ratio for a set of investment returns.
    
        :param returns: pandas Series or numpy array of investment returns.
        :param float risk_free_rate: Annualized risk-free rate (e.g., yield on government bonds).
        :return: float Sortino Ratio (returns 0 if downside risk is zero).
        """
        trading_days = RiskOptima.get_trading_days()
        excess_returns = returns - (risk_free_rate / trading_days)
        downside_returns = np.minimum(excess_returns, 0)
        annualized_excess_return = np.mean(excess_returns) * trading_days
        annualized_downside_std_dev = np.std(downside_returns) * np.sqrt(trading_days)
    
        # Return 0 if downside standard deviation is zero
        if (annualized_downside_std_dev == 0).all():  # Use `.all()` for Series comparison
            return 0.0
    
        return annualized_excess_return / annualized_downside_std_dev
    @staticmethod
    def information_ratio(returns, benchmark_returns):
        """
        Calculate the Information Ratio for a set of investment returns against a benchmark.
    
        :param returns: pandas Series or numpy array of portfolio returns.
        :param benchmark_returns: pandas Series or numpy array of benchmark returns.
        :return: float Information Ratio.
        """
        # Ensure inputs are Series
        if isinstance(returns, pd.DataFrame):
            if returns.shape[1] > 1:
                raise ValueError("`returns` must be a pandas Series or 1D numpy array, not a DataFrame with multiple columns.")
            returns = returns.squeeze()
    
        if isinstance(benchmark_returns, pd.DataFrame):
            if benchmark_returns.shape[1] > 1:
                raise ValueError("`benchmark_returns` must be a pandas Series or 1D numpy array, not a DataFrame with multiple columns.")
            benchmark_returns = benchmark_returns.squeeze()
    
        # Ensure alignment of indices
        common_index = returns.index.intersection(benchmark_returns.index)
        returns = returns.loc[common_index]
        benchmark_returns = benchmark_returns.loc[common_index]
    
        trading_days = RiskOptima.get_trading_days()
    
        # Compute active returns and tracking error
        active_returns = returns - benchmark_returns
    
        if np.allclose(active_returns, 0):  # If active returns are effectively zero
            return 0.0  # Explicitly return 0 for identical returns
    
        annualized_active_return = np.mean(active_returns) * trading_days
        tracking_error = np.std(active_returns) * np.sqrt(trading_days)
    
        if tracking_error == 0:  # Avoid division by zero
            return 0.0
    
        # Return single statistic
        return annualized_active_return / tracking_error

    @staticmethod
    def correlation_with_market(portfolio_returns, market_returns):
        """
        Calculate the correlation between portfolio returns and market index returns.

        :param portfolio_returns: pandas Series of portfolio returns.
        :param market_returns: pandas Series of market index returns.
        :return: float Correlation coefficient.
        """
        common_dates = portfolio_returns.index.intersection(market_returns.index)
        portfolio_aligned = portfolio_returns.loc[common_dates]
        market_aligned = market_returns.loc[common_dates]
        return portfolio_aligned.corr(market_aligned)
    
    @staticmethod
    def add_table_to_plot(ax, dataframe, column_descriptions=None, column_colors=None, x=1.15, y=0.2, fontsize=8, column_width=0.50):
        """
        Adds a table to the plot with consistent row heights and optional column colors.
        
        :param ax: The matplotlib Axes object.
        :param dataframe: The pandas DataFrame to display as a table.
        :param column_descriptions: Optional list of column header descriptions to override the defaults.
        :param column_colors: List of colors for the table columns. Must match the number of columns in the dataframe.
        :param x: The x-position of the table in Axes coordinates.
        :param y: The y-position of the table in Axes coordinates.
        :param fontsize: Font size for the table text.
        """
        dataframe_reset = dataframe.reset_index()

        if column_descriptions is not None:
            dataframe_reset.columns = column_descriptions

        num_rows = len(dataframe_reset) + 1
        row_height = 0.040  # Fixed height per row (adjust as needed)
        table_height = num_rows * row_height

        table_data = [dataframe_reset.columns.to_list()] + dataframe_reset.values.tolist()

        table = ax.table(
            cellText=table_data,
            colLabels=None,  
            colLoc="center",
            loc="right",
            bbox=[x, y, column_width, table_height],  # [left, bottom, width, height] with dynamic height
            cellLoc="center"
        )

        table.auto_set_font_size(False)
        table.set_fontsize(fontsize)

        table.auto_set_column_width(col=list(range(len(dataframe_reset.columns))))

        header_color = "#f2f2f2"  # Light gray background
        for col_index in range(len(dataframe_reset.columns)):
            cell = table[(0, col_index)]  
            cell.set_text_props(weight="bold") 
            cell.set_facecolor(header_color)  
            cell.set_edgecolor("black")  

        for (row, col), cell in table.get_celld().items():
            if row == 0:
                continue
            cell.set_edgecolor("black")
            cell.set_linewidth(0.5)

            if column_colors and col < len(column_colors):
                cell.set_facecolor(column_colors[col])

        return table
    
    @staticmethod
    def consolidate_stats_to_dataframe(titles, stats_lists):
        """
        Converts multiple sets of statistics into a single DataFrame for table display.

        :param titles: A list of titles for the columns (e.g., ["ML & MV Optimized Portfolio", "MV Optimized Portfolio"]).
        :param stats_lists: A list of stats lists, where each stats_list corresponds to a title.
                            Example: [["Sharpe Ratio: 1.95", ...], ["Sharpe Ratio: 1.50", ...]]
        :return: A pandas DataFrame with metrics as rows and titles as columns.
        """

        metrics = [stat.split(":")[0].strip() for stat in stats_lists[0]]

        columns = {}
        for title, stats_list in zip(titles, stats_lists):
            values = [stat.split(":")[1].strip() for stat in stats_list]
            columns[title] = values

        df = pd.DataFrame(columns, index=metrics)
        df.index.name = "Metric"
        return df
    
    @staticmethod
    def add_portfolio_terms_explanation(ax, x=0.02, y=0.02, fontsize=10):
        """
        Adds an explanation for portfolio-related terms to the chart.

        :param ax: The matplotlib Axes object where the explanation will be added.
        :param x: The x-coordinate of the text box in Axes coordinates (default: 0.02).
        :param y: The y-coordinate of the text box in Axes coordinates (default: 0.02).
        :param fontsize: Font size for the text (default: 10).
        """

        explanation_text = (
            "Portfolio Terms Explanation:\n"
            "1. Return: The expected gain or loss from an investment. Higher is better.\n"
            "2. Volatility: A measure of risk based on price fluctuations. Lower is safer.\n"
            "3. Sharpe Ratio: Measures risk-adjusted return using total volatility. Higher is better.\n"
            "4. Risk-Free Rate: The theoretical return of an investment with zero risk.\n"
            "5. Capital Market Line (CML): Shows risk-return combinations of efficient portfolios.\n"
            "6. Global Minimum Variance Portfolio: Portfolio with the lowest possible volatility.\n"
            "7. Optimal Portfolio: Portfolio with the best risk-return trade-off based on Sharpe Ratio.\n"
            "8. Naive Portfolio: Equal-weighted portfolio, used as a baseline for comparison."
        )

        ax.text(
            x, y,
            explanation_text,
            transform=ax.transAxes,
            fontsize=fontsize,
            verticalalignment='bottom',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'),
            ha='left'
        )
    
    @staticmethod
    def plot_efficient_frontier(simulated_portfolios, weights_record, assets, 
                                market_return, market_volatility, market_sharpe, 
                                daily_returns, cov_matrix,
                                risk_free_rate=0.0, title='Efficient Frontier',
                                current_weights=None,
                                current_labels=None,
                                start_date='2020-01-01', end_date='2023-01-01'):
        
        x_ticks = np.linspace(0, 0.15, 16)  # Adjust the range and number of ticks as needed
        y_ticks = np.linspace(0, 0.30, 16)  # Adjust the range and number of ticks as needed
        
        fig, ax = plt.subplots(figsize=(22, 10))
        
        fig.subplots_adjust(right=0.95)

        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.1f}%'.format(x * 100)))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1f}%'.format(y * 100)))

        sc = ax.scatter(
            simulated_portfolios['Volatility'], 
            simulated_portfolios['Return'], 
            c=simulated_portfolios['Sharpe Ratio'], 
            cmap='plasma', 
            alpha=0.5,
            label='Simulated Portfolios'
        )

        fig.colorbar(sc, ax=ax, label='Sharpe Ratio')

        ax.set_xlabel('Volatility')
        ax.set_ylabel('Return')
        ax.set_title(title)

        ax.scatter(
            market_volatility, market_return,
            color='red', marker='o', s=100,
            label='Market Benchmark (S&P 500)'
        )

        optimal_idx = simulated_portfolios['Sharpe Ratio'].idxmax()
        optimal_portfolio = simulated_portfolios.loc[optimal_idx]
        optimal_weights = weights_record[:, optimal_idx]

        annual_returns = daily_returns.mean() * RiskOptima.get_trading_days()
        annual_cov = daily_returns.cov() * RiskOptima.get_trading_days()
        
        n_points = 50
        show_cml = True
        show_ew = True
        show_gmv = True
        
        RiskOptima.plot_ef_ax(
            n_points=n_points,
            expected_returns=annual_returns,
            cov=annual_cov,
            style='.-',
            legend=False,
            show_cml=show_cml,
            riskfree_rate=risk_free_rate,
            show_ew=show_ew,
            show_gmv=show_gmv,
            ax=ax
        )
        
        # Add major and minor grid lines
        ax.grid(visible=True, which='major', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
        ax.grid(visible=True, which='minor', linestyle=':', linewidth=0.4, color='lightgray', alpha=0.5)

        # Ensure grid lines appear below data
        ax.set_axisbelow(True)
        
        if current_weights is not None:
            curr_portfolio_return = np.sum(current_weights * daily_returns.mean()) * RiskOptima.get_trading_days()
            curr_portfolio_vol = np.sqrt(
                np.dot(current_weights.T, np.dot(daily_returns.cov(), current_weights))
            ) * np.sqrt(RiskOptima.get_trading_days())

            current_sharpe = (curr_portfolio_return - risk_free_rate) / curr_portfolio_vol
            
            ax.scatter(
                curr_portfolio_vol,
                curr_portfolio_return,
                color='black',    
                marker='s',        
                s=150,             
                label='My Current Portfolio'
            )

        ax.scatter(
            optimal_portfolio['Volatility'], 
            optimal_portfolio['Return'],
            color='green', marker='*', s=200,
            label='Optimal Portfolio'
        )

        ax.legend(
            loc='upper center',
            bbox_to_anchor=(0.5, -0.08),
            fancybox=True,
            shadow=True,
            ncol=3
        )

        portfolio_df = pd.DataFrame({
            "Security": current_labels,
            "Current\nPortfolio Weights": current_weights,
            "Optimal\nPortfolio Weights": optimal_weights
        })
        
        # Set the Security column as the index
        portfolio_df.set_index("Security", inplace=True)
        
        # Convert weights to percentages for better readability
        portfolio_df = portfolio_df.apply(lambda col: col.map(lambda x: f"{x * 100:.2f}%"))

        RiskOptima.add_table_to_plot(ax, portfolio_df, x=1.15, y=0.52, column_width=0.50)

        titles = [
            "My Current\nPortfolio",
            "Optimized\nOptimized Portfolio",
            "Market Benchmark\n(S&P 500)"
        ]
        
        # Corresponding statistics lists
        stats_lists = [
            [
                f"Return: {curr_portfolio_return*100:.2f}%",
                f"Volatility: {curr_portfolio_vol*100:.2f}%",
                f"Sharpe Ratio: {current_sharpe:.2f}",
                f"Risk Free Rate: {risk_free_rate*100:.2f}%"
            ],      
            [
                f"Return: {optimal_portfolio['Return']*100:.2f}%",
                f"Volatility: {optimal_portfolio['Volatility']*100:.2f}%",
                f"Sharpe Ratio: {optimal_portfolio['Sharpe Ratio']:.2f}",
                f"Risk Free Rate: {risk_free_rate*100:.2f}%"
            ],        
            [
                f"Return: {market_return*100:.2f}%",
                f"Volatility: {market_volatility*100:.2f}%",
                f"Sharpe Ratio: {market_sharpe:.2f}",
                f"Risk Free Rate: {risk_free_rate*100:.2f}%"            
            ]
        ]
        
        # Convert to DataFrame
        stats_df = RiskOptima.consolidate_stats_to_dataframe(titles, stats_lists)

        RiskOptima.add_table_to_plot(ax, stats_df, None, None, x=1.15, y=0.30)

        RiskOptima.add_portfolio_terms_explanation(ax, x=1.15, y=0.00, fontsize=10)

        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f"efficient_frontier_monter_carlo_{timestamp}.png", dpi=300, bbox_inches='tight')
        plt.show()
        
    @staticmethod
    def add_stats_text_box(ax, title, stats_list, x=1.19, y=0.34, color='green', fontsize=10):
        """
        Adds a styled text box with statistics to the plot.

        :param ax: The matplotlib Axes object where the text box will be added.
        :param title: The title of the text box (e.g., "ML & MV Optimized Portfolio").
        :param stats_list: A list of strings with the statistics to display.
        :param x: The x-coordinate of the text box in Axes coordinates (default: 1.19).
        :param y: The y-coordinate of the text box in Axes coordinates (default: 0.34).
        :param color: The edge color of the text box (default: 'green').
        :param fontsize: The font size for the text (default: 10).
        """
        # Combine the title and statistics into a single string
        stats_text = title + ":\n" + "\n".join(stats_list)

        # Add the text box to the plot
        ax.text(
            x, y,
            stats_text,
            transform=ax.transAxes,
            fontsize=fontsize,
            verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor=color, facecolor='white'),
            ha='left'
        )        
        
    @staticmethod
    def add_ratio_explanation(ax, x=0.02, y=0.02, fontsize=10):
        """
        Adds an explanation for Sharpe Ratio, Sortino Ratio, and Info Ratio to the chart.

        :param ax: The matplotlib Axes object where the explanation will be added.
        :param x: The x-coordinate of the text box in Axes coordinates (default: 0.02).
        :param y: The y-coordinate of the text box in Axes coordinates (default: 0.02).
        :param fontsize: Font size for the text (default: 10).
        """
        # Prepare the explanation text
        explanation_text = (
            "Ratio Explanations:\n"
            "1. Sharpe Ratio: Measures risk-adjusted return using total volatility. Higher is better.\n"
            "2. Sortino Ratio: Focuses on downside risk-adjusted returns. Higher is better.\n"
            "3. Info Ratio: Measures portfolio performance vs. a benchmark. Higher is better."
        )

        # Add the text box to the plot
        ax.text(
            x, y,
            explanation_text,
            transform=ax.transAxes,
            fontsize=fontsize,
            verticalalignment='bottom',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'),
            ha='left'
        )
        
    @staticmethod
    def setup_chart_aesthetics(start_date="2023-12-01", end_date="2025-01-01"):
        sns.set_palette("bright")
        
        fig, ax = plt.subplots(figsize=(20, 12))
        
        fig.subplots_adjust(right=0.95)
        
        #plt.figure(figsize=(20, 12))
        #ax = plt.gca()
        ax.set_xlim(pd.Timestamp(start_date), pd.Timestamp(end_date))
        colors = sns.color_palette()

        # Increase gridlines and date labels
        major_locator = AutoDateLocator(minticks=10, maxticks=15)  # Automatically adjust the number of ticks
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_minor_locator(AutoDateLocator(minticks=20, maxticks=30))  # More granular minor ticks

        # Set x-axis formatter for dates
        ax.xaxis.set_major_formatter(DateFormatter("%Y/%m/%d"))  # Format: 'yyyy/MM/dd'

        # Tilt the date labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Increase gridlines on the y-axis
        ax.yaxis.set_major_locator(MultipleLocator(5))  # Major ticks every 5%
        ax.yaxis.set_minor_locator(MultipleLocator(1))  # Minor ticks every 1%

        # Set grid lines for both major and minor ticks
        ax.grid(visible=True, which='major', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
        ax.grid(visible=True, which='minor', linestyle=':', linewidth=0.4, color='lightgray', alpha=0.5)
        ax.set_axisbelow(True)
        
        # Format the y-axis as percentages
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2f}%'.format(y)))

        # Add an external border around the chart
        rect = patches.Rectangle(
            (0, 0), 1, 1, transform=ax.transAxes,  # Normalized coordinates
            linewidth=2, edgecolor='black', facecolor='none'
        )
        ax.add_patch(rect)
        
        return ax, plt, colors