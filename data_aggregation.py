class PriceAggregator:
    def __init__(self, fetchers):
        self.fetchers = fetchers

    def get_average_price(self):
        prices = [fetcher.fetch_price() for fetcher in self.fetchers]
        valid_prices = [price for price in prices if price is not None]
        if not valid_prices:
            return None
        return sum(valid_prices) / len(valid_prices)
