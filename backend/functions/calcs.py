import numpy as np 

def daily_return(historical_df):

        daily_returns = [None]

        for i in range(historical_df.shape[0] - 1):

            day_close = historical_df.loc[historical_df.index[i], 'Close']
            next_close = historical_df.loc[historical_df.index[i+1], 'Close']
            percent_change = ((next_close / day_close) - 1) * 100
            daily_returns.append(percent_change)

            return daily_returns

def asset_variance(historical_df, mean):

    variance = 0

    for i in range(historical_df.shape[0]):
        variance += (mean - historical_df.loc[historical_df.index[i], 'Percent Change']) ** 2
    
    variance /= historical_df.shape[0] - 1

    return variance


def find_covariances(list_of_returns):

    covariances = np.cov(list_of_returns, ddof=1)
    return covariances