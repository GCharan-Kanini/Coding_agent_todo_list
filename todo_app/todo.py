class Todo:
    def __init__(self, title):
        self.title = title
        self.done = False


class TodoList:
    def __init__(self):
        self._todos = []
    
    def add(self, title):
        todo = Todo(title)
        self._todos.append(todo)
    
    def list_all(self):
        return self._todos
    
    def complete(self, index):
        if index < 0 or index >= len(self._todos):
            raise ValueError("Index out of range")
        self._todos[index].done = True
