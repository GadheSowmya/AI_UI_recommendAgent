"""
Main Flask Application - AI UI Recommendation Agent Backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import base64
import io
from PIL import Image
import os
from dotenv import load_dotenv

# Import modules
from preprocessing.preprocessor import DataPreprocessor
from models.ai_models import AIAnalyzer
from ux_engine.rules import UXRuleEngine
from models.recommendation_generator import RecommendationGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
preprocessor = DataPreprocessor()
ai_analyzer = AIAnalyzer()
ux_engine = UXRuleEngine()
recommendation_generator = RecommendationGenerator()

# Store analysis results
analysis_history = []


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'AI UI Recommendation Agent'
    }), 200


@app.route('/api/analyze/screenshot', methods=['POST'])
def analyze_screenshot():
    """Analyze UI screenshot"""
    try:
        # Get image from request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        image_data = image_file.read()
        
        # Preprocess image
        logger.info('Preprocessing screenshot...')
        processed_data = preprocessor.preprocess_ui_screenshot(image_data)
        
        # Analyze with AI models
        logger.info('Running CV analysis...')
        cv_analysis = ai_analyzer.analyze_ui_screenshot(processed_data['image'])
        
        # Get quality scores
        logger.info('Calculating quality scores...')
        quality_scores = ai_analyzer.predict_quality_scores(
            cv_analysis['visual_features'],
            {}
        )
        
        # Evaluate UX rules
        logger.info('Evaluating UX rules...')
        rule_results = ux_engine.evaluate_all_rules(cv_analysis['visual_features'])
        
        # Get category summary
        category_summary = ux_engine.get_category_summary(rule_results)
        
        # Generate recommendations
        logger.info('Generating recommendations...')
        analysis_results = {
            'rule_results': rule_results,
            'quality_scores': quality_scores,
            'category_summary': category_summary,
            'visual_features': cv_analysis['visual_features']
        }
        report = recommendation_generator.generate_detailed_report(analysis_results)
        
        # Prepare response
        response = {
            'status': 'success',
            'analysis_type': 'screenshot',
            'timestamp': datetime.utcnow().isoformat(),
            'scores': quality_scores,
            'report': report,
            'visual_analysis': cv_analysis['visual_features'],
            'rule_details': {k: {
                'name': v['name'],
                'category': v['category'],
                'severity': v['severity'],
                'passed': v['passed'],
                'message': v['message'],
                'score': v['score']
            } for k, v in rule_results.items()}
        }
        
        # Store in history
        analysis_history.append(response)
        
        logger.info('Analysis completed successfully')
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Error analyzing screenshot: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze/code', methods=['POST'])
def analyze_code():
    """Analyze HTML/CSS/JavaScript code"""
    try:
        data = request.get_json()
        
        if not data or 'html' not in data:
            return jsonify({'error': 'No HTML code provided'}), 400
        
        html_code = data.get('html', '')
        css_code = data.get('css', '')
        js_code = data.get('js', '')
        
        # Preprocess code
        logger.info('Preprocessing code...')
        processed_data = preprocessor.preprocess_full_code(html_code, css_code, js_code)
        
        # Analyze with AI models
        logger.info('Running code analysis...')
        code_analysis = ai_analyzer.analyze_code(
            html_code,
            css_code,
            processed_data.get('html'),
            processed_data.get('css')
        )
        
        # Evaluate UX rules
        logger.info('Evaluating UX rules...')
        rule_results = ux_engine.evaluate_all_rules(processed_data.get('html', {}))
        
        # Get category summary
        category_summary = ux_engine.get_category_summary(rule_results)
        
        # Extract quality scores
        quality_scores = {
            'semantic_structure_score': code_analysis['html_analysis'].get('semantic_structure_score', 0),
            'accessibility_score': code_analysis['html_analysis'].get('accessibility_text_score', 0),
            'readability_score': code_analysis['html_analysis'].get('readability_score', 0),
            'code_quality_score': sum(code_analysis['code_quality'].values()) / len(code_analysis['code_quality']) if code_analysis['code_quality'] else 0
        }
        quality_scores['overall_quality_score'] = sum(quality_scores.values()) / len(quality_scores)
        
        # Generate recommendations
        logger.info('Generating recommendations...')
        analysis_results = {
            'rule_results': rule_results,
            'quality_scores': quality_scores,
            'category_summary': category_summary
        }
        report = recommendation_generator.generate_detailed_report(analysis_results)
        
        # Prepare response
        response = {
            'status': 'success',
            'analysis_type': 'code',
            'timestamp': datetime.utcnow().isoformat(),
            'scores': quality_scores,
            'report': report,
            'code_analysis': {
                'html': code_analysis['html_analysis'],
                'code_quality': code_analysis['code_quality']
            },
            'rule_details': {k: {
                'name': v['name'],
                'category': v['category'],
                'severity': v['severity'],
                'passed': v['passed'],
                'message': v['message'],
                'score': v['score']
            } for k, v in rule_results.items()}
        }
        
        # Store in history
        analysis_history.append(response)
        
        logger.info('Code analysis completed successfully')
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Error analyzing code: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze/hybrid', methods=['POST'])
def analyze_hybrid():
    """Analyze both screenshot and code together"""
    try:
        # Check for required data
        if 'image' not in request.files or 'html' not in request.form:
            return jsonify({'error': 'Both image and HTML code required'}), 400
        
        image_file = request.files['image']
        html_code = request.form.get('html', '')
        css_code = request.form.get('css', '')
        
        # Process image
        logger.info('Processing image and code for hybrid analysis...')
        image_data = image_file.read()
        processed_image = preprocessor.preprocess_ui_screenshot(image_data)
        
        # Process code
        processed_code = preprocessor.preprocess_full_code(html_code, css_code)
        
        # Run AI analysis on both
        cv_analysis = ai_analyzer.analyze_ui_screenshot(processed_image['image'])
        code_analysis = ai_analyzer.analyze_code(html_code, css_code, processed_code.get('html'))
        
        # Combine metrics for UX evaluation
        combined_metrics = {
            **cv_analysis['visual_features'],
            **processed_code.get('html', {})
        }
        
        # Evaluate rules
        rule_results = ux_engine.evaluate_all_rules(combined_metrics)
        category_summary = ux_engine.get_category_summary(rule_results)
        
        # Generate quality scores
        quality_scores = ai_analyzer.predict_quality_scores(
            cv_analysis['visual_features'],
            processed_code.get('html', {})
        )
        
        # Generate recommendations
        analysis_results = {
            'rule_results': rule_results,
            'quality_scores': quality_scores,
            'category_summary': category_summary
        }
        report = recommendation_generator.generate_detailed_report(analysis_results)
        
        # Prepare response
        response = {
            'status': 'success',
            'analysis_type': 'hybrid',
            'timestamp': datetime.utcnow().isoformat(),
            'scores': quality_scores,
            'report': report,
            'visual_analysis': cv_analysis['visual_features'],
            'code_analysis': code_analysis,
            'rule_details': {k: {
                'name': v['name'],
                'category': v['category'],
                'severity': v['severity'],
                'passed': v['passed'],
                'message': v['message'],
                'score': v['score']
            } for k, v in rule_results.items()}
        }
        
        analysis_history.append(response)
        
        logger.info('Hybrid analysis completed successfully')
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Error in hybrid analysis: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get analysis history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        return jsonify({
            'status': 'success',
            'count': len(analysis_history),
            'history': analysis_history[-limit:]
        }), 200
    except Exception as e:
        logger.error(f'Error fetching history: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/recommendations/<analysis_id>', methods=['GET'])
def get_recommendations(analysis_id):
    """Get specific recommendations"""
    try:
        idx = int(analysis_id)
        if 0 <= idx < len(analysis_history):
            return jsonify({
                'status': 'success',
                'analysis': analysis_history[idx]
            }), 200
        else:
            return jsonify({'error': 'Analysis not found'}), 404
    except Exception as e:
        logger.error(f'Error fetching recommendations: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/export-report', methods=['POST'])
def export_report():
    """Export analysis report as JSON or CSV"""
    try:
        data = request.get_json()
        analysis_idx = data.get('analysis_index', -1)
        format_type = data.get('format', 'json')
        
        if not (0 <= analysis_idx < len(analysis_history)):
            analysis = analysis_history[-1] if analysis_history else None
        else:
            analysis = analysis_history[analysis_idx]
        
        if not analysis:
            return jsonify({'error': 'No analysis available'}), 404
        
        if format_type == 'json':
            return jsonify({
                'status': 'success',
                'report': analysis,
                'format': 'json'
            }), 200
        else:
            return jsonify({'error': 'Format not supported'}), 400
            
    except Exception as e:
        logger.error(f'Error exporting report: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Get all UX rules"""
    try:
        rules_list = []
        for rule in ux_engine.rules:
            rules_list.append({
                'name': rule.name,
                'description': rule.description,
                'category': rule.category,
                'severity': rule.severity
            })
        
        return jsonify({
            'status': 'success',
            'total_rules': len(rules_list),
            'categories': ux_engine.categories,
            'rules': rules_list
        }), 200
    except Exception as e:
        logger.error(f'Error fetching rules: {str(e)}')
        return jsonify({'error': str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False') == 'True'
    app.run(debug=debug, port=port, host='0.0.0.0')
