import logging
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ArxivScraper:
    def __init__(self, base_url: str = "https://arxiv.org"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_page_content(self, url: str) -> str:
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return ""


# url = "https://arxiv.org/list/astro-ph.CO/new"
# page = requests.get(url)
# soup = BeautifulSoup(page.text, "html.parser")


# papers = []
# dl = soup.find("dl")
# dts = dl.find_all("dt")
# dds = dl.find_all("dd")

# for dt, dd in zip(dts, dds):
#     paper = {}

#     # ID
#     paper["arxiv_id"] = dt.find("a", {"title": "Abstract"}).text.strip()
#     # Title
#     paper["title"] = (
#         dd.find("div", {"class": "list-title"}).text.replace("Title:", "").strip()
#     )
#     # Authors
#     paper["authors"] = dd.find("div", {"class": "list-authors"}).text
#     # Get comments if exist
#     comments_div = dd.find("div", {"class": "list-comments"})
#     paper["comments"] = (
#         comments_div.text.replace("Comments:", "").strip()
#         if comments_div
#         else "No Comment"
#     )
#     # Get subject if exist
#     subjects_div = dd.find("div", {"class": "list-subjects"})
#     paper["subjects"] = (
#         subjects_div.text.replace("Subjects:", "").strip()
#         if subjects_div
#         else "No Subject"
#     )
#     # Get abstract of paper
#     paper["abstract"] = dd.find("p", {"class": "mathjax"}).text.strip()
#     # Make a pdf link using arxiv_id
#     paper["pdf_link"] = f"https://arxiv.org/pdf/{paper['arxiv_id']}"

#     papers.append(paper)
#     # Sleep for server
#     time.sleep(0.1)

# df = pd.DataFrame(papers)
# df.to_csv("arixic_papers.csv", index=False)
# print(f"Scraped {len(papers)} papers")
