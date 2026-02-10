"""
Flask Web Application
=====================
Personalized Obesity Risk Prediction and Nutrition Recommendation System
"""

from flask import Flask, render_template, request, jsonify
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.prediction import ObesityPredictor
from src.nutrition_recommendation import NutritionRecommender

app = Flask(__name__)

# Initialize predictor and recommender
predictor = ObesityPredictor(
    model_path='models/ensemble_model.pkl',
    preprocessor_path='models/preprocessor.pkl'
)
recommender = NutritionRecommender()

# Load models on startup
predictor.load_model()
predictor.load_preprocessor()


@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        # Get form data
        patient_data = {
            'Age': int(request.form.get('age')),
            'Gender': request.form.get('gender'),
            'Height': float(request.form.get('height')),
            'Weight': float(request.form.get('weight')),
            'family_history_with_overweight': request.form.get('family_history'),
            'FAVC': request.form.get('favc'),
            'FCVC': float(request.form.get('fcvc')),
            'NCP': int(request.form.get('ncp')),
            'CAEC': request.form.get('caec'),
            'SMOKE': request.form.get('smoke'),
            'CH2O': float(request.form.get('ch2o')),
            'SCC': request.form.get('scc'),
            'FAF': int(request.form.get('faf')),
            'TUE': int(request.form.get('tue')),
            'CALC': request.form.get('calc'),
            'MTRANS': request.form.get('mtrans')
        }
        
        # Make prediction
        result = predictor.predict_single(patient_data)
        
        # Get nutrition recommendations
        nutrition_plan = recommender.generate_nutrition_report(
            result['risk_level'],
            {**patient_data, 'BMI': result['bmi']}
        )
        
        # Get risk description
        risk_description = predictor.get_risk_description(result['risk_level'])
        
        # Prepare response
        response = {
            'success': True,
            'prediction': {
                'risk_level': result['risk_level'],
                'confidence': round(result['confidence'] * 100, 2),
                'bmi': round(result['bmi'], 2),
                'description': risk_description
            },
            'nutrition': {
                'calorie_min': nutrition_plan['calorie_recommendation']['min'],
                'calorie_max': nutrition_plan['calorie_recommendation']['max'],
                'goal': nutrition_plan['calorie_recommendation']['goal'],
                'meal_plan': {
                    'breakfast': [
                        {
                            'name': item['name'],
                            'calories': item['calories']
                        }
                        for item in nutrition_plan['daily_meal_plan']['breakfast']['items']
                    ],
                    'lunch': [
                        {
                            'name': item['name'],
                            'calories': item['calories']
                        }
                        for item in nutrition_plan['daily_meal_plan']['lunch']['items']
                    ],
                    'dinner': [
                        {
                            'name': item['name'],
                            'calories': item['calories']
                        }
                        for item in nutrition_plan['daily_meal_plan']['dinner']['items']
                    ],
                    'snacks': [
                        {
                            'name': item['name'],
                            'calories': item['calories']
                        }
                        for item in nutrition_plan['daily_meal_plan']['snacks']['items']
                    ]
                },
                'lifestyle_tips': nutrition_plan['lifestyle_recommendations'][:5]
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


if __name__ == '__main__':
    import os
    
    # Get port from environment variable (for deployment) or use 5000 for local
    port = int(os.environ.get('PORT', 5000))
    
    # Debug mode: False for production, True for local development
    debug = os.environ.get('DEBUG', 'True') == 'True'
    
    print("\n" + "="*60)
    print("🚀 OBESITY PREDICTION WEB APPLICATION")
    print("="*60)
    print("\n✓ Models loaded successfully")
    print("✓ Server starting...")
    print(f"\n📱 Open your browser and visit:")
    print(f"   http://127.0.0.1:{port}")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
