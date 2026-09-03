import { test, expect } from '@playwright/test';

test('submitting empty title shows error and adds nothing to list', async ({ page }) => {
  await page.goto('/');
  
  const titleInput = page.locator('#todo-title');
  const todoForm = page.locator('#todo-form');
  const todoList = page.locator('#todo-list');
  const errorElement = page.locator('#error');
  
  // Submit empty title
  await titleInput.fill('');
  await todoForm.locator('button[type="submit"]').click();
  
  // Verify error message appears
  await expect(errorElement).toHaveText('Title cannot be empty');
  
  // Verify no li is added
  await expect(todoList.locator('li')).toHaveCount(0);
});

test('submitting whitespace-only title shows error and adds nothing to list', async ({ page }) => {
  await page.goto('/');
  
  const titleInput = page.locator('#todo-title');
  const todoForm = page.locator('#todo-form');
  const todoList = page.locator('#todo-list');
  const errorElement = page.locator('#error');
  
  // Submit whitespace-only title
  await titleInput.fill('   ');
  await todoForm.locator('button[type="submit"]').click();
  
  // Verify error message appears
  await expect(errorElement).toHaveText('Title cannot be empty');
  
  // Verify no li is added
  await expect(todoList.locator('li')).toHaveCount(0);
});

test('error message disappears after successful add', async ({ page }) => {
  await page.goto('/');
  
  const titleInput = page.locator('#todo-title');
  const todoForm = page.locator('#todo-form');
  const todoList = page.locator('#todo-list');
  const errorElement = page.locator('#error');
  
  // First submit empty to trigger error
  await titleInput.fill('');
  await todoForm.locator('button[type="submit"]').click();
  await expect(errorElement).toHaveText('Title cannot be empty');
  
  // Then submit valid title
  await titleInput.fill('Valid task');
  await todoForm.locator('button[type="submit"]').click();
  
  // Verify error is cleared
  await expect(errorElement).toHaveText('');
  
  // Verify item was added
  await expect(todoList.locator('li')).toHaveCount(1);
});