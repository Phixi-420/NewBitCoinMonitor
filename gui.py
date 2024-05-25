import tkinter as tk
from tkinter import messagebox
from real_time_update import RealTimePriceUpdater
from price_alerts import set_price_alert, PriceAlert
from data_aggregation import PriceAggregator
from data_fetcher import CoinGeckoFetcher, CoinMarketCapFetcher

class BitcoinPriceMonitorGUI:
    def __init__(self, root, price_aggregator):
        self.root = root
        self.price_aggregator = price_aggregator
        self.root.title("Bitcoin Price Monitor")
        self.create_widgets()
        self.real_time_updater = RealTimePriceUpdater(price_aggregator)
        self.real_time_updater.start_updating()
        self.start_price_update()
        self.start_alert_checking()

    def create_widgets(self):
        self.price_label = tk.Label(self.root, text="Loading...", font=("Helvetica", 16))
        self.price_label.pack(pady=10)

        self.refresh_button = tk.Button(self.root, text="Refresh Price", command=self.manual_refresh)
        self.refresh_button.pack(pady=5)

        self.alert_label = tk.Label(self.root, text="Set Price Alert:", font=("Helvetica", 12))
        self.alert_label.pack(pady=5)

        self.alert_entry = tk.Entry(self.root)
        self.alert_entry.pack(pady=5)

        self.set_alert_button = tk.Button(self.root, text="Set Alert", command=self.set_alert)
        self.set_alert_button.pack(pady=5)

    def set_alert(self):
        try:
            target_price = float(self.alert_entry.get())
            set_price_alert(target_price, self.price_aggregator)
            messagebox.showinfo("Alert Set", f"Alert set for ${target_price}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    def update_price_label(self):
        avg_price = self.real_time_updater.get_current_price()
        if avg_price is not None:
            self.price_label.config(text=f"Current Bitcoin Price: ${avg_price:.2f}")
        else:
            self.price_label.config(text="Error fetching price")
        self.root.after(60000, self.update_price_label)

    def manual_refresh(self):
        avg_price = self.price_aggregator.get_average_price()
        if avg_price is not None:
            self.price_label.config(text=f"Current Bitcoin Price: ${avg_price:.2f}")
            messagebox.showinfo("Price Refreshed", f"Price manually refreshed: ${avg_price:.2f}")
        else:
            self.price_label.config(text="Error fetching price")
            messagebox.showerror("Error", "Failed to fetch the price")

    def check_alerts(self):
        for alert in PriceAlert.alerts:
            if alert.check():
                alert.send_notification()
        self.root.after(60000, self.check_alerts)

    def start_price_update(self):
        self.root.after(1000, self.update_price_label)

    def start_alert_checking(self):
        self.root.after(60000, self.check_alerts)

if __name__ == "__main__":
    root = tk.Tk()
    coingecko_fetcher = CoinGeckoFetcher("CoinGecko", "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    coinmarketcap_fetcher = CoinMarketCapFetcher("CoinMarketCap", "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC", api_key="")
    price_aggregator = PriceAggregator([coingecko_fetcher, coinmarketcap_fetcher])
    app = BitcoinPriceMonitorGUI(root, price_aggregator)
    root.mainloop()
