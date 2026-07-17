import re

from bs4 import BeautifulSoup


def extract_performer_id(url: str) -> str | None:
    """
    Extract an IBDB performer ID from a performer URL.

    Example
    -------
    /broadway-cast-staff/alfred-drake-4031 -> 4031
    """

    match = re.search(
        r"-(\d+)/?$",
        url
    )

    if match:
        return match.group(1)

    return None


def extract_opening_cast(soup: BeautifulSoup) -> list[dict]:
    """
    Extract the opening-night cast from an IBDB production page.

    Parameters
    ----------
    soup : BeautifulSoup
        Parsed production page.

    Returns
    -------
    list[dict]
        One dictionary per performer.
    """

    cast_section = soup.find(id="OpeningNightCast")

    if cast_section is None:
        return []

    cast = []

    cast_rows = cast_section.find_all(
        "div",
        class_="row mobile-a-align"
    )

    for row in cast_rows:

        performer = row.find(
            "a",
            href=re.compile(r"/broadway-cast-staff/")
        )

        if performer is None:
            continue

        performer_id = extract_performer_id(
            performer["href"]
        )

        if performer_id is None:
            continue

        columns = row.find_all(
            "div",
            class_="col m4 s12"
        )

        character = None

        if len(columns) > 1:
            character = columns[1].get_text(strip=True)

        cast.append(
            {
                "performer_id": performer_id,
                "performer_name": performer.get_text(strip=True),
                "character": character,
            }
        )

    return cast