class Book:
    def __init__(self, title, author, publication_year):
        self.title = title
        self.author = author
        self.publication_year = publication_year

    def show_author(self, author):
        return f"Author: {author}"

    def show_publication_year(self, publication_year):
        return f"Publication Year: {publication_year}"

    def get_info(self):
        return f"Title: {self.title}, Author: {self.author}, Publication Year: {self.publication_year}"

