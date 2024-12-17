# Arxiv Web Scraping

This Python project provides a multi-category web scraper for arxiv.org. It extracts details about academic papers from specific categories on Arxiv and stores the results in CSV files for further analysis.

## Features

- Scrapes paper information from multiple categories on Arxiv.org.
- Collects essential paper data such as title, authors, abstract, categories, and more.
- Automatically saves scraped data into CSV files for each category.
- Implements rate limiting and retry logic to avoid hitting Arxiv's servers too frequently.
- Supports asynchronous scraping for faster processing.

## Installation

The project is managed with [Poetry](https://python-poetry.org/) for dependency management. To get started, clone the repository and install the dependencies:

```bash
git clone https://github.com/shahinabdi/maktabkhooneh.git
cd maktabkhooneh/CH02/arxiv-web-scraping
poetry install
```

### Requirements

- Python 3.11 or higher
- The required libraries will be installed automatically via Poetry.

## Configuration

The scraper can be customized via the `ArxivConfig` class. By default, it scrapes papers from the following categories:

- `astro-ph.CO`
- `astro-ph.EP`
- `astro-ph.GA`
- `astro-ph.HE`
- `astro-ph.IM`
- `astro-ph.SR`

You can change these categories or adjust other settings by modifying the `ArxivConfig` class. Available settings include:

- `base_url`: The base URL for Arxiv (default: `https://arxiv.org`).
- `categories`: A list of categories to scrape (default includes various astronomy-related topics).
- `output_dir`: The directory to save the output CSV files (default: `output`).
- `rate_limit`: The number of requests allowed per second (default: 3).
- `max_retries`: Maximum number of retries for failed requests (default: 3).
- `timeout`: Timeout for each HTTP request (default: 30 seconds).
- `user_agent`: The user agent string used for requests (default: `ArxivScrapper/2.0`).

## Usage

To run the scraper, execute the following command:

```bash
poetry run python basic_scraper.py
```

The script will scrape the paper details from each category and save them as CSV files in the `output` directory.

### Example Output

The scraper will create files with names like:

```
arxiv_astro_ph_CO_20241217.csv
arxiv_astro_ph_EP_20241217.csv
```

Each file contains the scraped information for the corresponding category.

## Rate Limiting and Retries

This scraper uses the following strategies to avoid overloading the Arxiv server:

- **Rate Limiting**: It makes at most 3 requests per second.
- **Retries**: If a request fails due to network issues or timeouts, the scraper will retry the request up to 3 times with exponential backoff.

## Logging

The scraper logs its activities to a file (`arxiv_scraper.log`) and outputs information to the console. Logs include:

- Successful paper retrievals.
- Errors during scraping or saving data.

## Contributing

Contributions are welcome! If you find bugs or want to add new features, feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or inquiries, feel free to contact the author at:

- Shahin ABDI <contact@shahinabdi.fr>
