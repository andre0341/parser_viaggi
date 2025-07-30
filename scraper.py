import re
import sqlite3
import requests
from bs4 import BeautifulSoup

URL = "https://offerte.caesartour.it/last-second.aspx"
DB_PATH = "db.sqlite"

# regex to parse offer information from text block
OFFER_RE = re.compile(
    r"""
    (?P<country>[\w\s]+)\s*-\s*(?P<name>.*?)\s+
    (?P<date>\d{2}/\d{2}/\d{4})\s+da\s+(?P<airport>.*?)\s+
    (?P<duration>\d+\s+notti).*?
    (?P<formula>AI|BB|HB|FB|RO|\w{2})?.*?
    €(?P<price>[\d\.]+)
    (?:.*?\bTRF\b)?
    """,
    re.VERBOSE | re.IGNORECASE,
)


def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT,
            name TEXT,
            date TEXT,
            duration TEXT,
            airport TEXT,
            price REAL,
            formula TEXT,
            transfer INTEGER
        )"""
    )
    conn.commit()
    conn.close()


def save_offer(info):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO offers(country,name,date,duration,airport,price,formula,transfer)
        VALUES(?,?,?,?,?,?,?,?)""",
        (
            info.get("country"),
            info.get("name"),
            info.get("date"),
            info.get("duration"),
            info.get("airport"),
            info.get("price"),
            info.get("formula"),
            info.get("transfer"),
        ),
    )
    conn.commit()
    conn.close()


def parse_offers(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".last-second-item, .offer")
    for item in items:
        text = item.get_text(" ", strip=True)
        match = OFFER_RE.search(text)
        if match:
            data = match.groupdict()
            data["price"] = float(data["price"].replace(".", ""))
            data["transfer"] = 1 if "TRF" in text.upper() else 0
            save_offer(data)


def main():
    create_db()
    try:
        resp = requests.get(URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {URL}: {e}")
        return
    parse_offers(resp.text)


if __name__ == "__main__":
    main()
