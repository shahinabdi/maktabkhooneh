# Dictionary Commperhension
# Pythonic

prices = {"apple": 2.30, "banana": 1.99, "orange": 2.34}
taxed_prices = {fruit: price * 1.2 for fruit, price in prices.items()}

print(taxed_prices)
