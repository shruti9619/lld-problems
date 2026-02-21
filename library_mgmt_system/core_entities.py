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
    borrowed_copy_id: list[int] = []

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
    due_amt: int = 0


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
        self._add_book_copy(
            BookCopy(
                id=len(self.book_copies) + 1,
                book_id=book.id,
                book_copy_status=BookStatus.AVAILABLE,
                library_id=library_id,
            )
        )

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

    def borrow_book(self, user: User, book_id: int):
        print(f"User {user.name} is requesting to borrow book with id: {book_id}")
        is_available = self.get_book_availability(book_id)
        if not is_available:
            raise ValueError("Book not available")

        book_copy = next(
            (
                bc
                for bc in self.book_copies
                if bc.book_id == book_id and bc.book_copy_status == BookStatus.AVAILABLE
            ),
            None,
        )
        if not book_copy:
            raise ValueError("No available copies")

        book_copy.book_copy_status = BookStatus.BORROWED
        borrow_record = BorrowRecord(
            id=len(self.borrow_records) + 1,
            user_id=user.id,
            book_copy_id=book_copy.id,
            borrow_date=str(datetime.now()),
            due_date=str(datetime.now()),
        )

        # update available copies count
        book = next((b for b in self.books if b.id == book_copy.book_id), None)
        if book:
            book.available_copies -= 1

        # Save borrow_record to database or in-memory list
        self.borrow_records.append(borrow_record)
        user.borrowed_copy_id.append(book_copy.id)

    def _calc_penalty(self, borrow_record: BorrowRecord):
        if penalty_days := (datetime.now() - borrow_record.due_date).days > 0:
            borrow_record.due_amt = penalty_days * 10
            return borrow_record.due_amt
        else:
            return 0.0

    def _find_borrow_record(
        self, user_id: int, book_copy_id: int
    ) -> Union[BorrowRecord, None]:
        return next(
            (
                br
                for br in self.borrow_records
                if br.user_id == user_id and br.book_copy_id == book_copy_id
            ),
            None,
        )

    def check_pending_dues(self, borrow_record: BorrowRecord) -> float:
        # lookup borrow_records
        if borrow_record:
            return self._calc_penalty(borrow_record)
        else:
            raise Exception("User Borrow Record Not Found")

    def request_due_clearance(self, user, borrow_record: BorrowRecord, dues: float):
        print(f"User clearing due of amount: {dues}")
        borrow_record.due_amt = 0

    def return_book(self, user: User, book_copy: BookCopy):
        borrow_record: Union[BorrowRecord, None] = self._find_borrow_record(
            user_id=user.id, book_copy_id=book_copy.id
        )
        if borrow_record is None:
            raise Exception("Borrow record not found!")

        if (dues := self.check_pending_dues(borrow_record)) > 0:
            self.request_due_clearance(user, borrow_record, dues)

        book_copy.book_copy_status = BookStatus.AVAILABLE
        self.books[book_copy.book_id].available_copies += 1

        borrow_record.status = BorrowStatus.RETURNED
