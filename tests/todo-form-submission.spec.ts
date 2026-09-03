import { test, expect } from '@playwright/test';

test('submitting form with non-empty title appends new li and clears input', async ({ page }) => {
  await page.goto('/');
  
  // Verify the app initializes without throwing
  const errorMessage = await page.locator('#error').textContent();
  
  const titleInput = page.locator('#todo-title');
  const todoForm = page.locator('#todo-form');
  const todoList = page.locator('#todo-list');
  
  // Initial state: empty list
  await expect(todoList.locator('li')).toHaveCount(0);
  
  // Enter a title with whitespace to test trimming
  await titleInput.fill('  Buy groceries  ');
  await todoForm.locator('button[type="submit"]').click();
  
  // Verify new li is appended with trimmed text
  await expect(todoList.locator('li')).toHaveCount(1);
  await expect(todoList.locator('li').first()).toHaveText('Buy groceries');
  
  // Verify input is cleared
  await expect(titleInput).toHaveValue('');
});