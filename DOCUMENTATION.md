# Project Documentation
# Personalized Obesity Risk Prediction and Nutrition Recommendation System

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Module Descriptions](#module-descriptions)
3. [Machine Learning Pipeline](#machine-learning-pipeline)
4. [Feature Engineering](#feature-engineering)
5. [Model Details](#model-details)
6. [Evaluation Metrics](#evaluation-metrics)
7. [Nutrition Recommendation Engine](#nutrition-recommendation-engine)
8. [API Reference](#api-reference)
9. [Future Enhancements](#future-enhancements)

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     INPUT LAYER                              │
│  Patient Data (Demographics, Lifestyle, Eating Habits)      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              DATA PREPROCESSING                              │
│  • Missing Value Handling                                    │
│  • BMI Calculation                                           │
│  • Feature Engineering (Age Groups, Activity Levels)         │
│  • Categorical Encoding                                      │
│  • Feature Scaling (StandardScaler)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              ENSEMBLE MODEL                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Logistic    │  │   Random     │  │  Gradient    │      │
│  │  Regression  │  │   Forest     │  │  Boosting    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                 │
│                   ┌────────▼────────┐                        │
│                   │ Voting Ensemble │                        │
│                   └────────┬────────┘                        │
└────────────────────────────┼────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                  PREDICTION OUTPUT                           │
│  • Obesity Risk Level                                        │
│  • Confidence Score                                          │
│  • BMI Value                                                 │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│          NUTRITION RECOMMENDATION ENGINE                     │
│  • Calorie Recommendations                                   │
│  • Personalized Meal Plans                                   │
│  • Lifestyle Modification Tips                               │
│  • Food Suggestions with Nutritional Values                  │
└─────────────────────────────────────────────────────────────┘
```

## Module Descriptions

### 1. data_preprocessing.py
**Purpose**: Complete data preprocessing pipeline

**Key Features**:
- Missing value imputation (median for numerical, mode for categorical)
- BMI calculation from height and weight
- Feature engineering (age groups, activity levels, hydration scores)
- Label encoding for categorical variables
- Standard scaling for numerical features
- Train-test splitting with stratification

**Main Class**: `ObesityDataPreprocessor`

### 2. model_training.py
**Purpose**: Train individual and ensemble ML models

**Key Features**:
- Three base models with optimized hyperparameters
- Soft voting ensemble for improved accuracy
- Cross-validation for robust evaluation
- Model persistence (save/load functionality)
- Training history tracking

**Main Class**: `ObesityModelTrainer`

### 3. evaluation.py
**Purpose**: Comprehensive model evaluation

**Key Features**:
- Multiple metrics (Accuracy, Precision, Recall, F1-Score)
- Confusion matrix visualization
- Model comparison charts
- Classification reports
- Performance summaries

**Main Class**: `ModelEvaluator`

### 4. prediction.py
**Purpose**: Make predictions on new patient data

**Key Features**:
- Single patient prediction
- Batch prediction support
- Confidence scores
- Risk level descriptions

**Main Class**: `ObesityPredictor`

### 5. nutrition_recommendation.py
**Purpose**: Generate personalized nutrition plans

**Key Features**:
- Calorie recommendations based on risk level
- Sample meal plans (breakfast, lunch, dinner, snacks)
- Food database with nutritional values
- Lifestyle modification tips
- Gender and activity level adjustments

**Main Class**: `NutritionRecommender`

## Machine Learning Pipeline

### Step 1: Data Collection
- Demographics: Age, Gender, Height, Weight
- Family history of overweight
- Eating habits: High caloric food, vegetables, water intake
- Physical activity frequency
- Technology usage time
- Transportation method

### Step 2: Preprocessing
1. **Missing Values**: Imputed using median/mode
2. **BMI Calculation**: Weight / (Height²)
3. **Feature Engineering**:
   - Age groups (Teen, Young Adult, Adult, Middle Aged, Senior)
   - Activity levels (Sedentary, Low, Moderate, High)
   - Hydration scores (Low, Moderate, High)
   - Meal regularity indicators

4. **Encoding**: Label encoding for categorical variables
5. **Scaling**: StandardScaler for numerical features

### Step 3: Model Training
Three models trained independently:
1. **Logistic Regression**: Baseline linear classifier
2. **Random Forest**: 100 trees, max_depth=15
3. **Gradient Boosting**: 100 estimators, learning_rate=0.1

### Step 4: Ensemble Creation
- **Voting Classifier** with soft voting
- Combines predictions from all three models
- Weighted average of probability estimates

### Step 5: Evaluation
- 5-fold cross-validation
- Test set evaluation
- Confusion matrix analysis
- Feature importance extraction

## Feature Engineering

### Engineered Features

1. **BMI (Body Mass Index)**
   - Formula: Weight (kg) / Height² (m²)
   - Categories: Underweight, Normal, Overweight, Obese

2. **Age_Group**
   - Teen (0-18)
   - Young Adult (18-30)
   - Adult (30-45)
   - Middle Aged (45-60)
   - Senior (60+)

3. **Activity_Level**
   - Based on FAF (Frequency of physical Activity)
   - Sedentary (0)
   - Low (1)
   - Moderate (2)
   - High (3-4)

4. **Hydration_Score**
   - Based on CH2O (water consumption)
   - Low (0-1 liters)
   - Moderate (1-2 liters)
   - High (2-3 liters)

5. **Meal_Regularity**
   - Based on NCP (Number of main meals)
   - Regular (3 meals)
   - Irregular_Low (<3 meals)
   - Irregular_High (>3 meals)

## Model Details

### Logistic Regression
- **Type**: Linear classifier
- **Advantages**: Fast, interpretable, probability estimates
- **Parameters**:
  - max_iter: 1000
  - solver: lbfgs
  - multi_class: multinomial
  - class_weight: balanced

### Random Forest
- **Type**: Ensemble of decision trees
- **Advantages**: Handles non-linearity, feature importance, robust
- **Parameters**:
  - n_estimators: 100
  - max_depth: 15
  - min_samples_split: 5
  - class_weight: balanced

### Gradient Boosting
- **Type**: Sequential ensemble
- **Advantages**: High accuracy, error correction
- **Parameters**:
  - n_estimators: 100
  - learning_rate: 0.1
  - max_depth: 5
  - subsample: 0.8

### Voting Ensemble
- **Strategy**: Soft voting
- **Combines**: All three models
- **Advantage**: Reduces overfitting, improves generalization

## Evaluation Metrics

### Accuracy
Proportion of correct predictions
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

### Precision
Proportion of positive predictions that are correct
```
Precision = TP / (TP + FP)
```

### Recall (Sensitivity)
Proportion of actual positives correctly identified
```
Recall = TP / (TP + FN)
```

### F1-Score
Harmonic mean of precision and recall
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

### Confusion Matrix
Visual representation of prediction accuracy across all classes

## Nutrition Recommendation Engine

### Calorie Recommendations

| Risk Level | Daily Calories | Goal |
|-----------|---------------|------|
| Insufficient Weight | 2500-3000 | Weight Gain |
| Normal Weight | 2000-2500 | Maintenance |
| Overweight Level I | 1800-2200 | Moderate Loss |
| Overweight Level II | 1600-2000 | Weight Loss |
| Obesity Type I | 1500-1800 | Significant Loss |
| Obesity Type II | 1400-1700 | Major Loss |
| Obesity Type III | 1200-1500 | Intensive Loss |

### Meal Distribution
- Breakfast: 25% of daily calories
- Lunch: 35% of daily calories
- Dinner: 30% of daily calories
- Snacks: 10% of daily calories

### Food Database
Contains 20+ healthy foods with:
- Calories
- Protein content
- Carbohydrates
- Fats
- Fiber

## API Reference

### Making Predictions

```python
from src.prediction import predict_obesity_risk

patient_data = {
    'Age': 30,
    'Gender': 'Male',
    'Height': 1.75,
    'Weight': 85,
    # ... other features
}

result = predict_obesity_risk(patient_data)
print(result['risk_level'])
print(result['confidence'])
```

### Getting Nutrition Plan

```python
from src.nutrition_recommendation import get_nutrition_plan

nutrition_plan = get_nutrition_plan(risk_level, patient_data)
print(nutrition_plan['calorie_recommendation'])
print(nutrition_plan['daily_meal_plan'])
```

## Future Enhancements

### Web Application
- Flask/Django REST API
- React/Vue.js frontend
- User authentication
- Patient history tracking

### Advanced Features
- Deep learning models (Neural Networks)
- Real-time fitness tracker integration
- Personalized exercise recommendations
- Multi-language support
- Mobile application

### Clinical Integration
- Electronic Health Record (EHR) integration
- Doctor dashboard
- Progress tracking and analytics
- Automated report generation

### Research Extensions
- Genetic factors incorporation
- Medication interaction analysis
- Comorbidity risk assessment
- Long-term outcome prediction

## UN SDG 3 Contribution

This project directly supports:
- **Target 3.4**: Reduce premature mortality from NCDs
- **Target 3.d**: Strengthen early warning and risk reduction

By providing accessible obesity risk assessment and personalized recommendations, this system empowers individuals to make informed health decisions and take preventive action.

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**License**: Academic Project
