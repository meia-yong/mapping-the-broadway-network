from bs4 import BeautifulSoup

from .utils import get_page


def extract_production_metadata(url: str) -> dict:
    """
    Extract production metadata from an IBDB production page.

    Parameters
    ----------
    url : str
        IBDB production URL.

    Returns
    -------
    dict
        Production metadata fields.
    """

    response = get_page(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    metadata = {}

    for label in soup.find_all(
        "div",
        class_="xt-lable"
    ):

        key = label.get_text(strip=True)

        value = label.find_next_sibling("div")

        if value:
            value = value.get_text(
                " ",
                strip=True
            )
        else:
            value = None

        metadata[key] = value

    return {
        "opening_date": metadata.get("Opening Date"),
        "closing_date": metadata.get("Closing Date"),
        "production_type": metadata.get("Production Type"),
    }