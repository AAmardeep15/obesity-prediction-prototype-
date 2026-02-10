"""
Prediction Module
=================
This module handles making predictions on new data using trained models.
"""

import numpy as np
import pandas as pd
import joblib
import os


class ObesityPredictor:
    """Prediction pipeline for obesity risk assessment."""
    
    def __init__(self, model_path='models/ensemble_model.pkl', preprocessor_path='models/preprocessor.pkl'):
        """Initialize predictor with saved model and preprocessor."""
        self.model = None
        self.preprocessor = None
        self.model_path = model_path
        self.preprocessor_path = preprocessor_path
        self.obesity_categories = [
            'Insufficient_Weight',
            'Normal_Weight',
            'Overweight_Level_I',
            'Overweight_Level_II',
            'Obesity_Type_I',
            'Obesity_Type_II',
            'Obesity_Type_III'
        ]
    
    def load_model(self):
        """Load trained model from disk."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"✓ Model loaded from {self.model_path}")
        else:
            print(f"✗ Model file not found at {self.model_path}")
            return False
        return True
    
    def load_preprocessor(self):
        """Load preprocessor from disk."""
        if os.path.exists(self.preprocessor_path):
            self.preprocessor = joblib.load(self.preprocessor_path)
            print(f"✓ Preprocessor loaded from {self.preprocessor_path}")
        else:
            print(f"✗ Preprocessor file not found at {self.preprocessor_path}")
            return False
        return True
    
    def predict_single(self, patient_data):
        """
        Predict obesity risk for a single patient.
        
        Parameters:
        -----------
        patient_data : dict
            Dictionary containing patient features
            
        Returns:
        --------
        dict : Prediction results with risk level and confidence
        """
        if self.model is None or self.preprocessor is None:
            print("⚠ Model or preprocessor not loaded. Call load_model() and load_preprocessor() first.")
            return None
        
        # Preprocess the input
        X_processed = self.preprocessor.preprocess_single_sample(patient_data)
        
        # Make prediction
        prediction = self.model.predict(X_processed)[0]
        
        # Get prediction probabilities if available
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X_processed)[0]
            confidence = probabilities.max()
        else:
            probabilities = None
            confidence = None
        
        # Map prediction to category name
        risk_level = self.preprocessor.target_encoder.inverse_transform([prediction])[0]
        
        result = {
            'risk_level': risk_level,
            'risk_code': int(prediction),
            'confidence': float(confidence) if confidence else None,
            'bmi': patient_data.get('Weight', 0) / (patient_data.get('Height', 1) ** 2) if 'Weight' in patient_data and 'Height' in patient_data else None
        }
        
        return result
    
    def predict_batch(self, patients_df):
        """
        Predict obesity risk for multiple patients.
        
        Parameters:
        -----------
        patients_df : pd.DataFrame
            DataFrame containing patient features
            
        Returns:
        --------
        pd.DataFrame : DataFrame with predictions
        """
        if self.model is None or self.preprocessor is None:
            print("⚠ Model or preprocessor not loaded.")
            return None
        
        predictions = []
        
        for idx, row in patients_df.iterrows():
            patient_data = row.to_dict()
            result = self.predict_single(patient_data)
            predictions.append(result)
        
        return pd.DataFrame(predictions)
    
    def get_risk_description(self, risk_level):
        """Get human-readable description of obesity risk level."""
        descriptions = {
            'Insufficient_Weight': 'Underweight - May need to gain weight for optimal health',
            'Normal_Weight': 'Normal weight - Maintain current healthy lifestyle',
            'Overweight_Level_I': 'Overweight Level I - Moderate risk, lifestyle changes recommended',
            'Overweight_Level_II': 'Overweight Level II - Increased risk, medical consultation advised',
            'Obesity_Type_I': 'Obesity Type I - High risk, medical intervention recommended',
            'Obesity_Type_II': 'Obesity Type II - Very high risk, immediate medical attention needed',
            'Obesity_Type_III': 'Obesity Type III - Extreme risk, urgent medical intervention required'
        }
        
        return descriptions.get(risk_level, 'Unknown risk level')


def predict_obesity_risk(patient_data, model_path='models/ensemble_model.pkl', 
                         preprocessor_path='models/preprocessor.pkl'):
    """
    Convenience function for quick predictions.
    
    Parameters:
    -----------
    patient_data : dict
        Patient information
    model_path : str
        Path to saved model
    preprocessor_path : str
        Path to saved preprocessor
        
    Returns:
    --------
    dict : Prediction results
    """
    predictor = ObesityPredictor(model_path, preprocessor_path)
    
    if predictor.load_model() and predictor.load_preprocessor():
        return predictor.predict_single(patient_data)
    else:
        return None


# Example usage
if __name__ == "__main__":
    print("Prediction Module - Test Mode\n")
    
    # Example patient data
    sample_patient = {
        'Age': 25,
        'Gender': 'Male',
        'Height': 1.75,
        'Weight': 85,
        'family_history_with_overweight': 'yes',
        'FAVC': 'yes',
        'FCVC': 2.5,
        'NCP': 3,
        'CAEC': 'Sometimes',
        'SMOKE': 'no',
        'CH2O': 2.0,
        'SCC': 'no',
        'FAF': 2,
        'TUE': 1,
        'CALC': 'Sometimes',
        'MTRANS': 'Public_Transportation'
    }
    
    print("Sample patient data:")
    for key, value in sample_patient.items():
        print(f"  {key}: {value}")
    
    print("\n✓ Prediction module loaded successfully!")
    print("Note: To make predictions, train the model first using main.py")
