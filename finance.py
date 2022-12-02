import pandas as pd
from IPython.display import display
import requests
from alpha_vantage.timeseries import TimeSeries

api_key = "F71WF3729MHFB57L"

### Alpha Vantage: F71WF3729MHFB57L
## EODHistoricaldata: 6388da63ae6eb6.58329054


# def search_asset(asset, search_input, api_key):
#     url = f"https://eodhistoricaldata.com/api/search/{search_input}?api_token={api_key}&type={asset}"
#     results_json = requests.get(url).json()
#     results_df = (
#         pd.DataFrame(results_json)
#         .drop("ISIN", axis=1)
#         .rename(columns={"Code": "Symbol"})
#     )

#     return results_df


# assets = pd.DataFrame(
#     pd.Series(["stock", "etf", "fund", "bonds", "index", "commodity", "crypto"])
# ).rename(columns={0: "asset"})
# asset = input("Type of asset [stock, etf, fund, bonds, index, commodity, crypto]: ")

# if len(assets[assets.asset == asset]) == 0:
#     print("Input Error: Asset not found")
# else:
#     search_input = input(f"Search {asset}: ")
#     print(f"\nSearch Results for {search_input}\n")
#     print(asset)
#     print(search_input)
#     print(api_key)
#     search_results = search_asset(asset, search_input, api_key)
#     display(search_results)


ts = TimeSeries(
    key=api_key,
    output_format="pandas",
)

data = ts.get_daily_adjusted("MSFT")

print(data[0].head(30))
# print(data[0].describe())
# print(data[0].shape)
