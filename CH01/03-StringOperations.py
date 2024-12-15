# Non Pythonic

result = ""
words = ["Hello", "World"]

for word in words:
    result += word + " "
result = result.strip()

print(result)
