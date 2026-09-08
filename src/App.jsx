import React from 'react';
import Landing from './components/Landing.jsx';

/**
 * App - top level application shell
 * Renders the Landing component inside a semantic main element.
 */
export default function App() {
  return (
    <div className="app-shell">
      <main className="container">
        <Landing />
      </main>
    </div>
  );
}
