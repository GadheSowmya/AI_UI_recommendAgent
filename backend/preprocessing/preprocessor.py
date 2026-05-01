"""
Preprocessing module for UI screenshots and code analysis
Handles image preprocessing and code parsing
"""

import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Union, Tuple, Dict, List
import re
from bs4 import BeautifulSoup


class UIPreprocessor:
    """Preprocesses UI screenshots for analysis"""
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
    
    def process_image(self, image_input: Union[str, bytes]) -> np.ndarray:
        """
        Process image from file path or bytes
        
        Args:
            image_input: File path or byte array
            
        Returns:
            Processed numpy array ready for model input
        """
        if isinstance(image_input, str):
            img = cv2.imread(image_input)
        else:
            nparr = np.frombuffer(image_input, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to read image")
        
        # Resize
        img = cv2.resize(img, self.target_size)
        
        # Normalize
        img = img.astype(np.float32) / 255.0
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        return img
    
    def extract_ui_regions(self, image: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Extract key UI regions from screenshot
        
        Returns:
            Dictionary with regions: header, content, footer, sidebar
        """
        h, w = image.shape[:2]
        
        regions = {
            'header': image[:int(h*0.15), :],
            'content': image[int(h*0.15):int(h*0.85), :],
            'footer': image[int(h*0.85):, :],
            'left_sidebar': image[:, :int(w*0.15)],
            'right_sidebar': image[:, int(w*0.85):]
        }
        
        return regions
    
    def calculate_color_histogram(self, image: np.ndarray) -> Dict[str, float]:
        """Calculate color statistics"""
        img_hsv = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
        
        # Count pixels by hue (color)
        hist_hue = cv2.calcHist([img_hsv], [0], None, [180], [0, 180])
        
        colors = {
            'red_ratio': float(np.sum(hist_hue[:10] + hist_hue[170:])) / hist_hue.size,
            'green_ratio': float(np.sum(hist_hue[40:80])) / hist_hue.size,
            'blue_ratio': float(np.sum(hist_hue[100:130])) / hist_hue.size,
        }
        
        return colors


class CodePreprocessor:
    """Preprocesses HTML/CSS/JavaScript code for analysis"""
    
    def __init__(self):
        self.patterns = {
            'semantic_tags': ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer'],
            'aria_attrs': ['aria-label', 'aria-hidden', 'role'],
        }
    
    def parse_html(self, html_code: str) -> Dict[str, any]:
        """Parse HTML and extract structure information"""
        try:
            soup = BeautifulSoup(html_code, 'html.parser')
            
            analysis = {
                'total_elements': len(soup.find_all(True)),
                'semantic_tags': self._count_semantic_tags(soup),
                'accessibility_score': self._calculate_accessibility(soup),
                'has_meta_viewport': bool(soup.find('meta', attrs={'name': 'viewport'})),
                'has_title': bool(soup.find('title')),
                'has_favicon': bool(soup.find('link', attrs={'rel': 'icon'})),
                'images_without_alt': self._count_images_without_alt(soup),
                'buttons_accessible': self._check_buttons(soup),
                'form_labels': self._check_form_labels(soup),
            }
            
            return analysis
        except Exception as e:
            return {'error': str(e)}
    
    def _count_semantic_tags(self, soup) -> int:
        count = 0
        for tag in self.patterns['semantic_tags']:
            count += len(soup.find_all(tag))
        return count
    
    def _calculate_accessibility(self, soup) -> float:
        """Calculate accessibility score 0-100"""
        score = 50  # base score
        
        # Check for ARIA attributes
        aria_elements = len(soup.find_all(attrs={'role': True}))
        score += min(aria_elements * 2, 20)
        
        # Check alt text on images
        images = soup.find_all('img')
        if images:
            alt_ratio = len([img for img in images if img.get('alt')]) / len(images)
            score += alt_ratio * 20
        
        # Check form labels
        forms = soup.find_all('form')
        if forms:
            labels = soup.find_all('label')
            label_ratio = len(labels) / max(len(forms), 1)
            score += min(label_ratio * 10, 10)
        
        return min(score, 100)
    
    def _count_images_without_alt(self, soup) -> int:
        images = soup.find_all('img')
        return len([img for img in images if not img.get('alt')])
    
    def _check_buttons(self, soup) -> Dict[str, int]:
        buttons = soup.find_all(['button', 'a'])
        accessible = len([b for b in buttons if b.get('aria-label') or b.text.strip()])
        return {
            'total': len(buttons),
            'accessible': accessible
        }
    
    def _check_form_labels(self, soup) -> Dict[str, int]:
        inputs = soup.find_all(['input', 'textarea', 'select'])
        labels = soup.find_all('label')
        return {
            'total_inputs': len(inputs),
            'total_labels': len(labels),
            'label_ratio': len(labels) / max(len(inputs), 1) if inputs else 0
        }
    
    def extract_css_metrics(self, css_code: str) -> Dict[str, any]:
        """Extract CSS metrics"""
        metrics = {
            'selectors_count': len(re.findall(r'[^{]*\{', css_code)),
            'media_queries': len(re.findall(r'@media', css_code)),
            'font_families': len(set(re.findall(r'font-family\s*:\s*([^;]+)', css_code))),
            'colors_count': len(set(re.findall(r'#[0-9a-fA-F]{6}|rgb\([^)]+\)', css_code))),
            'animations': len(re.findall(r'@keyframes|animation:', css_code)),
        }
        return metrics


class DataPreprocessor:
    """Combines image and code preprocessing"""
    
    def __init__(self):
        self.ui_processor = UIPreprocessor()
        self.code_processor = CodePreprocessor()
    
    def preprocess_ui_screenshot(self, image_data: bytes) -> Dict:
        """Preprocess UI screenshot"""
        processed_image = self.ui_processor.process_image(image_data)
        regions = self.ui_processor.extract_ui_regions(processed_image)
        colors = self.ui_processor.calculate_color_histogram(processed_image)
        
        return {
            'image': processed_image,
            'regions': regions,
            'colors': colors,
            'image_shape': processed_image.shape
        }
    
    def preprocess_html_code(self, html_code: str) -> Dict:
        """Preprocess HTML code"""
        return self.code_processor.parse_html(html_code)
    
    def preprocess_full_code(self, html: str, css: str = "", js: str = "") -> Dict:
        """Preprocess complete web code"""
        result = {
            'html': self.code_processor.parse_html(html),
        }
        
        if css:
            result['css'] = self.code_processor.extract_css_metrics(css)
        
        return result
