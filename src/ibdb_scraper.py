import requests
from bs4 import BeautifulSoup


def scrape_production(url):
    """
    Scrape basic production metadata from an IBDB Broadway production page.
    """

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/131.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    )

    soup = BeautifulSoup(response.text, "html.parser")

    production = {}

    # Extract production ID
    production["production_id"] = url.split("-")[-1]

    # Extract production title
    title = soup.find("h3", class_="title-label")

    if title:
        production["title"] = title.get_text(strip=True)
    else:
        production["title"] = None


    # Extract metadata
    metadata_labels = [
        "Opening Date",
        "Closing Date",
        "Performances"
    ]

    for label in metadata_labels:
        element = soup.find(
            "div",
            class_="xt-lable",
            string=lambda text: text and text.strip() == label
        )

        if element:
            value = element.find_next(
                "div",
                class_="xt-main-title"
            )

            if value:
                production[label.lower().replace(" ", "_")] = (
                    value.get_text(strip=True)
                )


    return production

if __name__ == "__main__":

    url = "https://www.ibdb.com/broadway-production/oklahoma-1285"

    print("Scraping...")

    production = scrape_production(url)

    print(production)