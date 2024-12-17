import csv
import logging
import time
from datetime import datetime
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("arxiv_scraper.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class ArxivScraper:
    """Scraper for extracting paper information from arxiv.org"""

    def __init__(self, base_url: str = "https://arxiv.org"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_page_content(self, url: str) -> str:
        """Fetch page content"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return ""

    def parse_paper_info(self, dt_element, dd_element) -> Dict:
        """Extract paper information from dt and dd elements"""
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
        """Scrape papers from a specific category"""
        url = f"{self.base_url}/list/{category}/new"
        logger.info(f"Scraping category: {category}")

        page_content = self.get_page_content(url)
        if not page_content:
            return []

        soup = BeautifulSoup(page_content, "html.parser")
        papers = []
        dl_element = soup.find("dl")
        if dl_element:
            dt_elements = dl_element.find_all("dt")
            dd_elements = dl_element.find_all("dd")

            for dt, dd in zip(dt_elements, dd_elements):
                paper_info = self.parse_paper_info(dt, dd)
                if paper_info:
                    papers.append(paper_info)
        logger.info(f"Found {len(papers)} papers in category {category}")
        return papers

    def save_to_csv(self, papers: List[Dict], filename: str):
        """Save scraped papers to CSV file"""
        if not papers:
            logger.warning("No papers to save")
            return

        try:
            fieldnames = papers[0].keys()
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(papers)
            logger.info(f"Successfully saved {len(papers)} papers to {filename}")
        except IOError as e:
            logger.error(f"Error saving to CSV: {str(e)}")


def main():
    categories = [
        "astro-ph.CO",
        "astro-ph.EP",
        "astro-ph.GA",
        "astro-ph.HE",
        "astro-ph.IM",
        "astro-ph.SR",
    ]
    scraper = ArxivScraper()

    for category in categories:
        papers = scraper.scrape_category(category)
        if papers:
            filename = f"arxiv_{category.replace('.', '_')}_{datetime.now().strftime('%Y-%m-%d')}.csv"
            scraper.save_to_csv(papers, filename)


if __name__ == "__main__":
    main()
