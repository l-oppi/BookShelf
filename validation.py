class BookValidation:
    def isbn10_digit(isbn: str) -> bool:
        isbn = isbn.replace("-", "")
        if len(isbn) != 9:
            isbn = "0" + isbn
        if isbn.isnumeric() != True:
            return None
        multiplier = 10
        result = 0
        for i in isbn[:-1]:
            result += int(i) * multiplier
            print(i)
            multiplier -= 1
        return 11 - (result % 11)

    def isbn10_validation(isbn: str) -> bool:
        isbn = isbn.replace("-", "")
        if len(isbn) != 10:
            isbn = "0" + isbn
        if isbn.isnumeric() != True:
            return False
        multiplier = 10
        result = 0
        for i in isbn:
            result += int(i) * multiplier
            multiplier -= 1
        return result % 11 == 0

    def isbn13_digit(isbn: str) -> bool:
        isbn = isbn.replace("-", "")
        if len(isbn) != 12:
            isbn = "0" + isbn
        if isbn.isnumeric() != True:
            return False
        cur_multiplier = 1
        result = 0
        for i in isbn:
            result += int(i) * cur_multiplier
            if cur_multiplier == 1:
                cur_multiplier = 3
            else:
                cur_multiplier = 1
        return 10 - (result % 10)

    def isbn13_validation(isbn: str) -> bool:
        isbn = isbn.replace("-", "")
        if len(isbn) != 13:
            isbn = "0" + isbn
        if isbn.isnumeric() != True:
            return False
        cur_multiplier = 1
        result = 0
        for i in isbn:
            result += int(i) * cur_multiplier
            if cur_multiplier == 1:
                cur_multiplier = 3
            else:
                cur_multiplier = 1
        return result % 10 == 0


if __name__ == "__main__":
    print(BookValidation.isbn10_validation("8501110361"))
    print(BookValidation.isbn13_validation("978-8501110367"))
