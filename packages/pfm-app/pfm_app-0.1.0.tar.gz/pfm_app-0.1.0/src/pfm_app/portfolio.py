# portfolio.py
"""This file contains the Portfolio class which is used to store the stocks."""

from securities import Securities


class Portfolio:
    """
    This class defines a Portfolio.
    """

    def __init__(self):
        self.stocks = []

    def add_stock(self, stock):
        """Add a stock to the portfolio"""
        self.stocks.append(stock)

    def remove_stock(self, stock):
        """Remove a stock from the portfolio"""
        self.stocks.remove(stock)

    def total_value(self):
        """Calculate the total value of the portfolio"""
        return sum([stock.get_price() for stock in self.stocks])


if __name__ == "__main__":
    # create a stock object
    stock1 = Securities("Apple Inc.", "AAPL", 145.12, "USD")
    stock2 = Securities("Microsoft Corporation", "MSFT", 265.51, "USD")

    # create a portfolio object
    portfolio = Portfolio()

    # add the stocks to the portfolio
    portfolio.add_stock(stock1)
    portfolio.add_stock(stock2)

    # print the total value of the portfolio
    print(f"Total value of the portfolio: {portfolio.total_value()}")
