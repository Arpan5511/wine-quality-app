"""
Flask Web Application for Wine Quality Prediction.
Provides REST API and web interface for predictions.
"""

from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os
import json
from preprocessing import preprocess_single_sample
from datetime import datetime

app = Flask(__name__)

# Configuration
MODELS_DIR = 'models'
MODEL_NAME = 'random_forest_model.pkl'
SCALER_NAME = 'scaler.pkl'
FEATURE_NAMES_FILE = 'feature_names.pkl'

# Load model, scaler, and feature names
model = None
scaler = None
feature_names = None
model_loaded = False

def load_model():
    """Load trained model and scaler."""
    global model, scaler, feature_names, model_loaded
    
    try:
        model_path = os.path.join(MODELS_DIR, MODEL_NAME)
        scaler_path = os.path.join(MODELS_DIR, SCALER_NAME)
        feature_names_path = os.path.join(MODELS_DIR, FEATURE_NAMES_FILE)
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            
            if os.path.exists(feature_names_path):
                feature_names = joblib.load(feature_names_path)
            else:
                # Default feature names if file not found
                feature_names = [
                    'fixed acidity', 'volatile acidity', 'citric acid',
                    'residual sugar', 'chlorides', 'free sulfur dioxide',
                    'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol'
                ]
            
            model_loaded = True
            print("[OK] Model, scaler, and features loaded successfully!")
        else:
            print("[ERROR] Model or scaler files not found!")
            print(f"   Expected: {model_path}, {scaler_path}")
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")


@app.route('/')
def home():
    """Home page with prediction form."""
    return render_template('index.html', model_loaded=model_loaded)


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    API endpoint for wine quality prediction.
    Expects JSON with wine features.
    """
    if not model_loaded:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 400
    
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create feature dictionary with numeric values
        sample_dict = {}
        for feature in feature_names:
            key = feature.replace(' ', '_')
            value = data.get(key)
            
            if value is None:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
            
            try:
                sample_dict[feature] = float(value)
            except ValueError:
                return jsonify({'error': f'Invalid value for {feature}: {value}'}), 400
        
        # Preprocess the sample
        scaled_sample = preprocess_single_sample(sample_dict, scaler, feature_names)
        
        # Make prediction
        prediction = model.predict(scaled_sample)[0]
        
        # Clamp prediction to valid range (0-10)
        prediction = max(0, min(10, prediction))
        
        # Determine quality category
        if prediction < 4:
            quality_category = 'Poor'
        elif prediction < 6:
            quality_category = 'Average'
        elif prediction < 8:
            quality_category = 'Good'
        else:
            quality_category = 'Excellent'
        
        return jsonify({
            'success': True,
            'prediction': round(prediction, 2),
            'category': quality_category,
            'features_used': feature_names,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/features', methods=['GET'])
def get_features():
    """Get list of features with descriptions and typical ranges."""
    if not model_loaded:
        return jsonify({'error': 'Model not loaded'}), 400
    
    feature_info = {
        'fixed acidity': {
            'unit': 'g/dm³',
            'description': 'Most acids involved in wine are fixed',
            'typical_min': 4.6,
            'typical_max': 15.9
        },
        'volatile acidity': {
            'unit': 'g/dm³',
            'description': 'Too much acetic acid can cause unpleasant vinegar taste',
            'typical_min': 0.12,
            'typical_max': 1.58
        },
        'citric acid': {
            'unit': 'g/dm³',
            'description': 'Found in small quantities, adds freshness and flavor',
            'typical_min': 0.0,
            'typical_max': 1.0
        },
        'residual sugar': {
            'unit': 'g/dm³',
            'description': 'Sugar remaining after fermentation',
            'typical_min': 0.9,
            'typical_max': 15.5
        },
        'chlorides': {
            'unit': 'g/dm³',
            'description': 'Amount of salt in the wine',
            'typical_min': 0.012,
            'typical_max': 0.611
        },
        'free sulfur dioxide': {
            'unit': 'mg/dm³',
            'description': 'Prevents microbial growth and oxidation',
            'typical_min': 1.0,
            'typical_max': 72.0
        },
        'total sulfur dioxide': {
            'unit': 'mg/dm³',
            'description': 'Amount of free and bound forms of SO2',
            'typical_min': 6.0,
            'typical_max': 289.0
        },
        'density': {
            'unit': 'g/cm³',
            'description': 'Density of the wine (depends on alcohol and sugar)',
            'typical_min': 0.9901,
            'typical_max': 1.0037
        },
        'pH': {
            'unit': 'none',
            'description': 'Describes acidity level (0-14 scale)',
            'typical_min': 2.74,
            'typical_max': 4.01
        },
        'sulphates': {
            'unit': 'g/dm³',
            'description': 'Wine additive that acts as antimicrobial and antioxidant',
            'typical_min': 0.33,
            'typical_max': 2.0
        },
        'alcohol': {
            'unit': '% vol',
            'description': 'Percent alcohol content by volume',
            'typical_min': 8.4,
            'typical_max': 14.9
        }
    }
    
    return jsonify({
        'features': feature_names,
        'feature_details': feature_info
    })


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get model statistics."""
    if not model_loaded:
        return jsonify({'error': 'Model not loaded'}), 400
    
    return jsonify({
        'model_type': type(model).__name__,
        'features_count': len(feature_names),
        'features': feature_names,
        'prediction_range': [0, 10],
        'quality_categories': {
            'poor': '< 4.0',
            'average': '4.0 - 6.0',
            'good': '6.0 - 8.0',
            'excellent': '> 8.0'
        }
    })


@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """Get sample data for testing."""
    sample_data = {
        'sample_1': {
            'name': 'Good Red Wine',
            'data': {
                'fixed_acidity': 7.4,
                'volatile_acidity': 0.7,
                'citric_acid': 0.0,
                'residual_sugar': 1.9,
                'chlorides': 0.076,
                'free_sulfur_dioxide': 11.0,
                'total_sulfur_dioxide': 34.0,
                'density': 0.9978,
                'pH': 3.51,
                'sulphates': 0.56,
                'alcohol': 9.4
            }
        },
        'sample_2': {
            'name': 'High Quality Wine',
            'data': {
                'fixed_acidity': 8.5,
                'volatile_acidity': 0.28,
                'citric_acid': 0.56,
                'residual_sugar': 1.8,
                'chlorides': 0.05,
                'free_sulfur_dioxide': 16.0,
                'total_sulfur_dioxide': 56.0,
                'density': 0.99602,
                'pH': 3.58,
                'sulphates': 1.55,
                'alcohol': 11.6
            }
        },
        'sample_3': {
            'name': 'Average Quality Wine',
            'data': {
                'fixed_acidity': 6.2,
                'volatile_acidity': 0.66,
                'citric_acid': 0.48,
                'residual_sugar': 1.2,
                'chlorides': 0.029,
                'free_sulfur_dioxide': 29.0,
                'total_sulfur_dioxide': 40.0,
                'density': 0.99574,
                'pH': 3.42,
                'sulphates': 1.04,
                'alcohol': 10.5
            }
        }
    }
    
    return jsonify(sample_data)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("WINE QUALITY PREDICTION - WEB APPLICATION")
    print("="*70 + "\n")
    
    # Load model
    print("Loading model...")
    load_model()
    
    if not model_loaded:
        print("\n[WARNING] Model not loaded. Please run 'python train.py' first to train the model.\n")
    else:
        print("\nStarting Flask application...")
        print("Visit http://localhost:5000 to access the application\n")
    
    # Get port from environment variable (Render sets this), default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Run app
    app.run(debug=debug, host='0.0.0.0', port=port)
