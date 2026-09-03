/**
 * Todo list domain module.
 *
 * Exports `Todo` and `TodoList` classes for creating and managing todo items.
 */

/**
 * Represents a single todo item.
 */
export class Todo {
  /** @type {string} */
  #title;

  /** @type {boolean} */
  #done;

  /**
   * Creates a todo item.
   *
   * @param {string} title - The todo title.
   * @throws {TypeError} When `title` is not a string.
   * @throws {RangeError} When `title` is an empty string after trimming.
   */
  constructor(title) {
    if (typeof title !== 'string') {
      throw new TypeError(`Invalid title value: ${String(title)}. Expected a string.`);
    }

    const normalizedTitle = title.trim();
    if (normalizedTitle.length === 0) {
      throw new RangeError(`Invalid title value: ${JSON.stringify(title)}. Title cannot be empty.`);
    }

    this.#title = normalizedTitle;
    this.#done = false;
  }

  /**
   * Gets the todo title.
   *
   * @returns {string} The stored title.
   */
  get title() {
    return this.#title;
  }

  /**
   * Gets whether the todo is completed.
   *
   * @returns {boolean} True when completed; otherwise false.
   */
  get done() {
    return this.#done;
  }

  /**
   * Marks this todo as completed.
   *
   * @returns {void}
   */
  markDone() {
    this.#done = true;
  }
}

/**
 * Manages an ordered collection of todo items.
 */
export class TodoList {
  /** @type {Todo[]} */
  #todos = [];

  /**
   * Adds a new todo item to the end of the list.
   *
   * @param {string} title - The title for the todo item.
   * @returns {Todo} The created todo item.
   * @throws {TypeError} When `title` is not a string.
   * @throws {RangeError} When `title` is empty.
   */
  add(title) {
    const todo = new Todo(title);
    this.#todos.push(todo);
    return todo;
  }

  /**
   * Marks the todo at `index` as completed.
   *
   * @param {number} index - Zero-based list index.
   * @returns {void}
   * @throws {TypeError} When `index` is not an integer.
   * @throws {RangeError} When `index` is outside the list bounds.
   */
  complete(index) {
    if (!Number.isInteger(index)) {
      throw new TypeError(`Invalid index value: ${String(index)}. Expected an integer.`);
    }

    if (index < 0 || index >= this.#todos.length) {
      throw new RangeError(
        `Index out of range: ${index}. Valid range is 0..${this.#todos.length - 1}.`
      );
    }

    this.#todos[index].markDone();
  }

  /**
   * Returns todos in insertion order.
   *
   * @returns {Todo[]} A shallow copy of todos in insertion order.
   */
  listAll() {
    return [...this.#todos];
  }
}
