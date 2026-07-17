import re
import requests

from bs4 import BeautifulSoup

from .utils import get_page


def check_season_exists(season_id: int | str) -> bool:
    """
    Check whether an IBDB season page exists.
    """

    url = f"https://www.ibdb.com/season/{season_id}"

    try:
        response = get_page(url)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = soup.find("title")

        if title is None:
            return False

        return title.get_text(strip=True) != "Error"

    except requests.RequestException:
        return False


def get_season_label(season_id: int | str) -> str | None:
    """
    Extract season label such as 2019-2020.
    """

    url = f"https://www.ibdb.com/season/{season_id}"

    response = get_page(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text(
        " ",
        strip=True
    )

    match = re.search(
        r"\d{4}-\d{4}",
        text
    )

    if match:
        return match.group()

    return None