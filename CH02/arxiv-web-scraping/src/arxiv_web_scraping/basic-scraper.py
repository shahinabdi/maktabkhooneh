import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import aiohttp
import backoff
import pandas as pd
import requests
from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("arxiv_scraper.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


@dataclass
class ArxivConfig:
    """Configuration for ArxivScraper"""

    base_url: str = "https://arxiv.org"
    categories: List[str] = None
    output_dir: str = "output"
    rate_limit: int = 3
    max_retries: int = 3
    timeout: int = 30
    user_agent: str = "ArxivScrapper/2.0"

    def __post_init__(self):
        if self.categories is None:
            self.categories = [
                "astro-ph.CO",
                "astro-ph.EP",
                "astro-ph.GA",
                "astro-ph.HE",
                "astro-ph.IM",
                "astro-ph.SR",
            ]


class ArxivPaper:
    def __init__(self, data: Dict):
        self.arxiv_id: str = data.get("arxiv_id", "")
        self.title: str = data.get("title", "")
        self.authors: List[str] = data.get("authors", [])
        self.abstract: str = data.get("abstract", "")
        self.categories: List[str] = data.get("categories", [])
        self.primary_category: str = data.get("primary_category", "")
        self.comments: str = data.get("comments", "")
        self.pdf_url: str = data.get("pdf_url", "")
        self.scrape_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        """Convert paper to dictionary"""
        return {
            "arxiv_id": self.arxiv_id,
            "title": self.title,
            "authors": ";".join(self.authors),
            "abstract": self.abstract,
            "categories": ";".join(self.categories),
            "primary_category": self.primary_category,
            "comments": self.comments,
            "pdf_url": self.pdf_url,
            "scrape_date": self.scrape_date,
        }


class ArxivScraper:
    """Scraper for extracting paper information from arxiv.org"""

    def __init__(self, config: ArxivConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        Path(config.output_dir).mkdir(parents=True, exist_ok=True)

    async def __aenter__(self):
        """Set up async context manager"""
        self.session = aiohttp.ClientSession(
            headers={"User-Agent": self.config.user_agent}
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Clean up async context manager"""
        await self.session.close()

    @sleep_and_retry
    @limits(calls=3, period=1)
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=3,
    )
    async def fetch_page(self, url: str) -> str:
        async with self.session.get(url, timeout=self.config.timeout) as response:
            response.raise_for_status()
            return await response.text()

    def parse_paper_info(self, dt_element, dd_element) -> ArxivPaper:
        """Extract paper information from dt and dd elements"""
        try:
            arxiv_id = dt_element.find("a", {"title": "Abstract"}).text.strip()
            arxiv_id = arxiv_id.replace("arXiv:", "").strip()

            title_element = dd_element.find("div", {"class": "list-title"})
            title = (
                title_element.text.replace("Title:", "").strip()
                if title_element
                else "No Title"
            )

            authors_element = dd_element.find("div", {"class": "list-authors"})
            authors = (
                [a.text.strip() for a in authors_element.find_all("a")]
                if authors_element
                else []
            )

            comments_element = dd_element.find("div", {"class": "list-comments"})
            comments = (
                comments_element.text.replace("Comments:", "").strip()
                if comments_element
                else "No comments"
            )

            subjects_element = dd_element.find("div", {"class": "list-subjects"})
            categories = (
                [
                    c.strip()
                    for c in subjects_element.text.replace("Subjects:", "").split(";")
                ]
                if subjects_element
                else []
            )
            primary_category = categories[0] if categories else ""

            abstract = dd_element.find("p", {"class": "mathjax"}).text.strip()

            paper_data = {
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "categories": categories,
                "primary_category": primary_category,
                "comments": comments,
                "pdf_url": f"{self.config.base_url}/pdf/{arxiv_id}",
            }
            return ArxivPaper(paper_data)
        except Exception as e:
            logger.error(f"Error parsing paper entry: {str(e)}")
            return None

    async def scrape_category(self, category: str) -> List[ArxivPaper]:
        """Scrape papers from a specific category"""
        url = f"{self.config.base_url}/list/{category}/new"
        logger.info(f"Scraping category: {category}")

        try:
            html = await self.fetch_page(url)
            soup = BeautifulSoup(html, "html.parser")
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
        except Exception as e:
            logger.error(f"Error scraping category {category}: {str(e)}")
            return []

    def save_to_csv(self, papers: List[ArxivPaper], category: str):
        """Save scraped papers to CSV file"""
        if not papers:
            logger.warning(f"No papers to save for category {category}")
            return
        try:
            df = pd.DataFrame([paper.to_dict() for paper in papers])
            filename = (
                Path(self.config.output_dir)
                / f"arxiv_{category.replace('.','_')}_{datetime.now().strftime('%Y%m%d')}.csv"
            )
            df.to_csv(filename, index=False)
            logger.info(f"Successfully saved {len(papers)} papers to {filename}")
        except IOError as e:
            logger.error(f"Error saving to CSV: {str(e)}")


async def main():
    config = ArxivConfig()

    async with ArxivScraper(config) as scraper:
        tasks = [scraper.scrape_category(category) for category in config.categories]
        results = await asyncio.gather(*tasks)

        for category, papers in zip(config.categories, results):
            scraper.save_to_csv(papers, category)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Scrapping interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
