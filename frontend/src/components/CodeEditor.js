import React, { useState } from 'react';
import { FiX } from 'react-icons/fi';
import styles from './CodeEditor.module.css';

export function CodeEditor({ onAnalyze, isLoading }) {
  const [htmlCode, setHtmlCode] = useState('');
  const [cssCode, setCssCode] = useState('');
  const [activeTab, setActiveTab] = useState('html');
  const [error, setError] = useState(null);

  const handleAnalyze = () => {
    if (!htmlCode.trim()) {
      setError('Please enter HTML code');
      return;
    }
    setError(null);
    onAnalyze(htmlCode, cssCode);
  };

  const clearCode = () => {
    setHtmlCode('');
    setCssCode('');
    setError(null);
  };

  const loadExample = () => {
    setHtmlCode(`<!DOCTYPE html>
<html lang="en">
<head>
    <title>Example Page</title>
</head>
<body>
    <header>
        <nav>Navigation</nav>
    </header>
    <main>
        <section>
            <h1>Welcome</h1>
            <p>Your content here</p>
            <button>Click Me</button>
        </section>
    </main>
</body>
</html>`);
    setCssCode(`body {
  font-family: Arial, sans-serif;
  color: #333;
}

h1 {
  color: #007bff;
  font-size: 2em;
}

button {
  background: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}`);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>Code Analysis</h3>
        <button className={styles.exampleBtn} onClick={loadExample}>
          Load Example
        </button>
      </div>

      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === 'html' ? styles.active : ''}`}
          onClick={() => setActiveTab('html')}
        >
          HTML
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'css' ? styles.active : ''}`}
          onClick={() => setActiveTab('css')}
        >
          CSS
        </button>
      </div>

      <div className={styles.editor}>
        {activeTab === 'html' ? (
          <textarea
            value={htmlCode}
            onChange={(e) => setHtmlCode(e.target.value)}
            placeholder="Enter your HTML code here..."
            className={styles.textarea}
            disabled={isLoading}
          />
        ) : (
          <textarea
            value={cssCode}
            onChange={(e) => setCssCode(e.target.value)}
            placeholder="Enter your CSS code here (optional)..."
            className={styles.textarea}
            disabled={isLoading}
          />
        )}
      </div>

      {error && (
        <div className={styles.error}>
          {error}
          <button onClick={() => setError(null)} className={styles.closeError}>
            <FiX />
          </button>
        </div>
      )}

      <div className={styles.actions}>
        <button
          className={styles.analyzeBtn}
          onClick={handleAnalyze}
          disabled={isLoading || !htmlCode.trim()}
        >
          {isLoading ? 'Analyzing...' : 'Analyze Code'}
        </button>
        <button
          className={styles.clearBtn}
          onClick={clearCode}
          disabled={isLoading}
        >
          Clear
        </button>
      </div>
    </div>
  );
}
