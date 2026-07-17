import re

import pandas as pd
from bs4 import BeautifulSoup

from .utils import get_page


def get_season_productions(season_id: int | str) -> pd.DataFrame:
    """
    Extract all Broadway productions listed for a season.

    Parameters
    ----------
    season_id : int or str
        IBDB season identifier.

    Returns
    -------
    pandas.DataFrame
        Production catalogue entries.
    """

    url = f"https://www.ibdb.com/season/{season_id}"

    response = get_page(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    rows = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        match = re.search(
            r"/broadway-production/.*-(\d+)/?$",
            href
        )

        if match:
            rows.append(
                {
                    "production_id": match.group(1),
                    "title": a.get_text(strip=True),
                    "url": "https://www.ibdb.com" + href,
                    "season_id": season_id,
                }
            )

    df = (
        pd.DataFrame(rows)
        .drop_duplicates("production_id")
        .reset_index(drop=True)
    )

    assert df["production_id"].is_unique
    assert df["production_id"].notna().all()

    return df