import React from 'react';
import { FiAlertCircle, FiCheckCircle, FiCode } from 'react-icons/fi';
import styles from './RecommendationsPanel.module.css';

export function RecommendationsPanel({ report }) {
  if (!report) return null;

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'CRITICAL':
        return '#dc3545';
      case 'HIGH':
        return '#ff9800';
      case 'MEDIUM':
        return '#ffc107';
      case 'LOW':
        return '#17a2b8';
      default:
        return '#6c757d';
    }
  };

  const renderRecommendationSection = (title, recommendations) => {
    if (!recommendations || recommendations.length === 0) return null;

    return (
      <div className={styles.section} key={title}>
        <h4 className={styles.sectionTitle}>
          {title} ({recommendations.length})
        </h4>
        <div className={styles.recommendations}>
          {recommendations.map((rec, idx) => (
            <div
              key={idx}
              className={styles.recommendation}
              style={{
                borderLeftColor: getPriorityColor(rec.priority),
              }}
            >
              <div className={styles.header}>
                <h5>{rec.title}</h5>
                <span
                  className={styles.priority}
                  style={{ backgroundColor: getPriorityColor(rec.priority) }}
                >
                  {rec.priority}
                </span>
              </div>
              <p className={styles.description}>{rec.description}</p>
              <div className={styles.details}>
                <span className={styles.category}>{rec.category}</span>
                <span className={styles.effort}>{rec.estimated_effort} effort</span>
                <span className={styles.impact}>{rec.impact} impact</span>
              </div>
              <div className={styles.action}>
                <strong>Action:</strong> {rec.action}
              </div>
              {rec.example_code && (
                <details className={styles.codeExample}>
                  <summary>
                    <FiCode /> View example code
                  </summary>
                  <pre>{rec.example_code}</pre>
                </details>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className={styles.container}>
      <div className={styles.scoreBoard}>
        <div className={styles.mainScore}>
          <div className={styles.grade}>{report.grade}</div>
          <div className={styles.scoreInfo}>
            <span className={styles.score}>{report.overall_score.toFixed(1)}</span>
            <span className={styles.label}>Overall Score</span>
          </div>
        </div>

        <div className={styles.issuesGrid}>
          <div className={styles.issueCard} style={{ borderColor: '#dc3545' }}>
            <span className={styles.count}>{report.critical_issues}</span>
            <span className={styles.label}>Critical</span>
          </div>
          <div className={styles.issueCard} style={{ borderColor: '#ff9800' }}>
            <span className={styles.count}>{report.high_issues}</span>
            <span className={styles.label}>High</span>
          </div>
          <div className={styles.issueCard} style={{ borderColor: '#ffc107' }}>
            <span className={styles.count}>{report.medium_issues}</span>
            <span className={styles.label}>Medium</span>
          </div>
          <div className={styles.issueCard} style={{ borderColor: '#17a2b8' }}>
            <span className={styles.count}>{report.low_issues}</span>
            <span className={styles.label}>Low</span>
          </div>
        </div>
      </div>

      <div className={styles.categoryBreakdown}>
        <h4>Category Breakdown</h4>
        <div className={styles.categories}>
          {Object.entries(report.category_breakdown || {}).map(([cat, data]) => (
            <div key={cat} className={styles.categoryItem}>
              <div className={styles.categoryName}>{cat}</div>
              <div className={styles.categoryStats}>
                <span className={styles.passed}>✓ {data.passed}</span>
                <span className={styles.failed}>✗ {data.failed}</span>
              </div>
              <div className={styles.progressBar}>
                <div
                  className={styles.progress}
                  style={{
                    width: `${data.pass_rate}%`,
                    backgroundColor:
                      data.pass_rate >= 80 ? '#28a745' : '#ff9800',
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className={styles.recommendationsContainer}>
        <h3>Recommendations</h3>

        {renderRecommendationSection(
          'Critical Issues',
          report.recommendations?.critical
        )}
        {renderRecommendationSection('High Priority', report.recommendations?.high)}
        {renderRecommendationSection(
          'Medium Priority',
          report.recommendations?.medium
        )}
        {renderRecommendationSection('Low Priority', report.recommendations?.low)}

        {report.total_issues === 0 && (
          <div className={styles.noIssues}>
            <FiCheckCircle size={48} />
            <h4>Perfect Score!</h4>
            <p>Your UI meets all best practices recommendations.</p>
          </div>
        )}
      </div>
    </div>
  );
}
