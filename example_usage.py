"""
Example Usage Script
====================
This script demonstrates how to use the trained model for predictions
and nutrition recommendations.
"""

from src.prediction import ObesityPredictor
from src.nutrition_recommendation import NutritionRecommender


def example_prediction():
    """Example of making a prediction for a new patient."""
    
    # Initialize predictor
    predictor = ObesityPredictor(
        model_path='models/ensemble_model.pkl',
        preprocessor_path='models/preprocessor.pkl'
    )
    
    # Load models
    if not predictor.load_model() or not predictor.load_preprocessor():
        print("⚠ Please train the model first by running: python main.py")
        return
    
    # Example patient data
    patient = {
        'Age': 32,
        'Gender': 'Female',
        'Height': 1.65,
        'Weight': 72,
        'family_history_with_overweight': 'yes',
        'FAVC': 'no',
        'FCVC': 3.0,
        'NCP': 3,
        'CAEC': 'Sometimes',
        'SMOKE': 'no',
        'CH2O': 2.5,
        'SCC': 'yes',
        'FAF': 3,
        'TUE': 1,
        'CALC': 'no',
        'MTRANS': 'Walking'
    }
    
    print("\n" + "="*60)
    print("PATIENT INFORMATION")
    print("="*60)
    for key, value in patient.items():
        print(f"  {key:35s}: {value}")
    
    # Make prediction
    result = predictor.predict_single(patient)
    
    print("\n" + "="*60)
    print("PREDICTION RESULTS")
    print("="*60)
    print(f"\nObesity Risk Level: {result['risk_level']}")
    print(f"Confidence: {result['confidence']*100:.2f}%")
    print(f"BMI: {result['bmi']:.2f}")
    print(f"\nRisk Description:")
    print(f"  {predictor.get_risk_description(result['risk_level'])}")
    
    # Get nutrition recommendations
    recommender = NutritionRecommender()
    nutrition_plan = recommender.generate_nutrition_report(
        result['risk_level'],
        {**patient, 'BMI': result['bmi']}
    )
    
    print("\n" + "="*60)
    print("NUTRITION RECOMMENDATIONS")
    print("="*60)
    
    calorie_rec = nutrition_plan['calorie_recommendation']
    print(f"\nDaily Calorie Target: {calorie_rec['min']}-{calorie_rec['max']} kcal")
    print(f"Goal: {calorie_rec['goal']}")
    
    print("\n📋 Sample Breakfast:")
    for item in nutrition_plan['daily_meal_plan']['breakfast']['items']:
        print(f"  • {item['name']:30s} {item['calories']:4.0f} kcal")
    
    print("\n💡 Top 3 Lifestyle Tips:")
    for i, tip in enumerate(nutrition_plan['lifestyle_recommendations'][:3], 1):
        print(f"  {i}. {tip}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    example_prediction()
