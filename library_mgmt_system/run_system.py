from core_entities import User, Staff, LibManagementSystem, Book, Library


def create_lib():
    lib = LibManagementSystem()
    lib.add_library(Library(id=1, name="Central Library", status="Open"))
    print("Library created successfully!")
    total_copies = available_copies = 2
    lib.add_book(
        Book(
            id=1,
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            isbn="978-0743273565",
            total_copies=total_copies,
            available_copies=available_copies,
        ),
        library_id=1,
    )
    lib.add_book(
        Book(
            id=2,
            title="To Kill a Mockingbird",
            author="Harper Lee",
            isbn="978-0061120084",
            total_copies=total_copies,
            available_copies=available_copies,
        ),
        library_id=1,
    )
    print("Books added successfully!")
    return lib


if __name__ == "__main__":
    library_system = create_lib()
    print("Welcome to the Library Management System!")

    print("Registering users and staff...")
    user1 = User(id=1, name="Alice")
    user2 = User(id=2, name="Bob")
    staff1 = Staff(id=1, name="Eve", role="Librarian")

    library_system.register_user(user1)
    library_system.register_user(user2)
    library_system.register_staff(staff1)


    print("borrowing and returning books...")
    library_system.borrow_book(user= user1, book_id=1)
    library_system.borrow_book(user=user2, book_id=2)

    library_system.return_book(user=user1, book_copy_id=1)
    library_system.return_book(user=user2, book_copy_id=2)

    print("Thank you for using the Library Management System!")