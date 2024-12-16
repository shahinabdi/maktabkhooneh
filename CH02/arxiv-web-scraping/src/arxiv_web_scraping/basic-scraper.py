import logging
import time
from datetime import datetime
from typing import Dict, List

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

    def parse_paper_info(self, dt_element, dd_element) -> Dict:
        try:
            arxiv_id = dt_element.find("a", {"title": "Abstract"}).text.strip()
            arxiv_id = arxiv_id.replace("arXiv:", "").strip()

            title_element = dd_element.find("div", {"class": "list-title"})
            title = title_element.text.replace("Title:", "").strip()

            authors_element = dd_element.find("div", {"class": "list-authors"})
            authors = authors_element.text.strip()

            comments_element = dd_element.find("div", {"class": "list-comments"})
            comments = (
                comments_element.text.replace("Comments:", "").strip()
                if comments_element
                else "No comments"
            )

            subjects_element = dd_element.find("div", {"class": "list-subjects"})
            subjects = (
                subjects_element.text.replace("Subjects:", "").strip()
                if subjects_element
                else "No subjects"
            )

            abstract = dd_element.find("p", {"class": "mathjax"}).text.strip()

            pdf_link = f"{self.base_url}/pdf/{arxiv_id}"

            return {
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "comments": comments,
                "subjects": subjects,
                "abstract": abstract,
                "link": pdf_link,
                "scrape_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        except Exception as e:
            logger.error(f"Error parsing paper entry: {str(e)}")
            return {}

    def scrape_category(self, category: str) -> List[Dict]:
        url = f"{self.base_url}/list/{category}/new"
        logger.info(f"Scraping category: {category}")

        page_content = self.get_page_content(url)
        if not page_content:
            return []

        soup = BeautifulSoup(page_content.text, "html.parser")
        papers = []
        dl_element = soup.find("dl")
        if dl_element:
            dt_elements = dt_element.find_all("dt")
            dd_elements = dd_element.find_all("dd")

            for dt, dd in zip(dt_elements, dd_elements):
                paper_info = parse_paper_info(dt, dd)
                if paper_info:
                    papers.append(paper_info)
        logger.info(f"Found {len(papers)} papers in category {category}")
        return papers


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
