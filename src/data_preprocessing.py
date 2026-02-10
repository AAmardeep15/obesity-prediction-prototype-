"""
Data Preprocessing Module
==========================
This module handles all data preprocessing tasks including:
- Missing value imputation
- Categorical encoding
- Feature scaling
- BMI calculation and feature engineering
- Train-test splitting
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import warnings
warnings.filterwarnings('ignore')


class ObesityDataPreprocessor:
    """
    Comprehensive data preprocessing pipeline for obesity prediction.
    """
    
    def __init__(self):
        """Initialize encoders and scalers."""
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.target_encoder = LabelEncoder()
        self.feature_names = None
        
    def load_data(self, filepath):
        """
        Load obesity dataset from CSV file.
        
        Parameters:
        -----------
        filepath : str
            Path to the CSV file
            
        Returns:
        --------
        pd.DataFrame : Loaded dataset
        """
        try:
            df = pd.read_csv(filepath)
            print(f"✓ Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except FileNotFoundError:
            print(f"✗ Error: File not found at {filepath}")
            return None
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            return None
    
    def handle_missing_values(self, df):
        """
        Handle missing values in the dataset.
        
        Strategy:
        - Numerical features: Fill with median
        - Categorical features: Fill with mode
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
            
        Returns:
        --------
        pd.DataFrame : Dataframe with missing values handled
        """
        df_clean = df.copy()
        
        # Check for missing values
        missing_count = df_clean.isnull().sum().sum()
        
        if missing_count > 0:
            print(f"⚠ Found {missing_count} missing values. Imputing...")
            
            # Numerical columns: fill with median
            numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
            for col in numerical_cols:
                if df_clean[col].isnull().sum() > 0:
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
            
            # Categorical columns: fill with mode
            categorical_cols = df_clean.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if df_clean[col].isnull().sum() > 0:
                    df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
            
            print("✓ Missing values handled successfully")
        else:
            print("✓ No missing values found")
        
        return df_clean
    
    def calculate_bmi(self, df):
        """
        Calculate BMI and create BMI category feature.
        
        BMI = Weight (kg) / (Height (m))^2
        
        Categories:
        - Underweight: BMI < 18.5
        - Normal: 18.5 <= BMI < 25
        - Overweight: 25 <= BMI < 30
        - Obese: BMI >= 30
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe with Height and Weight columns
            
        Returns:
        --------
        pd.DataFrame : Dataframe with BMI features added
        """
        df_bmi = df.copy()
        
        if 'Height' in df_bmi.columns and 'Weight' in df_bmi.columns:
            # Calculate BMI
            df_bmi['BMI'] = df_bmi['Weight'] / (df_bmi['Height'] ** 2)
            
            # Create BMI category
            df_bmi['BMI_Category'] = pd.cut(
                df_bmi['BMI'],
                bins=[0, 18.5, 25, 30, float('inf')],
                labels=['Underweight', 'Normal', 'Overweight', 'Obese']
            )
            
            print("✓ BMI calculated and categorized")
        else:
            print("⚠ Warning: Height or Weight column not found. Skipping BMI calculation.")
        
        return df_bmi
    
    def engineer_features(self, df):
        """
        Create additional engineered features.
        
        New features:
        - Age_Group: Categorized age ranges
        - Activity_Level: Combined physical activity metric
        - Hydration_Score: Water consumption score
        - Meal_Regularity: Based on number of main meals
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
            
        Returns:
        --------
        pd.DataFrame : Dataframe with engineered features
        """
        df_eng = df.copy()
        
        # Age groups
        if 'Age' in df_eng.columns:
            df_eng['Age_Group'] = pd.cut(
                df_eng['Age'],
                bins=[0, 18, 30, 45, 60, 100],
                labels=['Teen', 'Young_Adult', 'Adult', 'Middle_Aged', 'Senior']
            )
        
        # Activity level score (if FAF exists - Frequency of physical Activity)
        if 'FAF' in df_eng.columns:
            df_eng['Activity_Level'] = pd.cut(
                df_eng['FAF'],
                bins=[-1, 0, 1, 2, 4],
                labels=['Sedentary', 'Low', 'Moderate', 'High']
            )
        
        # Hydration score (if CH2O exists - Consumption of water daily)
        if 'CH2O' in df_eng.columns:
            df_eng['Hydration_Score'] = pd.cut(
                df_eng['CH2O'],
                bins=[0, 1, 2, 3],
                labels=['Low', 'Moderate', 'High']
            )
        
        # Meal regularity (if NCP exists - Number of main meals)
        if 'NCP' in df_eng.columns:
            df_eng['Meal_Regularity'] = df_eng['NCP'].apply(
                lambda x: 'Regular' if x == 3 else ('Irregular_Low' if x < 3 else 'Irregular_High')
            )
        
        print("✓ Feature engineering completed")
        return df_eng
    
    def encode_categorical_variables(self, df, target_column='NObeyesdad', fit=True):
        """
        Encode categorical variables using Label Encoding.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        target_column : str
            Name of the target column
        fit : bool
            Whether to fit the encoders (True for training, False for prediction)
            
        Returns:
        --------
        pd.DataFrame : Dataframe with encoded categorical variables
        """
        df_encoded = df.copy()
        
        # Identify categorical columns (excluding target)
        categorical_cols = df_encoded.select_dtypes(include=['object', 'category']).columns
        categorical_cols = [col for col in categorical_cols if col != target_column]
        
        if fit:
            # Fit and transform
            for col in categorical_cols:
                self.label_encoders[col] = LabelEncoder()
                df_encoded[col] = self.label_encoders[col].fit_transform(df_encoded[col].astype(str))
            
            # Encode target variable
            if target_column in df_encoded.columns:
                df_encoded[target_column] = self.target_encoder.fit_transform(df_encoded[target_column])
            
            print(f"✓ Encoded {len(categorical_cols)} categorical features")
        else:
            # Transform only (for new data) - handle unseen labels gracefully
            for col in categorical_cols:
                if col in self.label_encoders:
                    # Get known classes
                    known_classes = set(self.label_encoders[col].classes_)
                    
                    # For each value, check if it's known, otherwise map to first known class
                    encoded_values = []
                    for val in df_encoded[col].astype(str):
                        if val in known_classes:
                            encoded_values.append(self.label_encoders[col].transform([val])[0])
                        else:
                            # Map unseen label to the first known class (default)
                            print(f"⚠ Warning: Unseen label '{val}' in column '{col}'. Using default encoding.")
                            encoded_values.append(0)  # Default to first class
                    
                    df_encoded[col] = encoded_values
        
        return df_encoded
    
    def scale_features(self, X, fit=True):
        """
        Scale numerical features using StandardScaler.
        
        Parameters:
        -----------
        X : pd.DataFrame or np.array
            Feature matrix
        fit : bool
            Whether to fit the scaler (True for training, False for prediction)
            
        Returns:
        --------
        np.array : Scaled feature matrix
        """
        if fit:
            X_scaled = self.scaler.fit_transform(X)
            print("✓ Features scaled using StandardScaler")
        else:
            X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def prepare_data(self, df, target_column='NObeyesdad', test_size=0.2, random_state=42):
        """
        Complete preprocessing pipeline: from raw data to train-test split.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Raw input dataframe
        target_column : str
            Name of the target column
        test_size : float
            Proportion of data for testing
        random_state : int
            Random seed for reproducibility
            
        Returns:
        --------
        tuple : (X_train, X_test, y_train, y_test)
        """
        print("\n" + "="*60)
        print("STARTING DATA PREPROCESSING PIPELINE")
        print("="*60 + "\n")
        
        # Step 1: Handle missing values
        df_clean = self.handle_missing_values(df)
        
        # Step 2: Calculate BMI
        df_bmi = self.calculate_bmi(df_clean)
        
        # Step 3: Feature engineering
        df_engineered = self.engineer_features(df_bmi)
        
        # Step 4: Encode categorical variables
        df_encoded = self.encode_categorical_variables(df_engineered, target_column, fit=True)
        
        # Step 5: Separate features and target
        if target_column in df_encoded.columns:
            X = df_encoded.drop(columns=[target_column])
            y = df_encoded[target_column]
        else:
            raise ValueError(f"Target column '{target_column}' not found in dataset")
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Step 6: Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"\n✓ Train-test split: {len(X_train)} training samples, {len(X_test)} test samples")
        
        # Step 7: Scale features
        X_train_scaled = self.scale_features(X_train, fit=True)
        X_test_scaled = self.scale_features(X_test, fit=False)
        
        print("\n" + "="*60)
        print("PREPROCESSING COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def preprocess_single_sample(self, sample_dict):
        """
        Preprocess a single sample for prediction.
        
        Parameters:
        -----------
        sample_dict : dict
            Dictionary containing feature values
            
        Returns:
        --------
        np.array : Preprocessed feature vector
        """
        # Convert to DataFrame
        df = pd.DataFrame([sample_dict])
        
        # Calculate BMI
        df = self.calculate_bmi(df)
        
        # Feature engineering
        df = self.engineer_features(df)
        
        # Encode categorical variables
        df = self.encode_categorical_variables(df, target_column=None, fit=False)
        
        # Ensure all expected features are present
        for feature in self.feature_names:
            if feature not in df.columns:
                df[feature] = 0
        
        # Select only the features used during training
        df = df[self.feature_names]
        
        # Scale features
        X_scaled = self.scale_features(df, fit=False)
        
        return X_scaled


# Example usage and testing
if __name__ == "__main__":
    print("Data Preprocessing Module - Test Mode\n")
    
    # Create sample data for testing
    sample_data = {
        'Age': [25, 30, 45, 22, 35],
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'Height': [1.75, 1.62, 1.80, 1.58, 1.70],
        'Weight': [85, 65, 95, 55, 78],
        'family_history_with_overweight': ['yes', 'no', 'yes', 'no', 'yes'],
        'FAVC': ['yes', 'no', 'yes', 'no', 'yes'],
        'FCVC': [2.5, 3.0, 2.0, 3.0, 2.5],
        'NCP': [3, 3, 4, 3, 2],
        'CAEC': ['Sometimes', 'no', 'Frequently', 'Sometimes', 'Sometimes'],
        'SMOKE': ['no', 'no', 'no', 'no', 'yes'],
        'CH2O': [2.0, 2.5, 1.5, 3.0, 2.0],
        'SCC': ['no', 'yes', 'no', 'yes', 'no'],
        'FAF': [2, 3, 1, 3, 2],
        'TUE': [1, 0, 2, 1, 1],
        'CALC': ['Sometimes', 'no', 'Frequently', 'no', 'Sometimes'],
        'MTRANS': ['Public_Transportation', 'Walking', 'Automobile', 'Public_Transportation', 'Automobile'],
        'NObeyesdad': ['Overweight_Level_I', 'Normal_Weight', 'Obesity_Type_I', 'Normal_Weight', 'Overweight_Level_II']
    }
    
    df_sample = pd.DataFrame(sample_data)
    
    # Initialize preprocessor
    preprocessor = ObesityDataPreprocessor()
    
    # Test preprocessing pipeline
    try:
        X_train, X_test, y_train, y_test = preprocessor.prepare_data(df_sample)
        print(f"Training set shape: {X_train.shape}")
        print(f"Test set shape: {X_test.shape}")
        print("\n✓ Preprocessing test completed successfully!")
    except Exception as e:
        print(f"✗ Error during preprocessing: {str(e)}")
