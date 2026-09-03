/**
 * Todo app browser behavior.
 *
 * Wires form submission and list interactions for adding and toggling todos.
 */

const EMPTY_TITLE_ERROR = 'Title cannot be empty';

/**
 * Return an element by selector and assert it exists.
 *
 * @template {Element} T
 * @param {ParentNode} root - Node used for querying.
 * @param {string} selector - CSS selector for the required element.
 * @returns {T} The matching element.
 * @throws {Error} When no matching element exists.
 */
function requireElement(root, selector) {
  const element = root.querySelector(selector);
  if (!element) {
    throw new Error(`Missing required element: ${selector}`);
  }
  return /** @type {T} */ (element);
}

/**
 * Initialize todo form behavior for a document.
 *
 * @param {Document} doc - The document containing the todo app markup.
 * @returns {void}
 */
export function initTodoApp(doc) {
  const form = requireElement(/** @type {ParentNode} */ (doc), '#todo-form');
  const titleInput = requireElement(/** @type {ParentNode} */ (doc), '#todo-title');
  const errorLine = requireElement(/** @type {ParentNode} */ (doc), '#error');
  const todoList = requireElement(/** @type {ParentNode} */ (doc), '#todo-list');

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const trimmedTitle = titleInput.value.trim();
    if (!trimmedTitle) {
      errorLine.textContent = EMPTY_TITLE_ERROR;
      return;
    }

    const listItem = doc.createElement('li');
    listItem.textContent = trimmedTitle;
    todoList.appendChild(listItem);

    titleInput.value = '';
    errorLine.textContent = '';
  });

  todoList.addEventListener('click', (event) => {
    const target = /** @type {Element|null} */ (event.target);
    if (!target) {
      return;
    }

    const listItem = target.closest('li');
    if (!listItem || !todoList.contains(listItem)) {
      return;
    }

    listItem.classList.toggle('done');
  });
}

initTodoApp(document);

