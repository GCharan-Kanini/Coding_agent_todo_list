import React from 'react';

/**
 * Landing - static, accessible, responsive landing page for the Todo app
 *
 * Semantic structure: header (brand + title), section.hero (copy + media),
 * features list and a primary call-to-action button. Designed mobile-first
 * with CSS rules in src/styles.css to switch to a side-by-side layout on
 * larger viewports.
 *
 * This component is presentational only and intentionally free of runtime
 * behaviour to serve as a static landing/hero for the application.
 */
export default function Landing() {
  return (
    <header>
      <div className="brand-row" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div>
          <div className="brand" aria-hidden="true">Todo</div>
          <h1 className="hero-title">Todo — Organize your day, one task at a time</h1>
          <p className="tagline">A minimal, focused todo app to capture tasks, plan your day, and get things done.</p>
        </div>
      </div>

      <section className="hero" aria-labelledby="todo-hero-title">
        <div className="hero-grid">
          <div className="hero-copy">
            <div id="todo-hero-title" style={{position: 'absolute', left: -9999, top: 'auto', width: 1, height: 1, overflow: 'hidden'}}>Todo app hero</div>
            <div className="cta-row">
              <button className="btn-primary" aria-label="Get started with Todo" autoFocus>Get Started</button>
            </div>

            <div className="features" aria-hidden="false">
              <ul>
                <li>Quickly add and organize tasks</li>
                <li>Keep track of progress with a simple UI</li>
                <li>Works on mobile and desktop with responsive layout</li>
              </ul>
            </div>
          </div>

          <div className="hero-media">
            {/* Illustrative image uses the favicon as a safe bundled asset and includes alt text. */}
            <img className="illustration" src="/favicon.ico" alt="Illustration: checklist and calendar representing tasks and planning" />
          </div>
        </div>
      </section>
    </header>
  );
}
