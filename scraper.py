"""Automated menu retrieval.

Works with the Antalya Bilim University cafeteria menu, which is published as a
weekly PDF (table: one column per weekday, one row per course). `menu_url` in
config.json can be either
  * the direct link to the menu PDF, or
  * the web page that lists the menu PDFs (the newest menu PDF is picked automatically).
"""
import io
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin

import pdfplumber
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (SmartMealGuide student project)"}
WEEKDAYS = ["PAZARTESİ", "SALI", "ÇARŞAMBA", "PERŞEMBE", "CUMA", "CUMARTESİ", "PAZAR"]
# Row order used in the cafeteria's menu table
COURSES = ["Soup", "Main", "Rice / Pasta", "Vegetable dish", "Salad", "Dessert / Fruit"]


def _clean(text) -> str:
    return " ".join(str(text or "").replace("\n", " ").split())


def _upper_tr(text: str) -> str:
    return text.replace("i", "İ").replace("ı", "I").upper()


def download(url: str) -> bytes:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.content


def find_menu_pdf(page_html: str, base_url: str) -> str | None:
    """Return the first (newest) menu PDF link found on a web page."""
    soup = BeautifulSoup(page_html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        label = _upper_tr(_clean(a.get_text()) + " " + href)
        if ".pdf" in href.lower() and any(k in label for k in ("YEMEK", "MENÜ", "MENU")):
            return urljoin(base_url, href)
    for a in soup.find_all("a", href=True):  # fallback: any PDF on the page
        if ".pdf" in a["href"].lower():
            return urljoin(base_url, a["href"])
    return None


def parse_menu_pdf(pdf_bytes: bytes) -> list[dict]:
    """Parse the weekly menu table into [{date, day, dishes:[{name, course}]}]."""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ""
        tables = page.extract_tables()

    m = re.search(r"(\d{1,2}\.\d{1,2}\.\d{4})\s*[-–]\s*(\d{1,2}\.\d{1,2}\.\d{4})", text)
    week_start = datetime.strptime(m.group(1), "%d.%m.%Y") if m else None

    for table in tables:
        rows = [[_clean(c) for c in row] for row in table]
        header_idx = next((i for i, r in enumerate(rows)
                           if sum(_upper_tr(c) in WEEKDAYS for c in r) >= 3), None)
        if header_idx is None:
            continue
        header = rows[header_idx]
        menu = []
        for col, day_name in enumerate(header):
            day = _upper_tr(day_name)
            if day not in WEEKDAYS:
                continue
            date = (week_start + timedelta(days=WEEKDAYS.index(day))).strftime("%d.%m.%Y") if week_start else ""
            dishes = []
            for r_i, row in enumerate(rows[header_idx + 1:]):
                if col < len(row) and row[col]:
                    course = COURSES[r_i] if r_i < len(COURSES) else "Other"
                    dishes.append({"name": row[col], "course": course})
            menu.append({"date": date, "day": day_name.title(), "dishes": dishes})
        return menu
    return []


def parse_menu_html(html: str) -> list[dict]:
    """Fallback for menus published as an HTML table (first column = date)."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    menu = []
    if table:
        for row in table.find_all("tr")[1:]:
            cells = [_clean(c.get_text()) for c in row.find_all("td")]
            if len(cells) >= 2:
                menu.append({"date": cells[0], "day": "",
                             "dishes": [{"name": d, "course": ""} for d in cells[1:] if d]})
    return menu


def get_menu(url: str) -> tuple[list[dict], str]:
    """Download and parse the menu. Returns (menu, source_url)."""
    content = download(url)
    if content[:4] == b"%PDF":
        return parse_menu_pdf(content), url
    html = content.decode("utf-8", errors="ignore")
    pdf_url = find_menu_pdf(html, url)
    if pdf_url:
        return parse_menu_pdf(download(pdf_url)), pdf_url
    return parse_menu_html(html), url


def get_menu_from_file(path) -> list[dict]:
    with open(path, "rb") as f:
        return parse_menu_pdf(f.read())
