import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, within, fireEvent } from '@testing-library/react';
import fs from 'fs';
import path from 'path';

// Import targets under test (relative to this test file)
import Landing from '../components/Landing.jsx';
import App from '../App.jsx';

// NOTE: Tests are intentionally explicit and will fail if the repository
// does not yet implement the requested targets. This is by design per the
// task's greenfield policy: failing tests are evidence of missing behaviour.

describe('Landing component - core UI and accessibility', () => {
  it('mounts Landing without throwing and renders title, tagline, primary CTA, and a three-item feature list', () => {
    // Render the Landing component in isolation to scope queries
    const { container } = render(React.createElement(Landing));

    // Semantic header element should be present
    const headerEl = container.querySelector('header');
    expect(headerEl).toBeTruthy();

    // There should be a heading. Prefer a heading that includes 'todo' (case-insensitive).
    // This asserts the app name/title is present and recognizable.
    const heading = screen.getByRole('heading');
    expect(heading).toBeTruthy();
    const headingText = (heading.textContent || '').trim();
    // Assert the heading contains 'todo' (case-insensitive) to satisfy AC-1.
    expect(/todo/i.test(headingText)).toBe(true);

    // There should be at least one paragraph (tagline)
    const p = container.querySelector('p');
    expect(p).toBeTruthy();
    expect((p.textContent || '').trim().length).toBeGreaterThan(0);

    // There should be at least one button (CTA). Ensure the primary CTA is focusable.
    const buttons = screen.getAllByRole('button');
    expect(buttons.length).toBeGreaterThan(0);
    // Prefer a button whose label suggests a primary action; otherwise take the first.
    const primary = buttons.find(b => /get started|start|try|create|add|signup|sign up|cta|primary/i.test((b.textContent || ''))) || buttons[0];
    expect(primary).toBeTruthy();
    expect((primary.textContent || '').trim().length).toBeGreaterThan(0);

    // Focus the primary CTA and ensure it receives focus (basic keyboard accessibility)
    fireEvent.focus(primary);
    expect(document.activeElement).toBe(primary);

    // Feature list: find a <ul> or <ol> within the landing that has exactly three items.
    const lists = screen.queryAllByRole('list');
    // Find a list that contains exactly three listitems
    const featureList = lists.find(l => within(l).queryAllByRole('listitem').length === 3);
    expect(featureList).toBeTruthy();
    const items = within(featureList).getAllByRole('listitem');
    expect(items.length).toBe(3);

    // If an illustrative image exists in the landing, it must have meaningful alt text
    const img = container.querySelector('img');
    if (img) {
      const alt = img.getAttribute('alt') || '';
      expect(alt.trim().length).toBeGreaterThan(0);
    }
  });

  it('renders the top-level App without throwing', () => {
    // Smoke test: mounting App should not throw
    const renderApp = () => render(React.createElement(App));
    expect(renderApp).not.toThrow();
  });
});

describe('Build / assets / styles checks', () => {
  it('imports styles.css from src/main.jsx', () => {
    const mainPath = path.resolve(process.cwd(), 'src', 'main.jsx');
    const exists = fs.existsSync(mainPath);
    expect(exists).toBe(true);
    const mainSrc = fs.readFileSync(mainPath, 'utf8');
    // Require an import reference to styles.css in the app entry
    expect(/styles\.css/.test(mainSrc)).toBe(true);
  });

  it('contains responsive CSS constructs in src/styles.css (e.g. @media)', () => {
    const cssPath = path.resolve(process.cwd(), 'src', 'styles.css');
    const exists = fs.existsSync(cssPath);
    expect(exists).toBe(true);
    const css = fs.readFileSync(cssPath, 'utf8');
    // Check for media queries to indicate responsive rules
    expect(/@media\b/.test(css)).toBe(true);
  });

  it('package.json defines dev, build, and preview scripts', () => {
    const pkgPath = path.resolve(process.cwd(), 'package.json');
    const exists = fs.existsSync(pkgPath);
    expect(exists).toBe(true);
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    expect(pkg).toBeTruthy();
    expect(pkg.scripts).toBeTruthy();
    expect(typeof pkg.scripts.dev === 'string' && pkg.scripts.dev.trim().length > 0).toBe(true);
    expect(typeof pkg.scripts.build === 'string' && pkg.scripts.build.trim().length > 0).toBe(true);
    expect(typeof pkg.scripts.preview === 'string' && pkg.scripts.preview.trim().length > 0).toBe(true);
  });
});
