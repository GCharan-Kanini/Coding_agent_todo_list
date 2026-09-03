import { describe, it, expect, beforeEach } from 'vitest';

function importTodo() {
  try {
    return require('../src/todo.js');
  } catch (error) {
    return null;
  }
}

function importTodoList() {
  try {
    return require('../src/todo.js');
  } catch (error) {
    return null;
  }
}

describe('Todo', () => {
  it('should store title and default done to false', () => {
    const todoModule = importTodo();
    expect(todoModule, 'todo module is not implemented yet').not.toBeNull();
    expect(todoModule.Todo, 'Todo class is not implemented yet').toBeDefined();
    
    const todo = new todoModule.Todo('Buy groceries');
    
    expect(todo.title).toBe('Buy groceries');
    expect(todo.done).toBe(false);
  });
});

describe('TodoList', () => {
  let todoListModule: any;
  let todoList: any;
  
  beforeEach(() => {
    todoListModule = importTodoList();
    if (todoListModule && todoListModule.TodoList) {
      todoList = new todoListModule.TodoList();
    }
  });
  
  it('should add todos and return them in insertion order', () => {
    expect(todoListModule, 'todo module is not implemented yet').not.toBeNull();
    expect(todoListModule.TodoList, 'TodoList class is not implemented yet').toBeDefined();
    expect(todoList.add, 'TodoList.add method is not implemented yet').toBeDefined();
    expect(todoList.listAll, 'TodoList.listAll method is not implemented yet').toBeDefined();
    
    todoList.add('First task');
    todoList.add('Second task');
    todoList.add('Third task');
    
    const todos = todoList.listAll();
    
    expect(todos).toHaveLength(3);
    expect(todos[0].title).toBe('First task');
    expect(todos[1].title).toBe('Second task');
    expect(todos[2].title).toBe('Third task');
    
    // Verify insertion order is preserved
    expect(todos[0].title).toBe('First task');
    expect(todos[1].title).toBe('Second task');
    expect(todos[2].title).toBe('Third task');
  });
  
  it('should mark todo as done when completed', () => {
    expect(todoListModule, 'todo module is not implemented yet').not.toBeNull();
    expect(todoListModule.TodoList, 'TodoList class is not implemented yet').toBeDefined();
    expect(todoList.add, 'TodoList.add method is not implemented yet').toBeDefined();
    expect(todoList.complete, 'TodoList.complete method is not implemented yet').toBeDefined();
    expect(todoList.listAll, 'TodoList.listAll method is not implemented yet').toBeDefined();
    
    todoList.add('Task to complete');
    todoList.add('Another task');
    
    // Verify initial state
    let todos = todoList.listAll();
    expect(todos[0].done).toBe(false);
    expect(todos[1].done).toBe(false);
    
    // Complete first todo
    todoList.complete(0);
    
    todos = todoList.listAll();
    expect(todos[0].done).toBe(true);
    expect(todos[1].done).toBe(false); // Other todos should remain unchanged
  });
  
  it('should throw RangeError for negative index', () => {
    expect(todoListModule, 'todo module is not implemented yet').not.toBeNull();
    expect(todoListModule.TodoList, 'TodoList class is not implemented yet').toBeDefined();
    expect(todoList.add, 'TodoList.add method is not implemented yet').toBeDefined();
    expect(todoList.complete, 'TodoList.complete method is not implemented yet').toBeDefined();
    expect(todoList.listAll, 'TodoList.listAll method is not implemented yet').toBeDefined();
    
    todoList.add('Test task');
    
    // Capture initial state
    const initialTodos = todoList.listAll();
    const initialDoneState = initialTodos[0].done;
    
    expect(() => {
      todoList.complete(-1);
    }).toThrow(RangeError);
    
    // Verify no partial state changes occurred
    const todosAfterError = todoList.listAll();
    expect(todosAfterError[0].done).toBe(initialDoneState);
    expect(todosAfterError).toHaveLength(initialTodos.length);
  });
  
  it('should throw RangeError for index equal to list length', () => {
    expect(todoListModule, 'todo module is not implemented yet').not.toBeNull();
    expect(todoListModule.TodoList, 'TodoList class is not implemented yet').toBeDefined();
    expect(todoList.add, 'TodoList.add method is not implemented yet').toBeDefined();
    expect(todoList.complete, 'TodoList.complete method is not implemented yet').toBeDefined();
    expect(todoList.listAll, 'TodoList.listAll method is not implemented yet').toBeDefined();
    
    todoList.add('First task');
    todoList.add('Second task');
    
    // Capture initial state
    const initialTodos = todoList.listAll();
    const initialDoneStates = initialTodos.map(todo => todo.done);
    
    expect(() => {
      todoList.complete(2); // Index equal to length
    }).toThrow(RangeError);
    
    // Verify no partial state changes occurred
    const todosAfterError = todoList.listAll();
    expect(todosAfterError).toHaveLength(initialTodos.length);
    todosAfterError.forEach((todo, index) => {
      expect(todo.done).toBe(initialDoneStates[index]);
    });
  });
  
  it('should throw RangeError for index greater than list length', () => {
    expect(todoListModule, 'todo module is not implemented yet').not.toBeNull();
    expect(todoListModule.TodoList, 'TodoList class is not implemented yet').toBeDefined();
    expect(todoList.add, 'TodoList.add method is not implemented yet').toBeDefined();
    expect(todoList.complete, 'TodoList.complete method is not implemented yet').toBeDefined();
    expect(todoList.listAll, 'TodoList.listAll method is not implemented yet').toBeDefined();
    
    todoList.add('Only task');
    
    // Capture initial state
    const initialTodos = todoList.listAll();
    const initialDoneState = initialTodos[0].done;
    
    expect(() => {
      todoList.complete(5); // Index much greater than length
    }).toThrow(RangeError);
    
    // Verify no partial state changes occurred
    const todosAfterError = todoList.listAll();
    expect(todosAfterError[0].done).toBe(initialDoneState);
    expect(todosAfterError).toHaveLength(initialTodos.length);
  });
  
  it('should throw RangeError on empty list', () => {
    expect(todoListModule, 'todo module is not implemented yet').not.toBeNull();
    expect(todoListModule.TodoList, 'TodoList class is not implemented yet').toBeDefined();
    expect(todoList.complete, 'TodoList.complete method is not implemented yet').toBeDefined();
    expect(todoList.listAll, 'TodoList.listAll method is not implemented yet').toBeDefined();
    
    // Verify list is empty
    expect(todoList.listAll()).toHaveLength(0);
    
    expect(() => {
      todoList.complete(0);
    }).toThrow(RangeError);
    
    // Verify list remains empty
    expect(todoList.listAll()).toHaveLength(0);
  });
});