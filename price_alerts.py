class PriceAlert:
    alerts = []

    def __init__(self, target_price, price_aggregator):
        self.target_price = target_price
        self.price_aggregator = price_aggregator
        PriceAlert.alerts.append(self)
        self.triggered = False

    def check(self):
        current_price = self.price_aggregator.get_average_price()
        if current_price and current_price >= self.target_price and not self.triggered:
            self.triggered = True
            return True
        return False

    def send_notification(self):
        print(f"Alert: Bitcoin price has reached or exceeded ${self.target_price:.2f}")

def set_price_alert(target_price, price_aggregator):
    return PriceAlert(target_price, price_aggregator)

def check_price_alert(alert):
    return alert.check()
