import requests
from bs4 import BeautifulSoup

url = "https://arxiv.org/list/astro-ph.CO/new"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
