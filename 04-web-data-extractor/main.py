import argparse
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_data(url):
    headers = {
        "User-Agent": "PortfolioDataExtractor/1.0"
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    records = []

    for link in soup.find_all("a", href=True):
        text = " ".join(link.get_text(" ", strip=True).split())
        href = urljoin(url, link["href"])

        if text:
            records.append({
                "text": text,
                "url": href
            })

    return records


def main():
    parser = argparse.ArgumentParser(
        description="Extract public link text and URLs from a permitted webpage."
    )
    parser.add_argument("url", help="URL to process")
    parser.add_argument(
        "--output",
        default="extracted_links.csv",
        help="Output CSV filename"
    )
    args = parser.parse_args()

    try:
        records = extract_data(args.url)
        df = pd.DataFrame(records)
        df.to_csv(args.output, index=False)

        print(f"Extracted {len(records)} links.")
        print(f"Saved results to: {args.output}")

    except requests.RequestException as error:
        print(f"Request failed: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
