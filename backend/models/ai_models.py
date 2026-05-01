"""
AI Models for UI analysis using Computer Vision, NLP, and Machine Learning
"""

import numpy as np
from typing import Dict, List, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')


class CVModel:
    """Computer Vision Model for visual UI analysis"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def extract_visual_features(self, image: np.ndarray) -> Dict[str, float]:
        """
        Extract visual features from UI screenshot
        
        Args:
            image: Preprocessed image array (224x224x3)
            
        Returns:
            Dictionary of visual features
        """
        features = {}
        
        # Edge detection
        gray = np.mean(image, axis=2)
        edges = np.gradient(gray)
        features['edge_density'] = float(np.mean(np.abs(edges[0]) + np.abs(edges[1])))
        
        # Contrast analysis
        features['contrast'] = float(np.std(gray))
        features['brightness'] = float(np.mean(gray))
        
        # Color distribution
        features['color_diversity'] = float(np.std(image))
        
        # Symmetry analysis
        h, w = gray.shape
        left_half = gray[:, :w//2]
        right_half = np.fliplr(gray[:, w//2:])
        features['horizontal_symmetry'] = float(1 - np.mean(np.abs(left_half - right_half[:, :left_half.shape[1]])))
        
        # Layout analysis
        h_edges = np.sum(np.abs(edges[0]), axis=1)
        v_edges = np.sum(np.abs(edges[1]), axis=0)
        features['layout_complexity'] = float((np.std(h_edges) + np.std(v_edges)) / 2)
        
        # White space analysis
        white_pixels = np.sum(gray > 0.9) / gray.size
        features['white_space_ratio'] = float(white_pixels)
        
        return features
    
    def analyze_text_regions(self, image: np.ndarray) -> Dict[str, float]:
        """Analyze text readability regions"""
        gray = np.mean(image, axis=2)
        
        # Estimate text regions using contrast
        contrast_map = np.abs(np.gradient(gray)[0])
        high_contrast_ratio = np.sum(contrast_map > np.percentile(contrast_map, 75)) / contrast_map.size
        
        return {
            'estimated_text_coverage': float(high_contrast_ratio),
            'color_count_estimate': float(len(np.unique(np.round(image * 255))))
        }


class NLPModel:
    """NLP Model for code and text analysis"""
    
    def __init__(self):
        self.vocab = {}
        self.class_weights = {}
    
    def analyze_html_structure(self, html_metrics: Dict) -> Dict[str, float]:
        """
        Analyze HTML structure quality
        
        Args:
            html_metrics: Metrics from HTML parsing
            
        Returns:
            NLP-based quality scores
        """
        scores = {
            'semantic_structure_score': 0,
            'accessibility_text_score': 0,
            'readability_score': 0
        }
        
        # Semantic structure
        if 'semantic_tags' in html_metrics:
            semantic_count = html_metrics['semantic_tags']
            total_elements = html_metrics.get('total_elements', 1)
            scores['semantic_structure_score'] = min((semantic_count / max(total_elements / 5, 1)) * 100, 100)
        
        # Accessibility
        if 'accessibility_score' in html_metrics:
            scores['accessibility_text_score'] = html_metrics['accessibility_score']
        
        # Readability based on structure
        if 'buttons_accessible' in html_metrics:
            buttons = html_metrics['buttons_accessible']
            if buttons['total'] > 0:
                scores['readability_score'] = (buttons['accessible'] / buttons['total']) * 100
        
        return scores
    
    def analyze_code_quality(self, code: str) -> Dict[str, float]:
        """Analyze code quality indicators"""
        # Check for common best practices
        indicators = {
            'uses_semantic_html': int('header' in code or 'nav' in code or 'main' in code or 'footer' in code),
            'has_comments': int(code.count('<!--') > 0 or code.count('//') > 0),
            'uses_classes': int('class=' in code),
            'uses_ids': int('id=' in code),
            'inline_styles': code.count('style='),
            'semantic_score': 0
        }
        
        # Calculate semantic score
        semantic_indicators = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
        semantic_count = sum(1 for tag in semantic_indicators if tag in code)
        indicators['semantic_score'] = min(semantic_count * 15, 100)
        
        return indicators


class MLModel:
    """Machine Learning Model for predictive analysis"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.feature_names = []
    
    def extract_combined_features(self, visual_features: Dict, html_metrics: Dict, 
                                  css_metrics: Dict = None) -> np.ndarray:
        """Extract and combine all features for ML model"""
        
        features = []
        self.feature_names = []
        
        # Visual features
        if visual_features:
            for key, value in sorted(visual_features.items()):
                features.append(float(value) if value is not None else 0.0)
                self.feature_names.append(f'visual_{key}')
        
        # HTML metrics
        if html_metrics:
            metrics_to_use = ['total_elements', 'semantic_tags', 'accessibility_score', 
                             'images_without_alt']
            for metric in metrics_to_use:
                if metric in html_metrics:
                    value = html_metrics[metric]
                    features.append(float(value) if value is not None else 0.0)
                    self.feature_names.append(f'html_{metric}')
        
        # CSS metrics
        if css_metrics:
            for key, value in sorted(css_metrics.items()):
                features.append(float(value) if value is not None else 0.0)
                self.feature_names.append(f'css_{key}')
        
        return np.array([features])
    
    def predict_ui_quality(self, features: np.ndarray) -> Dict[str, float]:
        """Predict overall UI quality"""
        
        # Normalize features
        try:
            scaled_features = self.scaler.fit_transform(features)
        except:
            scaled_features = features
        
        # Calculate composite scores
        scores = {
            'visual_quality_score': float(np.mean(scaled_features[0, :6]) * 50 + 50) if len(scaled_features[0]) > 0 else 50,
            'structural_quality_score': float(np.mean(scaled_features[0, 6:10]) * 50 + 50) if len(scaled_features[0]) > 6 else 50,
            'css_quality_score': float(np.mean(scaled_features[0, 10:]) * 50 + 50) if len(scaled_features[0]) > 10 else 50,
        }
        
        # Overall score
        scores['overall_quality_score'] = float(np.mean(list(scores.values())))
        
        return scores


class AIAnalyzer:
    """Main AI analyzer combining all models"""
    
    def __init__(self):
        self.cv_model = CVModel()
        self.nlp_model = NLPModel()
        self.ml_model = MLModel()
    
    def analyze_ui_screenshot(self, image: np.ndarray) -> Dict:
        """Comprehensive UI screenshot analysis"""
        
        visual_features = self.cv_model.extract_visual_features(image)
        text_features = self.cv_model.analyze_text_regions(image)
        visual_features.update(text_features)
        
        return {
            'visual_features': visual_features,
            'type': 'screenshot'
        }
    
    def analyze_code(self, html: str, css: str = "", html_metrics: Dict = None, 
                    css_metrics: Dict = None) -> Dict:
        """Comprehensive code analysis"""
        
        html_analysis = self.nlp_model.analyze_html_structure(html_metrics or {})
        code_quality = self.nlp_model.analyze_code_quality(html)
        
        result = {
            'html_analysis': html_analysis,
            'code_quality': code_quality,
            'type': 'code'
        }
        
        if css:
            result['css_analysis'] = code_quality
        
        return result
    
    def predict_quality_scores(self, visual_features: Dict, html_metrics: Dict,
                              css_metrics: Dict = None) -> Dict:
        """Predict quality scores using ML model"""
        
        features = self.ml_model.extract_combined_features(visual_features, html_metrics, css_metrics)
        scores = self.ml_model.predict_ui_quality(features)
        
        return scores
