import requests
import pandas as pd

# Fetch Ethereum price data from Coin Metrics Community API
url = "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics"
params = {
    "assets": "eth",
    "metrics": "PriceUSD",
    "frequency": "1d",
    "start_time": "2023-01-01",
    "end_time": "2024-01-01"
}

response = requests.get(url, params=params)
data = response.json()
staking_rate = 0.04
base_value = 100

# Convert to DataFrame
df = pd.DataFrame(data['data'])
df['time'] = pd.to_datetime(df['time'])
df['price'] = df['PriceUSD'].astype(float)
df = df[['time', 'price']]

df['return'] = df['price']/df['price'].shift(1)

df['staking_index'] = base_value*(df['return'] + staking_rate).cumprod()
df.at[df.index[0], 'staking_index'] = base_value

print(df.head())