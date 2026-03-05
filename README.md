# Personalized Obesity Risk Prediction and Nutrition Recommendation System

## Project Overview
This project implements an ensemble machine learning system for obesity risk prediction and personalized nutrition recommendations, aligned with **UN Sustainable Development Goal 3: Good Health and Well-Being**.

## Features
- **Multi-Model Ensemble Learning**: Combines Logistic Regression, Random Forest, and Gradient Boosting
- **Comprehensive Data Preprocessing**: Missing value handling, encoding, scaling, and feature engineering
- **Advanced Evaluation Metrics**: Accuracy, Precision, Recall, F1-Score, and Confusion Matrix
- **Personalized Nutrition Recommendations**: Calorie-based meal suggestions based on obesity risk
- **Modular Architecture**: Clean, extensible code structure for web application integration

## Project Structure
```
mini_project/
├── data/
│   └── obesity_data.csv          # Dataset (to be added)
├── src/
│   ├── data_preprocessing.py     # Data cleaning and feature engineering
│   ├── model_training.py         # ML model training and ensemble creation
│   ├── evaluation.py             # Model evaluation and metrics
│   ├── prediction.py             # Prediction pipeline
│   └── nutrition_recommendation.py # Nutrition recommendation engine
├── models/
│   └── (saved models will be stored here)
├── outputs/
│   └── (evaluation results and visualizations)
├── main.py                       # Main application entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Installation

1. Clone or navigate to the project directory
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dataset Requirements
The obesity dataset should contain the following features:
- **Demographic**: Age, Gender, Height, Weight
- **Physical**: Physical Activity Frequency (FAF), Time Using Technology (TUE)
- **Lifestyle**: Family History with Overweight (family_history_with_overweight), Smoking (SMOKE), Alcohol Consumption (CALC)
- **Eating Habits**: Frequent Consumption of High Caloric Food (FAVC), Frequency of Consumption of Vegetables (FCVC), Number of Main Meals (NCP), Consumption of Food Between Meals (CAEC), Consumption of Water Daily (CH2O), Calories Consumption Monitoring (SCC), Transportation Used (MTRANS)
- **Target**: NObeyesdad (Obesity Level)

## Usage

### Basic Usage
```python
python main.py
```

### Custom Prediction
```python
from src.prediction import predict_obesity_risk
from src.nutrition_recommendation import get_nutrition_plan

# Example patient data
patient_data = {
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

# Get prediction
risk_level = predict_obesity_risk(patient_data)
print(f"Predicted Obesity Risk: {risk_level}")

# Get nutrition recommendations
nutrition_plan = get_nutrition_plan(risk_level, patient_data)
print(nutrition_plan)
```

## Model Performance
The ensemble model combines three algorithms:
1. **Logistic Regression**: Fast baseline classifier
2. **Random Forest**: Handles non-linear relationships and feature interactions
3. **Gradient Boosting**: Sequential error correction for improved accuracy

## Nutrition Recommendation System
Based on predicted obesity risk, the system provides:
- **Calorie intake recommendations**
- **Meal suggestions** with nutritional breakdown
- **Healthy food alternatives**
- **Lifestyle modification tips**

## UN SDG 3 Alignment
This project contributes to:
- **Target 3.4**: Reduce premature mortality from non-communicable diseases
- **Target 3.d**: Strengthen capacity for early warning and risk reduction

## Future Enhancements
- Web application interface (Flask/Django/Streamlit)
- Real-time prediction API
- Integration with fitness tracking devices
- Personalized exercise recommendations
- Multi-language support

## License
Academic Project - 2026

## Author
Final Year Project - Healthcare AI Research
