from pydantic import BaseModel
from core_enums import BookStatus, LibStatus, BorrowStatus

from typing import Union
from datetime import datetime

class Book(BaseModel):
    id: int
    title: str
    author: str
    available_copies: int
    total_copies: int
    borrowed: int = 0

class BookCopy(BaseModel):
    id: int
    book_id: int
    book_copy_status: BookStatus
    library_id: int

class Library(BaseModel):
    id: int
    name: str
    status: LibStatus

class LibWallet(BaseModel):
    id: int
    balance: float = 0.0

class User:
    id: int
    name: str
    dues: float = 0.0

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def request_book(self, book_id: int):
        pass

    def request_book_return(self, book_id: int):
        pass

    def pay_fines(self, amount: float):
        pass


class Staff(BaseModel):
    id: int
    name: str
    role: str

class BorrowRecord(BaseModel):
    id: int
    user_id: int
    book_copy_id: int
    borrow_date: str
    due_date: str
    return_date: Union[str, None] = None
    status: BorrowStatus = BorrowStatus.BORROWED

class LibManagementSystem:
    def __init__(self):
        self.books = []
        self.book_copies = []
        self.libraries = []
        self.users = []
        self.staff_members = []
        self.lib_wallets = []
        self.borrow_records = []

    def add_library(self, library: Library):
        self.libraries.append(library)

    def add_book(self, book: Book, library_id: int):
        self.books.append(book)
        self._add_book_copy(BookCopy(id=len(self.book_copies)+1, 
                                     book_id=book.id, 
                                     book_copy_status=BookStatus.AVAILABLE, 
                                     library_id=library_id))


    def _add_book_copy(self, book_copy: BookCopy):
        self.book_copies.append(book_copy)

    def register_user(self, user: User):
        self.users.append(user)

    def register_staff(self, staff: Staff):
        self.staff_members.append(staff)

    def get_book_availability(self, book_id: int) -> bool:
        if not (book := next((b for b in self.books if b.id == book_id), None)):
            raise ValueError("Book not found")
        elif book.available_copies > 0:
            return True
        else:
            return False

    def borrow_book(self, user_id: int, book_id: int):
        is_available = self.get_book_availability(book_id)
        if not is_available:
            raise ValueError("Book not available")

        book_copy = next((bc for bc in self.book_copies if bc.book_id == book_id and bc.book_copy_status == BookStatus.AVAILABLE), None)
        if not book_copy:
            raise ValueError("No available copies")

        book_copy.book_copy_status = BookStatus.BORROWED
        self.books[book_id].available_copies -= 1
        borrow_record = BorrowRecord(id=len(self.borrow_records)+1, user_id=user_id, 
                                     book_copy_id=book_copy.id, borrow_date=str(datetime.now()),
                                     due_date = str(datetime.now())
                                     )
        # Save borrow_record to database or in-memory list
        self.borrow_records.append(borrow_record)


    def check_pending_dues(self, user_id: int) -> float:
        return 1.0
    
    def return_book(self, user_id: int, book_id: int):
        book_copy = next((bc for bc in self.book_copies if bc.book_id == book_id and bc.book_copy_status == BookStatus.BORROWED), None)
        if not book_copy:
            raise ValueError("No borrowed copies found")
        
        # todo: design function to cjeck dues from borrow record
        if self.check_pending_dues(user_id) > 0:
            raise ValueError("User has pending dues")
            # todo: handle this by checking borrow record and asking user to pay

        book_copy.book_copy_status = BookStatus.AVAILABLE
        self.books[book_id].available_copies += 1

        # find borrowrecord and update it



