import { test, expect } from '@playwright/test';

test('clicking list item toggles done class', async ({ page }) => {
  await page.goto('/');
  
  const titleInput = page.locator('#todo-title');
  const todoForm = page.locator('#todo-form');
  const todoList = page.locator('#todo-list');
  
  // Add a todo item first
  await titleInput.fill('Test task');
  await todoForm.locator('button[type="submit"]').click();
  
  const todoItem = todoList.locator('li').first();
  
  // Initially should not have done class
  await expect(todoItem).not.toHaveClass(/done/);
  
  // Click once to mark as done
  await todoItem.click();
  await expect(todoItem).toHaveClass(/done/);
  
  // Click again to unmark
  await todoItem.click();
  await expect(todoItem).not.toHaveClass(/done/);
});