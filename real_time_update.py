import threading
import time

class RealTimePriceUpdater:
    def __init__(self, price_aggregator, update_interval=60):
        self.price_aggregator = price_aggregator
        self.update_interval = update_interval
        self.current_price = None
        self.updating = False

    def start_updating(self):
        self.updating = True
        self.update_thread = threading.Thread(target=self._update_price, daemon=True)
        self.update_thread.start()

    def stop_updating(self):
        self.updating = False
        if self.update_thread.is_alive():
            self.update_thread.join()

    def _update_price(self):
        while self.updating:
            try:
                self.current_price = self.price_aggregator.get_average_price()
                print(f"Updated price: ${self.current_price:.2f}")
            except Exception as e:
                print(f"Error updating price: {e}")
            time.sleep(self.update_interval)

    def get_current_price(self):
        return self.current_price
