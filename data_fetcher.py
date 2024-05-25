import requests

class DataFetcher:
    def __init__(self, source_name, api_url, headers=None):
        self.source_name = source_name
        self.api_url = api_url
        self.headers = headers

    def fetch_price(self):
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return self.parse_price(response.json())
        except requests.RequestException as e:
            print(f"Error fetching data from {self.source_name}: {e}")
            return None

    def parse_price(self, data):
        raise NotImplementedError("Subclasses should implement this method")

class CoinGeckoFetcher(DataFetcher):
    def parse_price(self, data):
        return data["bitcoin"]["usd"]

class CoinMarketCapFetcher(DataFetcher):
    def __init__(self, source_name, api_url, api_key):
        headers = {"X-CMC_PRO_API_KEY": api_key}
        super().__init__(source_name, api_url, headers)

    def parse_price(self, data):
        return data["data"]["BTC"]["quote"]["USD"]["price"]
