"""Retrieve every book from the Flask API in pages of ten."""

import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

BOOKS_URL = os.getenv("BOOK_API_URL", "http://127.0.0.1:5000/api/books")
PAGE_SIZE = 10


def fetch_all_books():
    """Fetch pages until the API returns an empty list."""
    all_books = []
    page = 1

    while True:
        query = urlencode({"page": page, "limit": PAGE_SIZE})
        with urlopen(f"{BOOKS_URL}?{query}", timeout=5) as response:
            current_page = json.load(response)

        if not current_page:
            break

        print(f"Page {page}: {len(current_page)} books")
        all_books.extend(current_page)
        page += 1

    return all_books


if __name__ == "__main__":
    downloaded_books = fetch_all_books()
    print(f"Fetched {len(downloaded_books)} books in total.")
