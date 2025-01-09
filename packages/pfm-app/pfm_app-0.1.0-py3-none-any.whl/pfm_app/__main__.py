"""Module providing yahoo finance apis."""
import yfinance as yf

import pandas as pd

# TO-DO Nasdaq 100 Fund not working well, find a way to fix it
# TO-DO Currency conversion between USD and EUR

# define the stock tickers
tickers = [
    "ANDR.VI", "WIE.VI",
    "ASML.AS", "BC.MI",
    "V", "MSFT", "OTIS", "AMZN",
    "CSNDX.DE"]

# Define a mapping for stock exchanges from abbreviation to full name
exchange_mapping = {
    "NYQ": "New York Stock Exchange",
    "NMS": "NASDAQ Stock Market",
    "FRA": "Frankfurt Stock Exchange",
    "VIE": "Vienna Stock Exchange",
    "AMS": "Euronext Amsterdam",
    "MIL": "Milano Stock Exchange"
}

# initialize a list to store the stock data
stock_data = []

# loop through each ticker and fetch the stock information
for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info

    # extract stock fields
    name = info.get("longName", "N/A")
    price = info.get("currentPrice", "N/A")
    currency = info.get("currency", "N/A")
    exchange = info.get("exchange", "N/A")
    previous_close = info.get("regularMarketPreviousClose", "N/A")

    # Map the exchange abbreviation to the full name
    exchange_full_name = exchange_mapping.get(exchange, exchange)

    # Append the data to the list
    stock_data.append({
        "Stock Name": name,
        "Ticker": ticker,
        "Current Price": price,
        "Currency": currency,
        "Stock Exchange": exchange_full_name,
        "Previous Close": previous_close
    })

# Create a Dataframe from the stock data
df = pd.DataFrame(stock_data)

# specify target Excel file name
OUTPUT_FILE = "stock_data.xlsx"

# write the data to the Excel file
df.to_excel(OUTPUT_FILE, index=False, engine="openpyxl")

print(f"Stock data has been successfully saved to '{OUTPUT_FILE}'")


def main():
    """Entry point for the script."""
    print("Main flow of the script.")


if __name__ == "__main__":
    main()
