from typing import Union
import re
from urllib.request import urlopen
from urllib.error import HTTPError
import pprint
import bs4
import requests


pp = pprint.PrettyPrinter(indent=4)

# from config.config import AMAZON_HOSTNAME
AMAZON_HOSTNAME = "https://www.amazon.com.br"


class Amazon:
    def get_book_url(self, book_title: str) -> Union[str, None]:
        url = f"{AMAZON_HOSTNAME}/s?k={book_title.lower().replace(' ', '+')}&s=review-rank"
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36",
            "Accept-Language": "en-US, en;q=0.5",
        }
        # search_page = requests.get(url, headers=HEADERS)
        search_page = urlopen(url)
        search_soup = bs4.BeautifulSoup(search_page, "html.parser")
        found_name = None
        for i in range(1, 49):
            book_search = search_soup.find(
                "div", {"cel_widget_id": f"MAIN-SEARCH_RESULTS-{i}"}
            )
            try:
                for item in book_search.find(
                    "span", {"class": "a-size-base-plus a-color-base a-text-normal"}
                ):
                    found_name = item
                if found_name and book_title.lower().replace(
                    " ", ""
                ) in found_name.lower().replace(" ", ""):
                    break
            except Exception as e:
                continue
        if found_name is None:
            return None
        book_url = book_search.find("a")["href"]
        while book_url is None:
            book_url = self.get_book_url(book_title)
        return book_url

    def get_book_price(self, book_url) -> float:
        book_page = urlopen(f"{AMAZON_HOSTNAME}{book_url}")
        book_soup = bs4.BeautifulSoup(book_page, "html.parser")
        price = book_soup.find("span", {"class": "a-size-medium a-color-price"}).text
        return price.replace(" ", "")


if __name__ == "__main__":
    book_url = Amazon().get_book_url("O Hobbit")
    print(book_url)
    book_price = Amazon().get_book_price(book_url)
    print(book_price)
