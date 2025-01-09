# securities.py
"""
This module contains class definition of a Securities.
"""


class Securities:
    """
    This class defines a Securities.

    It has the following 2 key attributes:
    - price: instant price of the securities.
    - symbol: code of the securities.
    """

    def __init__(self, name, symbol, price, currency):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.currency = currency

    def get_price(self):
        """get the price of the securities"""
        return self.price

    def set_price(self, price):
        """set the price of the securities"""
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.symbol}): {self.price} {self.currency}"


if __name__ == "__main__":
    # create a stock object
    stock = Securities("Apple Inc.", "AAPL", 145.12, "USD")

    # print the stock object
    print(stock)

    # set the price of the stock
    stock.set_price(150.0)

    # print the stock object
    print(stock)
