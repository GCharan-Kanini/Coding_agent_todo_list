import { test, expect } from '@playwright/test';

test('items maintain insertion order in rendered list', async ({ page }) => {
  await page.goto('/');
  
  const titleInput = page.locator('#todo-title');
  const todoForm = page.locator('#todo-form');
  const todoList = page.locator('#todo-list');
  
  // Add three items in specific order
  const titles = ['First task', 'Second task', 'Third task'];
  
  for (const title of titles) {
    await titleInput.fill(title);
    await todoForm.locator('button[type="submit"]').click();
  }
  
  // Verify all three items are present
  await expect(todoList.locator('li')).toHaveCount(3);
  
  // Verify they appear in insertion order (top to bottom)
  const listItems = todoList.locator('li');
  await expect(listItems.nth(0)).toHaveText('First task');
  await expect(listItems.nth(1)).toHaveText('Second task');
  await expect(listItems.nth(2)).toHaveText('Third task');
});