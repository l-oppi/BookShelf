from typing import Union
import re
from urllib.request import urlopen
import bs4

HOSTNAME = "https://www.goodreads.com"


class Goodreads:
    def get_genres(self, soup) -> str:
        genres = []
        for node in soup.find_all("div", {"class": "left"}):
            current_genres = node.find_all(
                "a", {"class": "actionLinkLite bookPageGenreLink"}
            )
            current_genre = " > ".join([g.text for g in current_genres])
            if current_genre.strip():
                genres.append(current_genre)
        return genres

    def get_series_name(self, soup) -> str:
        series = soup.find(id="bookSeries").find("a")
        if series:
            series_name = re.search(r"\((.*?)\)", series.text).group(1)
            return series_name
        else:
            return ""

    def get_isbn(self, soup) -> Union[str, None]:
        try:
            isbn = re.findall(r"nisbn: [0-9]{10}", str(soup))[0].split()[1]
            return isbn
        except:
            return None

    def get_isbn13(self, soup) -> Union[str, None]:
        try:
            isbn13 = re.findall(r"nisbn13: [0-9]{13}", str(soup))[0].split()[1]
            return isbn13
        except:
            return None

    def get_num_pages(self, soup):
        if soup.find("span", {"itemprop": "numberOfPages"}):
            num_pages = soup.find("span", {"itemprop": "numberOfPages"}).text.strip()
            return int(num_pages.split()[0])
        return ""

    def get_year_first_published(self, soup) -> str:
        year_first_published = soup.find("nobr", attrs={"class": "greyText"})
        if year_first_published:
            year_first_published = year_first_published.string
            return re.search("([0-9]{3,4})", year_first_published).group(1)
        else:
            return ""

    def get_book_metadata(self, book_title: str) -> dict:
        url = f"{HOSTNAME}/search?q={book_title.replace(' ', '+')}"
        search_source = urlopen(url)
        search_soup = bs4.BeautifulSoup(search_source, "html.parser")
        book_path = search_soup.find("a", {"itemprop": "url"})["href"]
        book_url = f"{HOSTNAME}{book_path}"
        book_source = urlopen(book_url)
        book_soup = bs4.BeautifulSoup(book_source, "html.parser")
        return {
            "title": " ".join(book_soup.find("h1", {"id": "bookTitle"}).text.split()),
            "isbn": self.get_isbn(book_soup),
            "isbn13": self.get_isbn13(book_soup),
            "year_first_published": self.get_year_first_published(book_soup),
            "author": " ".join(
                book_soup.find("span", {"itemprop": "name"}).text.split()
            ),
            "num_pages": self.get_num_pages(book_soup),
            "rating": book_soup.find("span", {"itemprop": "ratingValue"}).text.strip(),
            "image_url": book_soup.find("img", {"id": "coverImage"})["src"],
        }


if __name__ == "__main__":
    # main()
    print(Goodreads().get_book_metadata("The Hobbit"))
