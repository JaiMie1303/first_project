import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CurrenciesConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f"Валюта {base} не найдена!")

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise ConvertionException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://v6.exchangerate-api.com/v6/034d318f6d0821b1be6b9429/pair/{base_key}/{quote_key}")

        resp = json.loads(r.content)
        new_price = resp['conversion_rate'] * amount

        return new_price