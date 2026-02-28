from core_entities import TodoSystem, TodoStatus


def main():
    todo_system = TodoSystem()
    print("Welcome to the ToDo System!")

    print("Alice is an active user.")
    user = todo_system.add_user("Alice")
    print(f"User added: {user}")

    todo1 = todo_system.add_todo(user_id=user.id, title="Buy groceries", description="Milk, Bread, Eggs")
    print(f"Todo added: {todo1}")

    todo2 = todo_system.add_todo(user_id=user.id, title="Read a book", description="Finish reading 'The Great Gatsby'")
    print(f"Todo added: {todo2}")

    todo_system.update_todo_status(todo_id=todo1.id, status=TodoStatus.COMPLETED)
    print(f"Updated Todo: {todo_system.todos[todo1.id]}")

    print('Dave is an inactive user.')

    user2 = todo_system.add_user("Dave")
    print(f"User added: {user2}")
    todo3 = todo_system.add_todo(user_id=user2.id, title="Go for a run", description="Run 5 miles in the park")
    print(f"Todo added: {todo3}")
    todo_system.update_todo_status(todo_id=todo3.id, status=TodoStatus.DELETED)
    
    print("Alice's Todos:")
    alice_todos = todo_system.get_user_todos(user_id=user.id)
    for todo in alice_todos:
        print(f"  - {todo}")
    
    print("Dave's Todos:")
    dave_todos = todo_system.get_user_todos(user_id=user2.id)
    for todo in dave_todos:
        print(f"  - {todo}")

if __name__ == "__main__":
    main()