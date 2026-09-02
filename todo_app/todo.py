"""Todo list module — stubs to be implemented."""


class Todo:
    def __init__(self, title):
        self.title = title
        self.done = False


class TodoList:
    def __init__(self):
        self.todos = []
    
    def add(self, title):
        todo = Todo(title)
        self.todos.append(todo)

    def complete(self, index):
        if index < 0 or index >= len(self.todos):
            raise ValueError
        self.todos[index].done = True

    def list_all(self):
        return self.todos
