"""
Main Application Entry Point
=============================
Personalized Obesity Risk Prediction and Nutrition Recommendation System

This is the main script that orchestrates the entire ML pipeline:
1. Data loading and preprocessing
2. Model training (Logistic Regression, Random Forest, Gradient Boosting)
3. Ensemble model creation
4. Model evaluation
5. Prediction and nutrition recommendation demonstration
"""

import os
import sys
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from src.data_preprocessing import ObesityDataPreprocessor
from src.model_training import ObesityModelTrainer
from src.evaluation import ModelEvaluator
from src.prediction import ObesityPredictor
from src.nutrition_recommendation import NutritionRecommender

import joblib


def create_sample_dataset():
    """
    Create a sample obesity dataset for demonstration.
    This simulates a real obesity dataset with various features.
    """
    print("\n" + "="*60)
    print("CREATING SAMPLE DATASET")
    print("="*60 + "\n")
    
    np.random.seed(42)
    n_samples = 500
    
    # Generate synthetic data
    data = {
        'Age': np.random.randint(18, 65, n_samples),
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'Height': np.random.uniform(1.50, 1.95, n_samples),
        'Weight': np.random.uniform(45, 130, n_samples),
        'family_history_with_overweight': np.random.choice(['yes', 'no'], n_samples, p=[0.6, 0.4]),
        'FAVC': np.random.choice(['yes', 'no'], n_samples, p=[0.7, 0.3]),
        'FCVC': np.random.uniform(1, 3, n_samples),
        'NCP': np.random.randint(1, 5, n_samples),
        'CAEC': np.random.choice(['no', 'Sometimes', 'Frequently', 'Always'], n_samples),
        'SMOKE': np.random.choice(['yes', 'no'], n_samples, p=[0.2, 0.8]),
        'CH2O': np.random.uniform(1, 3, n_samples),
        'SCC': np.random.choice(['yes', 'no'], n_samples, p=[0.3, 0.7]),
        'FAF': np.random.randint(0, 4, n_samples),
        'TUE': np.random.randint(0, 3, n_samples),
        'CALC': np.random.choice(['no', 'Sometimes', 'Frequently', 'Always'], n_samples),
        'MTRANS': np.random.choice(['Automobile', 'Motorbike', 'Bike', 'Public_Transportation', 'Walking'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate BMI and assign obesity categories based on BMI
    df['BMI'] = df['Weight'] / (df['Height'] ** 2)
    
    def assign_obesity_category(bmi):
        if bmi < 18.5:
            return 'Insufficient_Weight'
        elif bmi < 25:
            return 'Normal_Weight'
        elif bmi < 27:
            return 'Overweight_Level_I'
        elif bmi < 30:
            return 'Overweight_Level_II'
        elif bmi < 35:
            return 'Obesity_Type_I'
        elif bmi < 40:
            return 'Obesity_Type_II'
        else:
            return 'Obesity_Type_III'
    
    df['NObeyesdad'] = df['BMI'].apply(assign_obesity_category)
    df = df.drop('BMI', axis=1)  # Remove BMI as it will be recalculated in preprocessing
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/obesity_data.csv', index=False)
    
    print(f"✓ Sample dataset created with {n_samples} records")
    print(f"✓ Saved to: data/obesity_data.csv")
    print(f"\nDataset shape: {df.shape}")
    print(f"\nObesity category distribution:")
    print(df['NObeyesdad'].value_counts())
    
    return df


def main():
    """Main execution pipeline."""
    
    print("\n" + "="*70)
    print(" PERSONALIZED OBESITY RISK PREDICTION SYSTEM")
    print(" UN SDG 3: Good Health and Well-Being")
    print("="*70)
    
    # Step 1: Load or create dataset
    data_path = 'data/obesity_data.csv'
    
    if not os.path.exists(data_path):
        print("\n⚠ Dataset not found. Creating sample dataset...")
        df = create_sample_dataset()
    else:
        print(f"\n✓ Loading dataset from {data_path}")
        df = pd.read_csv(data_path)
        print(f"Dataset shape: {df.shape}")
    
    # Step 2: Data Preprocessing
    print("\n" + "="*70)
    print("STEP 1: DATA PREPROCESSING")
    print("="*70)
    
    preprocessor = ObesityDataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(df, target_column='NObeyesdad')
    
    # Save preprocessor for later use
    os.makedirs('models', exist_ok=True)
    joblib.dump(preprocessor, 'models/preprocessor.pkl')
    print("✓ Preprocessor saved to models/preprocessor.pkl")
    
    # Step 3: Model Training
    print("\n" + "="*70)
    print("STEP 2: MODEL TRAINING")
    print("="*70)
    
    trainer = ObesityModelTrainer(random_state=42)
    
    # Train individual models
    trainer.train_individual_models(X_train, y_train)
    
    # Create ensemble model
    ensemble_model = trainer.create_ensemble_model(X_train, y_train, voting='soft')
    
    # Save models
    trainer.save_models('models')
    
    # Print training summary
    trainer.print_training_summary()
    
    # Step 4: Model Evaluation
    print("\n" + "="*70)
    print("STEP 3: MODEL EVALUATION")
    print("="*70)
    
    # Get class names
    class_names = preprocessor.target_encoder.classes_
    
    evaluator = ModelEvaluator(class_names=class_names)
    
    # Evaluate all models
    models_to_evaluate = {
        'Logistic Regression': trainer.models['Logistic_Regression'],
        'Random Forest': trainer.models['Random_Forest'],
        'Gradient Boosting': trainer.models['Gradient_Boosting'],
        'Ensemble Model': ensemble_model
    }
    
    comparison_df = evaluator.evaluate_multiple_models(models_to_evaluate, X_test, y_test)
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    os.makedirs('outputs', exist_ok=True)
    
    # Plot metrics comparison
    evaluator.plot_metrics_comparison(save_path='outputs/metrics_comparison.png')
    
    # Plot confusion matrix for ensemble model
    evaluator.plot_confusion_matrix('Ensemble Model', save_path='outputs/confusion_matrix_ensemble.png')
    
    # Generate classification report
    evaluator.generate_classification_report('Ensemble Model')
    
    # Step 5: Feature Importance
    print("\n" + "="*70)
    print("STEP 4: FEATURE IMPORTANCE ANALYSIS")
    print("="*70)
    
    feature_importance = trainer.get_feature_importance(preprocessor.feature_names)
    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10).to_string(index=False))
    
    # Step 6: Demonstration - Prediction and Nutrition Recommendation
    print("\n" + "="*70)
    print("STEP 5: PREDICTION & NUTRITION RECOMMENDATION DEMO")
    print("="*70)
    
    # Sample patient for demonstration
    sample_patient = {
        'Age': 28,
        'Gender': 'Male',
        'Height': 1.75,
        'Weight': 88,
        'family_history_with_overweight': 'yes',
        'FAVC': 'yes',
        'FCVC': 2.0,
        'NCP': 3,
        'CAEC': 'Sometimes',
        'SMOKE': 'no',
        'CH2O': 2.0,
        'SCC': 'no',
        'FAF': 1,
        'TUE': 2,
        'CALC': 'Sometimes',
        'MTRANS': 'Public_Transportation'
    }
    
    print("\nSample Patient Profile:")
    print("-" * 40)
    for key, value in sample_patient.items():
        print(f"  {key:35s}: {value}")
    
    # Make prediction
    print("\nMaking prediction...")
    X_sample = preprocessor.preprocess_single_sample(sample_patient)
    prediction = ensemble_model.predict(X_sample)[0]
    prediction_proba = ensemble_model.predict_proba(X_sample)[0]
    
    risk_level = preprocessor.target_encoder.inverse_transform([prediction])[0]
    confidence = prediction_proba.max()
    
    bmi = sample_patient['Weight'] / (sample_patient['Height'] ** 2)
    
    print("\n" + "="*70)
    print("PREDICTION RESULTS")
    print("="*70)
    print(f"\nPredicted Obesity Risk: {risk_level}")
    print(f"Confidence: {confidence*100:.2f}%")
    print(f"Calculated BMI: {bmi:.2f}")
    
    # Generate nutrition recommendations
    print("\n" + "="*70)
    print("PERSONALIZED NUTRITION RECOMMENDATIONS")
    print("="*70)
    
    recommender = NutritionRecommender()
    nutrition_report = recommender.generate_nutrition_report(risk_level, {**sample_patient, 'BMI': bmi})
    
    # Display recommendations
    calorie_rec = nutrition_report['calorie_recommendation']
    print(f"\nDaily Calorie Target: {calorie_rec['min']}-{calorie_rec['max']} kcal")
    print(f"Goal: {calorie_rec['goal']}")
    
    print("\n📋 Sample Daily Meal Plan:")
    print("-" * 40)
    
    for meal_name, meal_data in nutrition_report['daily_meal_plan'].items():
        print(f"\n{meal_name.upper()}:")
        for item in meal_data['items']:
            print(f"  • {item['name']:30s} {item['calories']:4.0f} kcal")
        print(f"  Total: {meal_data['total_calories']:.0f} kcal")
    
    print("\n💡 Lifestyle Recommendations:")
    print("-" * 40)
    for i, tip in enumerate(nutrition_report['lifestyle_recommendations'], 1):
        print(f"  {i}. {tip}")
    
    # Final Summary
    print("\n" + "="*70)
    print("SYSTEM SUMMARY")
    print("="*70)
    print(f"\n✓ Dataset: {len(df)} samples processed")
    print(f"✓ Models trained: 3 individual + 1 ensemble")
    print(f"✓ Best model accuracy: {comparison_df.iloc[0]['Accuracy']:.4f}")
    print(f"✓ Models saved to: models/")
    print(f"✓ Visualizations saved to: outputs/")
    print(f"\n✓ System ready for deployment!")
    
    print("\n" + "="*70)
    print(" PROJECT COMPLETED SUCCESSFULLY")
    print(" Ready for web application integration")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
