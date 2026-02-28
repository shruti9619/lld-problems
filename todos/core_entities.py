from dataclasses import dataclass
from enum import Enum

@dataclass
class User:
    id: int
    name: str

class TodoStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    DELETED = "deleted"    
    

@dataclass
class Todo:
    id: int
    user_id: int
    title: str
    description: str
    status: TodoStatus = TodoStatus.PENDING


class TodoSystem:
    def __init__(self):
        self.users = {}
        self.todos = {}
        self.next_user_id = 1
        self.next_todo_id = 1

    def add_user(self, name: str) -> User:
        print(f"Adding user: {name}")
        user = User(id=self.next_user_id, name=name)
        self.users[self.next_user_id] = user
        self.next_user_id += 1
        return user

    def add_todo(self, user_id: int, title: str, description: str) -> Todo:
        print(f"Adding todo for user_id: {user_id}, title: {title}")
        if user_id not in self.users:
            raise ValueError("User not found")
        todo = Todo(id=self.next_todo_id, user_id=user_id, title=title, description=description)
        self.todos[self.next_todo_id] = todo
        self.next_todo_id += 1
        return todo

    def update_todo_status(self, todo_id: int, status: TodoStatus):
        print(f"Updating todo_id: {todo_id} to status: {status}")
        if todo_id not in self.todos:
            raise ValueError("Todo not found")
        self.todos[todo_id].status = status

    def get_user_todos(self, user_id: int):
        print(f"Getting todos for user_id: {user_id}")
        if user_id not in self.users:
            raise ValueError("User not found")
        return [todo for todo in self.todos.values() if todo.user_id == user_id]
    