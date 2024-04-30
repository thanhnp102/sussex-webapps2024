"""
This is the API for currency exchange
"""

import requests

currency_list = {"EUR":"Euro","USD":"US Dollar","JPY":"Japanese Yen","BGN":"Bulgarian Lev","CZK":"Czech Republic Koruna","DKK":"Danish Krone","GBP":"British Pound Sterling","HUF":"Hungarian Forint","PLN":"Polish Zloty","RON":"Romanian Leu","SEK":"Swedish Krona","CHF":"Swiss Franc","ISK":"Icelandic Króna","NOK":"Norwegian Krone","HRK":"Croatian Kuna","RUB":"Russian Ruble","TRY":"Turkish Lira","AUD":"Australian Dollar","BRL":"Brazilian Real","CAD":"Canadian Dollar","CNY":"Chinese Yuan","HKD":"Hong Kong Dollar","IDR":"Indonesian Rupiah","ILS":"Israeli New Sheqel","INR":"Indian Rupee","KRW":"South Korean Won","MXN":"Mexican Peso","MYR":"Malaysian Ringgit","NZD":"New Zealand Dollar","PHP":"Philippine Peso","SGD":"Singapore Dollar","THB":"Thai Baht","ZAR":"South African Rand"}


def get_list():
    choices = []
    for c, n in currency_list.items():
        choices.append((c, f"{c} - {n}"))
    return choices


def convert_currency(base_currency="GBP"):
    url = f'http://127.0.0.1:8000/conversion/{base_currency}'

    res = requests.get(url)
    res.raise_for_status()
    if res.status_code == 200:
        exchange = res.json().get("data")
        return exchange
