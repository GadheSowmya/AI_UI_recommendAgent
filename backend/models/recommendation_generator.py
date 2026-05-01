"""
Recommendation Generator - Produces actionable recommendations
"""

from typing import Dict, List
from enum import Enum
from dataclasses import dataclass


class Priority(Enum):
    """Priority levels for recommendations"""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class Recommendation:
    """Represents a single recommendation"""
    title: str
    description: str
    category: str
    priority: Priority
    action: str
    impact: str  # high, medium, low
    estimated_effort: str  # low, medium, high
    example_code: str = ""


class RecommendationGenerator:
    """Generates actionable recommendations based on analysis"""
    
    def __init__(self):
        self.recommendation_templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load recommendation templates"""
        return {
            'alt_text_for_images': Recommendation(
                title='Add Alt Text to Images',
                description='Images are critical for accessibility. Users with screen readers need descriptive alt text.',
                category='accessibility',
                priority=Priority.HIGH,
                action='Add descriptive alt attributes to all <img> tags',
                impact='high',
                estimated_effort='low',
                example_code='<img src="photo.jpg" alt="User profile photo of John Doe" />'
            ),
            'keyboard_navigation': Recommendation(
                title='Improve Keyboard Navigation',
                description='Ensure all interactive elements can be accessed via keyboard for better accessibility.',
                category='accessibility',
                priority=Priority.HIGH,
                action='Add tabindex, implement focus management, and keyboard event handlers',
                impact='high',
                estimated_effort='medium',
                example_code='<button tabindex="0" onKeyDown={(e) => e.key === "Enter" && handleClick()}>Click me</button>'
            ),
            'color_contrast': Recommendation(
                title='Improve Color Contrast',
                description='Low contrast text is hard to read and inaccessible. Aim for 4.5:1 ratio for normal text.',
                category='accessibility',
                priority=Priority.HIGH,
                action='Increase contrast between foreground and background colors',
                impact='high',
                estimated_effort='low',
                example_code='.text { color: #333; background: #fff; /* Good contrast */ }'
            ),
            'form_labels': Recommendation(
                title='Add Form Labels',
                description='Every form input needs an associated <label> for accessibility and usability.',
                category='accessibility',
                priority=Priority.HIGH,
                action='Add <label> elements for all form inputs',
                impact='high',
                estimated_effort='low',
                example_code='<label htmlFor="email">Email:</label>\n<input id="email" type="email" />'
            ),
            'responsive_design': Recommendation(
                title='Implement Responsive Design',
                description='Ensure your site works well on all screen sizes with a mobile-first approach.',
                category='mobile-responsive',
                priority=Priority.HIGH,
                action='Add viewport meta tag, use CSS media queries, implement flexible layouts',
                impact='high',
                estimated_effort='high',
                example_code='<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n@media (max-width: 768px) { /* mobile styles */ }'
            ),
            'visual_hierarchy': Recommendation(
                title='Improve Visual Hierarchy',
                description='Guide user attention with consistent sizing, spacing, and styling.',
                category='design',
                priority=Priority.MEDIUM,
                action='Use consistent heading levels, scale, contrast, and spacing',
                impact='medium',
                estimated_effort='medium',
                example_code='h1 { font-size: 2em; }\nh2 { font-size: 1.5em; }\np { font-size: 1em; }'
            ),
            'whitespace_usage': Recommendation(
                title='Improve Whitespace',
                description='Adequate whitespace makes content more readable and less overwhelming.',
                category='design',
                priority=Priority.LOW,
                action='Increase padding, margins, and line-height in content areas',
                impact='medium',
                estimated_effort='low',
                example_code='.card { padding: 2rem; margin: 1.5rem 0; line-height: 1.6; }'
            ),
            'semantic_html': Recommendation(
                title='Use Semantic HTML',
                description='Semantic tags improve SEO, accessibility, and code maintainability.',
                category='seo',
                priority=Priority.MEDIUM,
                action='Replace divs with semantic tags: <header>, <nav>, <main>, <section>, <footer>',
                impact='high',
                estimated_effort='medium',
                example_code='<header>\n  <nav>Navigation</nav>\n</header>\n<main>\n  <section>Content</section>\n</main>'
            ),
            'clear_cta': Recommendation(
                title='Make CTAs More Prominent',
                description='Call-to-action buttons should stand out and be easy to find and click.',
                category='usability',
                priority=Priority.HIGH,
                action='Use contrasting colors, larger font size, and clear copy for CTA buttons',
                impact='high',
                estimated_effort='low',
                example_code='.cta-button { background: #007bff; color: white; padding: 12px 24px; font-size: 1.1em; }'
            ),
            'font_readability': Recommendation(
                title='Improve Font Readability',
                description='Choose readable fonts with appropriate sizing and spacing.',
                category='readability',
                priority=Priority.MEDIUM,
                action='Use system fonts or widely-supported web fonts; minimum 14px size for body text',
                impact='medium',
                estimated_effort='low',
                example_code='body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 1rem; line-height: 1.6; }'
            ),
            'meta_tags': Recommendation(
                title='Add Important Meta Tags',
                description='Meta tags improve SEO and browser rendering.',
                category='seo',
                priority=Priority.MEDIUM,
                action='Add title, description, viewport, and favicon tags',
                impact='medium',
                estimated_effort='low',
                example_code='<title>Page Title</title>\n<meta name="description" content="Page description">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            ),
            'button_size': Recommendation(
                title='Increase Button Size',
                description='Buttons should be at least 44x44px for mobile touch targets (WCAG standard).',
                category='usability',
                priority=Priority.MEDIUM,
                action='Set minimum padding/size for clickable elements',
                impact='medium',
                estimated_effort='low',
                example_code='button { min-width: 44px; min-height: 44px; padding: 10px 16px; }'
            ),
            'loading_states': Recommendation(
                title='Add Loading States',
                description='Provide visual feedback during async operations to improve UX.',
                category='usability',
                priority=Priority.MEDIUM,
                action='Show spinners, disabled states, or progress indicators during loading',
                impact='medium',
                estimated_effort='medium',
                example_code='{isLoading && <Spinner />}\n<button disabled={isLoading}>Submit</button>'
            ),
            'error_messages': Recommendation(
                title='Improve Error Messages',
                description='Clear, actionable error messages help users fix problems quickly.',
                category='usability',
                priority=Priority.MEDIUM,
                action='Provide specific, helpful error messages with clear solutions',
                impact='medium',
                estimated_effort='low',
                example_code='{error && <ErrorAlert message={error} suggestion="Please check your email format" />}'
            ),
        }
    
    def generate_recommendations(self, rule_results: Dict, quality_scores: Dict, 
                                category_summary: Dict) -> List[Recommendation]:
        """Generate recommendations based on rule results"""
        recommendations = []
        
        # Get failed rules
        failed_rules = [name for name, result in rule_results.items() if not result.get('passed', True)]
        
        # Generate recommendations for failed rules
        for failed_rule in failed_rules:
            if failed_rule in self.recommendation_templates:
                recommendations.append(self.recommendation_templates[failed_rule])
        
        # Sort by priority and impact
        recommendations.sort(key=lambda x: (x.priority.value, x.impact), reverse=True)
        
        return recommendations
    
    def generate_detailed_report(self, analysis_results: Dict) -> Dict:
        """Generate detailed improvement report"""
        
        rule_results = analysis_results.get('rule_results', {})
        quality_scores = analysis_results.get('quality_scores', {})
        category_summary = analysis_results.get('category_summary', {})
        
        recommendations = self.generate_recommendations(rule_results, quality_scores, category_summary)
        
        # Calculate overall score
        all_scores = [r['score'] for r in rule_results.values()]
        overall_score = sum(all_scores) / len(all_scores) if all_scores else 0
        
        # Prioritize recommendations
        critical_recs = [r for r in recommendations if r.priority == Priority.CRITICAL]
        high_recs = [r for r in recommendations if r.priority == Priority.HIGH]
        medium_recs = [r for r in recommendations if r.priority == Priority.MEDIUM]
        low_recs = [r for r in recommendations if r.priority == Priority.LOW]
        
        report = {
            'overall_score': round(overall_score, 2),
            'grade': self._calculate_grade(overall_score),
            'total_issues': len(recommendations),
            'critical_issues': len(critical_recs),
            'high_issues': len(high_recs),
            'medium_issues': len(medium_recs),
            'low_issues': len(low_recs),
            'category_breakdown': category_summary,
            'recommendations': {
                'critical': [self._rec_to_dict(r) for r in critical_recs],
                'high': [self._rec_to_dict(r) for r in high_recs],
                'medium': [self._rec_to_dict(r) for r in medium_recs],
                'low': [self._rec_to_dict(r) for r in low_recs],
            },
            'quality_scores': quality_scores,
        }
        
        return report
    
    def _rec_to_dict(self, rec: Recommendation) -> Dict:
        """Convert recommendation to dictionary"""
        return {
            'title': rec.title,
            'description': rec.description,
            'category': rec.category,
            'priority': rec.priority.name,
            'action': rec.action,
            'impact': rec.impact,
            'estimated_effort': rec.estimated_effort,
            'example_code': rec.example_code,
        }
    
    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from score"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def get_quick_wins(self, recommendations: List[Recommendation], limit: int = 5) -> List[Recommendation]:
        """Get quick wins - high impact, low effort recommendations"""
        quick_wins = []
        
        for rec in recommendations:
            if rec.estimated_effort == 'low' and rec.impact in ['high', 'medium']:
                quick_wins.append(rec)
                if len(quick_wins) >= limit:
                    break
        
        return quick_wins
    
    def get_implementation_roadmap(self, recommendations: List[Recommendation]) -> Dict[str, List]:
        """Create implementation roadmap grouped by effort"""
        roadmap = {
            'quick_wins': [],
            'short_term': [],
            'long_term': []
        }
        
        for rec in recommendations:
            if rec.estimated_effort == 'low':
                roadmap['quick_wins'].append(self._rec_to_dict(rec))
            elif rec.estimated_effort == 'medium':
                roadmap['short_term'].append(self._rec_to_dict(rec))
            else:
                roadmap['long_term'].append(self._rec_to_dict(rec))
        
        return roadmap
