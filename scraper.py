"""Automated menu retrieval: downloads the cafeteria menu page and extracts dishes per day."""
import requests
from bs4 import BeautifulSoup


def fetch_html(url: str) -> str:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def parse_menu(html: str) -> list[dict]:
    """Parse a menu table: first column = date, other columns = dishes.

    NOTE: The selectors will be adapted to the real cafeteria website.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        return []
    menu = []
    for row in table.find_all("tr")[1:]:
        cells = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cells) >= 2:
            menu.append({"date": cells[0], "dishes": [d for d in cells[1:] if d]})
    return menu
