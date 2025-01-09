# currency.py
"""external module providing currency conversion utilities"""

from currency_converter.converter import CurrencyConverter


def convert_usd_to_eur(usd_amount: float) -> float:
    """
    Converts USD to EUR using the currency-converter-lite library.
    This library uses Google or Yahoo finance APIs and has caching feature.
    :param usd_amount: Amount in USD to convert
    :return: Equivalent amount in EUR
    """
    converter = CurrencyConverter()
    eur_amount = converter.convert(usd_amount, 'USD', 'EUR')
    return eur_amount


# Example usage
if __name__ == "__main__":
    eur = convert_usd_to_eur(100.00)
    if eur is not None:
        print(f"100.00 USD is equivalent to {eur:.2f} EUR.")
    else:
        print("Could not perform the conversion.")
