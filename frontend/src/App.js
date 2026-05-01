import React, { useState, useEffect } from 'react';
import { FiMenu, FiX } from 'react-icons/fi';
import { analysisService } from './services/analysisService';
import { ImageUploader } from './components/ImageUploader';
import { CodeEditor } from './components/CodeEditor';
import { RecommendationsPanel } from './components/RecommendationsPanel';
import styles from './App.module.css';

function App() {
  const [activeTab, setActiveTab] = useState('screenshot');
  const [isLoading, setIsLoading] = useState(false);
  const [currentReport, setCurrentReport] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await analysisService.getHistory(5);
      if (response.data.status === 'success') {
        setHistory(response.data.history || []);
      }
    } catch (err) {
      console.log('Failed to load history');
    }
  };

  const handleScreenshotAnalysis = async (imageFile) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await analysisService.analyzeScreenshot(imageFile);
      if (response.data.status === 'success') {
        setCurrentReport(response.data.report);
        loadHistory();
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze screenshot');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCodeAnalysis = async (htmlCode, cssCode) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await analysisService.analyzeCode(htmlCode, cssCode);
      if (response.data.status === 'success') {
        setCurrentReport(response.data.report);
        loadHistory();
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze code');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleHistoryClick = (index) => {
    const item = history[index];
    if (item && item.report) {
      setCurrentReport(item.report);
      setSidebarOpen(false);
    }
  };

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <h1>🤖 AI UI Recommendation Agent</h1>
          <button
            className={styles.menuButton}
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <FiX /> : <FiMenu />}
          </button>
        </div>
      </header>

      <div className={styles.container}>
        {/* Sidebar */}
        <aside className={`${styles.sidebar} ${sidebarOpen ? styles.open : ''}`}>
          <div className={styles.sidebarContent}>
            <h3>Recent Analyses</h3>
            {history.length > 0 ? (
              <div className={styles.historyList}>
                {history.map((item, idx) => (
                  <button
                    key={idx}
                    className={styles.historyItem}
                    onClick={() => handleHistoryClick(idx)}
                  >
                    <span className={styles.type}>
                      {item.analysis_type === 'screenshot' ? '📸' : '📝'}
                    </span>
                    <div className={styles.historyInfo}>
                      <div className={styles.score}>
                        Score: {item.report?.overall_score.toFixed(1)}
                      </div>
                      <div className={styles.time}>
                        {new Date(item.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            ) : (
              <p className={styles.noHistory}>No analyses yet</p>
            )}
          </div>
        </aside>

        {/* Main Content */}
        <main className={styles.main}>
          {error && (
            <div className={styles.errorBanner}>
              <p>{error}</p>
              <button onClick={() => setError(null)} className={styles.closeError}>
                ✕
              </button>
            </div>
          )}

          <div className={styles.tabsContainer}>
            <div className={styles.tabs}>
              <button
                className={`${styles.tab} ${activeTab === 'screenshot' ? styles.active : ''}`}
                onClick={() => setActiveTab('screenshot')}
              >
                📸 Screenshot Analysis
              </button>
              <button
                className={`${styles.tab} ${activeTab === 'code' ? styles.active : ''}`}
                onClick={() => setActiveTab('code')}
              >
                📝 Code Analysis
              </button>
            </div>
          </div>

          <div className={styles.content}>
            {activeTab === 'screenshot' && (
              <ImageUploader
                onAnalyze={handleScreenshotAnalysis}
                isLoading={isLoading}
              />
            )}

            {activeTab === 'code' && (
              <CodeEditor
                onAnalyze={handleCodeAnalysis}
                isLoading={isLoading}
              />
            )}
          </div>

          {currentReport && (
            <div className={styles.resultsContainer}>
              <RecommendationsPanel report={currentReport} />
            </div>
          )}

          {!currentReport && !error && (
            <div className={styles.emptyState}>
              <h2>Welcome to AI UI Recommendation Agent</h2>
              <p>
                Get AI-powered insights and recommendations to improve your UI/UX
              </p>
              <ul className={styles.features}>
                <li>✅ Screenshot Analysis - Upload a UI screenshot for instant feedback</li>
                <li>✅ Code Analysis - Paste your HTML/CSS for code quality insights</li>
                <li>✅ Best Practices - Get recommendations based on UX principles</li>
                <li>✅ Accessibility Check - Ensure your UI is accessible</li>
                <li>✅ Performance Tips - Optimize for better user experience</li>
              </ul>
            </div>
          )}
        </main>
      </div>

      <footer className={styles.footer}>
        <p>© 2024 AI UI Recommendation Agent - Making better UX for everyone</p>
      </footer>
    </div>
  );
}

export default App;
