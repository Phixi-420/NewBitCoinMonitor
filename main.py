import tkinter as tk
from data_fetcher import CoinGeckoFetcher, CoinMarketCapFetcher
from data_aggregation import PriceAggregator
from gui import BitcoinPriceMonitorGUI

def main():
    root = tk.Tk()
    coingecko_fetcher = CoinGeckoFetcher("CoinGecko", "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    coinmarketcap_fetcher = CoinMarketCapFetcher("CoinMarketCap", "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC", api_key="YOUR_CMC_API_KEY")
    price_aggregator = PriceAggregator([coingecko_fetcher, coinmarketcap_fetcher])
    app = BitcoinPriceMonitorGUI(root, price_aggregator)
    root.mainloop()

if __name__ == "__main__":
    main()
