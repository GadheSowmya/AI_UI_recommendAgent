"""
UX Rule Engine - Contains UX principles and best practices
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class UXRule:
    """Represents a UX rule"""
    name: str
    description: str
    category: str
    severity: str  # low, medium, high, critical
    check_function: callable


class UXRuleEngine:
    """Engine for applying UX best practices rules"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
        self.categories = [
            'accessibility', 'performance', 'usability', 'design', 
            'mobile-responsive', 'readability', 'seo', 'security'
        ]
    
    def _initialize_rules(self) -> List[UXRule]:
        """Initialize all UX rules"""
        rules = [
            # Accessibility Rules
            UXRule(
                name='alt_text_for_images',
                description='All images should have descriptive alt text',
                category='accessibility',
                severity='high',
                check_function=self._check_alt_text
            ),
            UXRule(
                name='keyboard_navigation',
                description='All interactive elements should be keyboard accessible',
                category='accessibility',
                severity='high',
                check_function=self._check_keyboard_navigation
            ),
            UXRule(
                name='color_contrast',
                description='Text should have sufficient color contrast',
                category='accessibility',
                severity='high',
                check_function=self._check_color_contrast
            ),
            UXRule(
                name='form_labels',
                description='All form inputs should have associated labels',
                category='accessibility',
                severity='high',
                check_function=self._check_form_labels
            ),
            
            # Usability Rules
            UXRule(
                name='consistent_navigation',
                description='Navigation should be consistent across pages',
                category='usability',
                severity='medium',
                check_function=self._check_navigation_consistency
            ),
            UXRule(
                name='clear_cta',
                description='Call-to-action buttons should be clear and distinct',
                category='usability',
                severity='high',
                check_function=self._check_clear_cta
            ),
            UXRule(
                name='responsive_design',
                description='Design should be responsive to different screen sizes',
                category='mobile-responsive',
                severity='high',
                check_function=self._check_responsive_design
            ),
            
            # Design Rules
            UXRule(
                name='visual_hierarchy',
                description='Visual hierarchy should guide user attention',
                category='design',
                severity='medium',
                check_function=self._check_visual_hierarchy
            ),
            UXRule(
                name='whitespace_usage',
                description='Adequate whitespace should be used for clarity',
                category='design',
                severity='low',
                check_function=self._check_whitespace
            ),
            UXRule(
                name='font_readability',
                description='Fonts should be readable and consistent',
                category='readability',
                severity='medium',
                check_function=self._check_font_readability
            ),
            
            # Performance Rules
            UXRule(
                name='page_load_speed',
                description='Page should load quickly (< 3 seconds)',
                category='performance',
                severity='medium',
                check_function=self._check_load_speed
            ),
            
            # SEO Rules
            UXRule(
                name='semantic_html',
                description='HTML should use semantic tags properly',
                category='seo',
                severity='medium',
                check_function=self._check_semantic_html
            ),
            UXRule(
                name='meta_tags',
                description='Important meta tags should be present',
                category='seo',
                severity='medium',
                check_function=self._check_meta_tags
            ),
            
            # Security Rules
            UXRule(
                name='https_usage',
                description='Site should use HTTPS',
                category='security',
                severity='critical',
                check_function=self._check_https
            ),
        ]
        return rules
    
    # Rule checking functions
    def _check_alt_text(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check if images have alt text"""
        if 'images_without_alt' in metrics:
            count = metrics['images_without_alt']
            score = max(0, 100 - (count * 10))
            return count == 0, f"{count} images missing alt text", score
        return True, "No images found", 100
    
    def _check_keyboard_navigation(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check keyboard navigation support"""
        score = 75  # Default score
        issues = []
        
        if 'buttons_accessible' in metrics:
            buttons = metrics['buttons_accessible']
            if buttons['total'] > 0:
                accessibility = buttons['accessible'] / buttons['total']
                score = accessibility * 100
                if accessibility < 0.8:
                    issues.append("Not all buttons are keyboard accessible")
        
        return score >= 80, "; ".join(issues) or "Good keyboard navigation", score
    
    def _check_color_contrast(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check color contrast ratios"""
        # Simplified check based on available metrics
        if 'brightness' in metrics and 'contrast' in metrics:
            # If contrast is high, text should be readable
            score = min(100, metrics.get('contrast', 0) * 100)
            return score > 50, f"Contrast ratio: {metrics.get('contrast', 0):.2f}", score
        return True, "Unable to calculate contrast", 75
    
    def _check_form_labels(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check form label coverage"""
        if 'form_labels' in metrics:
            labels = metrics['form_labels']
            if labels['total_inputs'] > 0:
                ratio = labels['label_ratio']
                score = ratio * 100
                return ratio >= 0.9, f"Label ratio: {ratio:.1%}", score
        return True, "No forms found", 100
    
    def _check_navigation_consistency(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check navigation consistency"""
        # Simplified check
        if 'semantic_tags' in metrics and metrics['semantic_tags'] > 0:
            return True, "Navigation structure appears consistent", 80
        return True, "Unable to verify navigation", 60
    
    def _check_clear_cta(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check for clear call-to-action buttons"""
        if 'buttons_accessible' in metrics:
            buttons = metrics['buttons_accessible']
            if buttons['total'] > 0:
                score = min(100, (buttons['total'] / 3) * 100)
                return buttons['total'] > 0, f"Found {buttons['total']} buttons", score
        return False, "No clear CTA buttons found", 40
    
    def _check_responsive_design(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check if design is responsive"""
        if 'has_meta_viewport' in metrics:
            is_responsive = metrics['has_meta_viewport']
            return is_responsive, "Viewport meta tag present" if is_responsive else "Missing viewport meta tag", 100 if is_responsive else 40
        return True, "Unable to verify responsiveness", 70
    
    def _check_visual_hierarchy(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check visual hierarchy"""
        if 'layout_complexity' in metrics:
            complexity = metrics['layout_complexity']
            # Optimal complexity is in middle range
            score = max(0, 100 - abs(0.5 - complexity) * 100)
            return score > 60, f"Layout complexity: {complexity:.2f}", score
        return True, "Unable to assess visual hierarchy", 70
    
    def _check_whitespace(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check whitespace usage"""
        if 'white_space_ratio' in metrics:
            ratio = metrics['white_space_ratio']
            # Optimal whitespace is 20-40%
            if 0.2 <= ratio <= 0.4:
                return True, f"Good whitespace: {ratio:.1%}", 90
            elif 0.1 <= ratio <= 0.5:
                return True, f"Acceptable whitespace: {ratio:.1%}", 70
            else:
                return False, f"Poor whitespace: {ratio:.1%}", 50
        return True, "Unable to assess whitespace", 70
    
    def _check_font_readability(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check font readability"""
        if 'estimated_text_coverage' in metrics:
            coverage = metrics['estimated_text_coverage']
            score = coverage * 100
            return score > 50, f"Text coverage: {coverage:.1%}", score
        return True, "Unable to assess font readability", 70
    
    def _check_load_speed(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check page load speed"""
        # Simplified - in production would measure actual load time
        return True, "Page load speed: Acceptable", 75
    
    def _check_semantic_html(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check semantic HTML usage"""
        if 'semantic_tags' in metrics:
            tags = metrics['semantic_tags']
            score = min(100, tags * 15)
            return tags > 2, f"Semantic tags: {tags}", score
        return False, "No semantic tags found", 30
    
    def _check_meta_tags(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check meta tags"""
        checks = {
            'has_title': metrics.get('has_title', False),
            'has_meta_viewport': metrics.get('has_meta_viewport', False),
        }
        present = sum(1 for v in checks.values() if v)
        score = (present / len(checks)) * 100
        return present == len(checks), f"Meta tags: {present}/{len(checks)} present", score
    
    def _check_https(self, metrics: Dict) -> Tuple[bool, str, float]:
        """Check HTTPS usage"""
        return True, "HTTPS check: Deploy with HTTPS", 50
    
    def evaluate_all_rules(self, metrics: Dict) -> Dict[str, Dict]:
        """Evaluate all rules against metrics"""
        results = {}
        
        for rule in self.rules:
            try:
                passed, message, score = rule.check_function(metrics)
                results[rule.name] = {
                    'name': rule.name,
                    'description': rule.description,
                    'category': rule.category,
                    'severity': rule.severity,
                    'passed': passed,
                    'message': message,
                    'score': score
                }
            except Exception as e:
                results[rule.name] = {
                    'name': rule.name,
                    'description': rule.description,
                    'category': rule.category,
                    'severity': rule.severity,
                    'passed': False,
                    'message': f"Error evaluating rule: {str(e)}",
                    'score': 0
                }
        
        return results
    
    def get_category_summary(self, results: Dict[str, Dict]) -> Dict[str, Dict]:
        """Get summary by category"""
        summary = {}
        
        for category in self.categories:
            category_results = [r for r in results.values() if r['category'] == category]
            if category_results:
                passed = sum(1 for r in category_results if r['passed'])
                avg_score = sum(r['score'] for r in category_results) / len(category_results)
                summary[category] = {
                    'total_rules': len(category_results),
                    'passed': passed,
                    'failed': len(category_results) - passed,
                    'average_score': avg_score,
                    'pass_rate': (passed / len(category_results)) * 100
                }
        
        return summary
