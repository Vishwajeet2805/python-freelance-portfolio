# Web Data Extraction Tool

A small Python utility that extracts publicly visible link text and URLs from a webpage and exports the results to CSV.

## Features

- Accepts a URL from the command line
- Uses a clear User-Agent
- Handles HTTP failures and timeouts
- Resolves relative links to absolute URLs
- Exports structured CSV data
- Uses reusable functions

## Tech Stack

- Python
- Requests
- BeautifulSoup
- Pandas

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Use a website that permits automated access, or a local/demo page:

```bash
python main.py https://example.com
```

Custom output:

```bash
python main.py https://example.com --output results.csv
```

## Output

The tool creates a CSV containing:

- `text`
- `url`

## Responsible Use

Only extract publicly accessible information from websites where automated access is permitted. Respect robots.txt, terms of service, rate limits, copyright, and privacy requirements. Do not bypass CAPTCHAs, authentication, paywalls, access controls, or anti-bot protections.

## Portfolio Highlights

This project demonstrates HTTP requests, HTML parsing, URL handling, structured data extraction, CSV export, and error handling.
