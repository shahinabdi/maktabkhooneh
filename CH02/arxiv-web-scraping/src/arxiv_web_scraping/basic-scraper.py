import requests
from bs4 import BeautifulSoup

url = "https://arxiv.org/list/astro-ph.CO/new"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")


papers = []
dl = soup.find("dl")
dts = dl.find_all("dt")
dds = dl.find_all("dd")

dt = dts[0]
arxiv_id = dt.find("a", {"title": "Abstract"}).text.strip()
print(arxiv_id)
dd = dds[1]
print(dd.find("div", {"class": "list-title"}).text.replace("Title:", "").strip())

print(dd.find("div", {"class": "list-authors"}).text)

print(dd.find("div", {"class": "list-comments"}).text.replace("Comments:", "").strip())

print(dd.find("div", {"class": "list-subjects"}).text.replace("Subjects:", "").strip())

print(dd.find("p", {"class": "mathjax"}).text.strip())

print(f"https://arxiv.org/pdf/{arxiv_id}")
