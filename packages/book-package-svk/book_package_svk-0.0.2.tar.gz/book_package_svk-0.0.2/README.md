# Book Class Package

This is a simple Python package that defines a `Book` class with basic functionality to store and retrieve information about books.

## Features

- **Store Book Information**: Store a book's title, author, and publication year.
- **Show Author**: Retrieve the author of the book.
- **Show Publication Year**: Retrieve the publication year of the book.
- **Get Complete Book Info**: Retrieve a full description of the book, including title, author, and publication year.

## Installation

You can install this package from PyPI using `pip`:

```bash
pip install book_package_svk
```

### Usage
 ```python
from book_package_svk import Book

# Create a book instance
book = Book("1984", "George Orwell", 1949)

# Show the author's name
print(book.show_author(book.author))  # Output: Author: George Orwell

# Show the publication year
print(book.show_publication_year(book.publication_year))  # Output: Publication Year: 1949

# Get complete information about the book

print(book.get_info())  
# Output: Title: 1984, Author: George Orwell, Publication Year: 1949

 ```



