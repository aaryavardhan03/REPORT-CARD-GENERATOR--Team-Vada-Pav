# library.py

def get_library_info():
    """Collect library information."""
    issued_books = []
    count = int(input("Enter number of books issued: "))

    for i in range(count):
        book = input(f"Enter book {i+1} name: ")
        issued_books.append(book.title())

    fine = float(input("Enter fine amount (if any): ₹"))
    return issued_books, fine
