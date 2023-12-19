import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#e1d8b9")
        self.style.configure("TLabel", background="#e1d8b9")
        self.style.configure("TButton", background="#4caf50")
        self.style.configure("TCombobox", background="#ffffff")

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10)

        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.from_currency_label = tk.Label(root, text="From:")
        self.from_currency_label.grid(row=1, column=0, padx=10, pady=10)

        self.from_currency_combobox = ttk.Combobox(root)
        self.from_currency_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.to_currency_label = tk.Label(root, text="To:")
        self.to_currency_label.grid(row=2, column=0, padx=10, pady=10)

        self.to_currency_combobox = ttk.Combobox(root)
        self.to_currency_combobox.grid(row=2, column=1, padx=10, pady=10)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.get_exchange_rates()

    def get_exchange_rates(self):
        try:
            url = "https://www.bnr.ro/Cursul-de-schimb-524.aspx"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            table = soup.find("table", class_="cursTable")
            rows = table.find_all("tr")

            exchange_rates = {}

            for row in rows:
                columns = row.find_all("td")
                if columns:
                    currency_name = columns[0].text.strip()
                    if currency_name != "Euro":
                        rate = float(columns[5].text.strip().replace(",", "."))
                        exchange_rates[currency_name] = rate

            currencies = list(exchange_rates.keys())
            self.from_currency_combobox["values"] = currencies
            self.to_currency_combobox["values"] = currencies

            return exchange_rates

        except Exception as e:
            print(f"Error getting exchange rates: {e}")
            return None

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency_combobox.get()
            to_currency = self.to_currency_combobox.get()

            exchange_rates = self.get_exchange_rates()

            if exchange_rates is not None:
                if from_currency in exchange_rates and to_currency in exchange_rates:
                    if from_currency == "RON":
                        result = amount * exchange_rates[to_currency]
                    else:
                        result = amount * exchange_rates[from_currency] / exchange_rates[to_currency]

                    self.result_label.config(text=f"{amount} {from_currency} = {result:.2f} {to_currency}")
                else:
                    self.result_label.config(text="Selected currencies do not have available exchange rates.")
            else:
                self.result_label.config(text="Error getting exchange rates.")
        except ValueError:
            self.result_label.config(text="Enter a valid amount.")

root = tk.Tk()
app = CurrencyConverterApp(root)

root.mainloop()
