from enum import Enum

class UserRole(Enum):
    MEMBER = "Member"
    LIBRARIAN = "Librarian"
    ADMIN = "Admin"

class BookStatus(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"

class LibStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"

class BorrowStatus(Enum):
    BORROWED = "Borrowed"
    RETURNED = "Returned"
    OVERDUE = "Overdue"