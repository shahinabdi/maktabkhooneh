import time

import requests
from bs4 import BeautifulSoup

url = "https://arxiv.org/list/astro-ph.CO/new"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")


papers = []
dl = soup.find("dl")
dts = dl.find_all("dt")
dds = dl.find_all("dd")

for dt, dd in zip(dts, dds):
    paper = {}

    # ID
    paper["arxiv_id"] = dt.find("a", {"title": "Abstract"}).text.strip()
    # Title
    paper["title"] = (
        dd.find("div", {"class": "list-title"}).text.replace("Title:", "").strip()
    )
    # Authors
    paper["authors"] = dd.find("div", {"class": "list-authors"}).text
    # Get comments if exist
    comments_div = dd.find("div", {"class": "list-comments"})
    paper["comments"] = (
        comments_div.text.replace("Comments:", "").strip()
        if comments_div
        else "No Comment"
    )
    # Get subject if exist
    subjects_div = dd.find("div", {"class": "list-subjects"})
    paper["subjects"] = (
        subjects_div.text.replace("Subjects:", "").strip()
        if subjects_div
        else "No Subject"
    )
    # Get abstract of paper
    paper["abstract"] = dd.find("p", {"class": "mathjax"}).text.strip()
    # Make a pdf link using arxiv_id
    paper["pdf_link"] = f"https://arxiv.org/pdf/{paper['arxiv_id']}"

    papers.append(paper)
    # Sleep for server
    time.sleep(0.1)
