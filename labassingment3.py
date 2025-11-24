
"""
Clean and corrected version of the Library Inventory Manager
"""

from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from typing import List, Optional
from pathlib import Path
import logging
import sys
import traceback


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"  # "available" or "issued"

    def __post_init__(self):
        self.title = self.title.strip()
        self.author = self.author.strip()
        self.isbn = self.isbn.strip()
        if self.status not in ("available", "issued"):
            self.status = "available"

    def __str__(self) -> str:
        return f"{self.title} — {self.author} (ISBN: {self.isbn}) [{self.status}]"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Book":
        return cls(
            title=d.get("title", "").strip(),
            author=d.get("author", "").strip(),
            isbn=d.get("isbn", "").strip(),
            status=d.get("status", "available").strip()
        )

    def issue(self) -> None:
        if self.status == "issued":
            raise ValueError("Book already issued.")
        self.status = "issued"

    def return_book(self) -> None:
        if self.status == "available":
            raise ValueError("Book is not issued.")
        self.status = "available"

    def is_available(self) -> bool:
        return self.status == "available"


class LibraryInventory:
    def __init__(self, json_path: Optional[Path] = None):
        # Determine json_path
        if json_path:
            self.json_path = Path(json_path)
        else:
            self.json_path = Path.cwd() / "data" / "books.json"

        # Ensure directories exist
        self.json_path.parent.mkdir(parents=True, exist_ok=True)

        # Logging
        self._setup_logging()

        self.books: List[Book] = []
        try:
            self.load()
            logging.getLogger(__name__).info(f"Loaded inventory from {self.json_path}")
        except Exception as e:
            logging.getLogger(__name__).exception(f"Failed to load inventory: {e}")

    def _setup_logging(self):
        log_dir = Path.cwd() / "library_manager" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "library.log"

        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s"
        )

        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)


    def add_book(self, book: Book) -> None:
        if any(b.isbn == book.isbn for b in self.books):
            logging.getLogger(__name__).error(f"Duplicate ISBN {book.isbn}")
            raise ValueError("Book with same ISBN already exists.")
        self.books.append(book)
        logging.getLogger(__name__).info(f"Added book: {book}")

    def search_by_title(self, title_substr: str) -> List[Book]:
        s = title_substr.strip().lower()
        results = [b for b in self.books if s in b.title.lower()]
        return results

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        isbn = isbn.strip()
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> List[str]:
        return [str(b) for b in self.books]

    def issue_book_by_isbn(self, isbn: str) -> None:
        book = self.search_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found.")
        if not book.is_available():
            raise ValueError("Book already issued.")
        book.issue()
        self.save()

    def return_book_by_isbn(self, isbn: str) -> None:
        book = self.search_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found.")
        if book.is_available():
            raise ValueError("Book is not issued.")
        book.return_book()
        self.save()

    def save(self) -> None:
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=2, ensure_ascii=False)

    def load(self) -> None:
        if not self.json_path.exists():
            self.books = []
            self.save()
            return
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.books = [Book.from_dict(item) for item in data]


def prompt_nonempty(text: str) -> str:
    while True:
        s = input(text).strip()
        if s:
            return s
        print("Input cannot be empty.")


def print_header():
    print("=" * 60)
    print("Library Inventory Manager".center(60))
    print("=" * 60)


def cli_main():
    print_header()
    inv = LibraryInventory()

    MENU = """
1. Add Book
2. Issue Book
3. Return Book
4. View All Books
5. Search by Title
6. Search by ISBN
7. Exit
"""

    while True:
        try:
            print(MENU)
            choice = input("Enter choice (1-7): ").strip()

            if choice == "1":
                title = prompt_nonempty("Title: ")
                author = prompt_nonempty("Author: ")
                isbn = prompt_nonempty("ISBN: ")
                inv.add_book(Book(title, author, isbn))
                inv.save()
                print("Book added.")

            elif choice == "2":
                isbn = prompt_nonempty("ISBN to issue: ")
                inv.issue_book_by_isbn(isbn)
                print("Book issued.")

            elif choice == "3":
                isbn = prompt_nonempty("ISBN to return: ")
                inv.return_book_by_isbn(isbn)
                print("Book returned.")

            elif choice == "4":
                items = inv.display_all()
                if not items:
                    print("No books in inventory.")
                else:
                    for b in items:
                        print(" -", b)

            elif choice == "5":
                title = prompt_nonempty("Search title: ")
                results = inv.search_by_title(title)
                if not results:
                    print("No books found.")
                else:
                    for b in results:
                        print(" -", b)

            elif choice == "6":
                isbn = prompt_nonempty("Search ISBN: ")
                b = inv.search_by_isbn(isbn)
                print(b if b else "Book not found.")

            elif choice == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            print("Error:", e)
            print(traceback.format_exc())


if __name__ == "__main__":
    cli_main()
