"""
Model Training Module
=====================
This module handles:
- Training individual ML models (Logistic Regression, Random Forest, Gradient Boosting)
- Creating ensemble models (Voting Classifier)
- Model persistence (saving and loading)
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import cross_val_score
import joblib
import os
from datetime import datetime


class ObesityModelTrainer:
    """
    Comprehensive model training pipeline for obesity prediction.
    """
    
    def __init__(self, random_state=42):
        """
        Initialize model trainer with base models.
        
        Parameters:
        -----------
        random_state : int
            Random seed for reproducibility
        """
        self.random_state = random_state
        self.models = {}
        self.ensemble_model = None
        self.training_history = {}
        
        # Initialize base models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize individual ML models with optimized hyperparameters."""
        
        # Model 1: Logistic Regression
        # - Fast and interpretable
        # - Good for linearly separable data
        # - Provides probability estimates
        self.models['Logistic_Regression'] = LogisticRegression(
            max_iter=1000,
            random_state=self.random_state,
            solver='lbfgs',
            multi_class='multinomial',
            class_weight='balanced'  # Handle class imbalance
        )
        
        # Model 2: Random Forest
        # - Handles non-linear relationships
        # - Robust to outliers
        # - Provides feature importance
        self.models['Random_Forest'] = RandomForestClassifier(
            n_estimators=100,  # Number of trees
            max_depth=15,      # Prevent overfitting
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=self.random_state,
            class_weight='balanced',
            n_jobs=-1  # Use all CPU cores
        )
        
        # Model 3: Gradient Boosting
        # - Sequential error correction
        # - High accuracy
        # - Handles complex patterns
        self.models['Gradient_Boosting'] = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=self.random_state,
            subsample=0.8  # Stochastic gradient boosting
        )
        
        print("✓ Base models initialized:")
        print("  - Logistic Regression")
        print("  - Random Forest (100 trees)")
        print("  - Gradient Boosting (100 estimators)")
    
    def train_individual_models(self, X_train, y_train, verbose=True):
        """
        Train all individual models.
        
        Parameters:
        -----------
        X_train : np.array
            Training features
        y_train : np.array
            Training labels
        verbose : bool
            Print training progress
            
        Returns:
        --------
        dict : Trained models
        """
        print("\n" + "="*60)
        print("TRAINING INDIVIDUAL MODELS")
        print("="*60 + "\n")
        
        for model_name, model in self.models.items():
            if verbose:
                print(f"Training {model_name}...")
            
            start_time = datetime.now()
            
            # Train the model
            model.fit(X_train, y_train)
            
            # Calculate training time
            training_time = (datetime.now() - start_time).total_seconds()
            
            # Perform cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            
            # Store training history
            self.training_history[model_name] = {
                'training_time': training_time,
                'cv_mean_accuracy': cv_scores.mean(),
                'cv_std_accuracy': cv_scores.std()
            }
            
            if verbose:
                print(f"  ✓ Training completed in {training_time:.2f} seconds")
                print(f"  ✓ Cross-validation accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
                print()
        
        print("="*60)
        print("INDIVIDUAL MODEL TRAINING COMPLETED")
        print("="*60 + "\n")
        
        return self.models
    
    def create_ensemble_model(self, X_train, y_train, voting='soft', verbose=True):
        """
        Create and train an ensemble model using Voting Classifier.
        
        Voting strategies:
        - 'hard': Majority voting (class labels)
        - 'soft': Weighted average of probabilities (recommended)
        
        Parameters:
        -----------
        X_train : np.array
            Training features
        y_train : np.array
            Training labels
        voting : str
            Voting strategy ('hard' or 'soft')
        verbose : bool
            Print training progress
            
        Returns:
        --------
        VotingClassifier : Trained ensemble model
        """
        print("\n" + "="*60)
        print("CREATING ENSEMBLE MODEL")
        print("="*60 + "\n")
        
        # Create voting classifier
        estimators = [
            ('lr', self.models['Logistic_Regression']),
            ('rf', self.models['Random_Forest']),
            ('gb', self.models['Gradient_Boosting'])
        ]
        
        self.ensemble_model = VotingClassifier(
            estimators=estimators,
            voting=voting,
            n_jobs=-1
        )
        
        if verbose:
            print(f"Ensemble strategy: {voting.upper()} voting")
            print("Training ensemble model...")
        
        start_time = datetime.now()
        
        # Train ensemble
        self.ensemble_model.fit(X_train, y_train)
        
        training_time = (datetime.now() - start_time).total_seconds()
        
        # Cross-validation for ensemble
        cv_scores = cross_val_score(self.ensemble_model, X_train, y_train, cv=5, scoring='accuracy')
        
        # Store ensemble training history
        self.training_history['Ensemble'] = {
            'training_time': training_time,
            'cv_mean_accuracy': cv_scores.mean(),
            'cv_std_accuracy': cv_scores.std(),
            'voting_strategy': voting
        }
        
        if verbose:
            print(f"✓ Ensemble training completed in {training_time:.2f} seconds")
            print(f"✓ Cross-validation accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        print("\n" + "="*60)
        print("ENSEMBLE MODEL CREATED SUCCESSFULLY")
        print("="*60 + "\n")
        
        return self.ensemble_model
    
    def get_feature_importance(self, feature_names):
        """
        Extract feature importance from Random Forest model.
        
        Parameters:
        -----------
        feature_names : list
            List of feature names
            
        Returns:
        --------
        pd.DataFrame : Feature importance scores
        """
        if 'Random_Forest' not in self.models:
            print("⚠ Random Forest model not trained yet")
            return None
        
        rf_model = self.models['Random_Forest']
        
        # Get feature importances
        importances = rf_model.feature_importances_
        
        # Create DataFrame
        feature_importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)
        
        return feature_importance_df
    
    def save_models(self, save_dir='models'):
        """
        Save all trained models to disk.
        
        Parameters:
        -----------
        save_dir : str
            Directory to save models
        """
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Save individual models
        for model_name, model in self.models.items():
            model_path = os.path.join(save_dir, f"{model_name.lower()}.pkl")
            joblib.dump(model, model_path)
            print(f"✓ Saved {model_name} to {model_path}")
        
        # Save ensemble model
        if self.ensemble_model is not None:
            ensemble_path = os.path.join(save_dir, "ensemble_model.pkl")
            joblib.dump(self.ensemble_model, ensemble_path)
            print(f"✓ Saved Ensemble Model to {ensemble_path}")
        
        # Save training history
        history_path = os.path.join(save_dir, "training_history.pkl")
        joblib.dump(self.training_history, history_path)
        print(f"✓ Saved training history to {history_path}")
    
    def load_models(self, save_dir='models'):
        """
        Load trained models from disk.
        
        Parameters:
        -----------
        save_dir : str
            Directory containing saved models
        """
        # Load individual models
        for model_name in ['Logistic_Regression', 'Random_Forest', 'Gradient_Boosting']:
            model_path = os.path.join(save_dir, f"{model_name.lower()}.pkl")
            if os.path.exists(model_path):
                self.models[model_name] = joblib.load(model_path)
                print(f"✓ Loaded {model_name} from {model_path}")
        
        # Load ensemble model
        ensemble_path = os.path.join(save_dir, "ensemble_model.pkl")
        if os.path.exists(ensemble_path):
            self.ensemble_model = joblib.load(ensemble_path)
            print(f"✓ Loaded Ensemble Model from {ensemble_path}")
        
        # Load training history
        history_path = os.path.join(save_dir, "training_history.pkl")
        if os.path.exists(history_path):
            self.training_history = joblib.load(history_path)
            print(f"✓ Loaded training history from {history_path}")
    
    def print_training_summary(self):
        """Print a summary of training results."""
        print("\n" + "="*60)
        print("TRAINING SUMMARY")
        print("="*60 + "\n")
        
        for model_name, history in self.training_history.items():
            print(f"{model_name}:")
            print(f"  Training Time: {history['training_time']:.2f} seconds")
            print(f"  CV Accuracy: {history['cv_mean_accuracy']:.4f} (+/- {history['cv_std_accuracy']:.4f})")
            if 'voting_strategy' in history:
                print(f"  Voting Strategy: {history['voting_strategy']}")
            print()
        
        print("="*60 + "\n")


# Example usage and testing
if __name__ == "__main__":
    print("Model Training Module - Test Mode\n")
    
    # Create sample data for testing
    from sklearn.datasets import make_classification
    
    X_train, y_train = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=7,  # Simulating 7 obesity categories
        random_state=42
    )
    
    # Initialize trainer
    trainer = ObesityModelTrainer(random_state=42)
    
    # Train individual models
    trainer.train_individual_models(X_train, y_train)
    
    # Create ensemble model
    trainer.create_ensemble_model(X_train, y_train, voting='soft')
    
    # Print training summary
    trainer.print_training_summary()
    
    print("✓ Model training test completed successfully!")
