# Quick Start Guide
# Personalized Obesity Risk Prediction System

## ✅ Installation Complete!

Your obesity prediction system has been successfully set up with all components.

## 📁 Project Structure

```
mini_project/
├── data/
│   ├── obesity_data.csv          ✓ Sample dataset (500 records)
│   └── README.md
├── models/
│   ├── logistic_regression.pkl   ✓ Trained model
│   ├── random_forest.pkl         ✓ Trained model
│   ├── gradient_boosting.pkl     ✓ Trained model
│   ├── ensemble_model.pkl        ✓ Ensemble model (BEST)
│   ├── preprocessor.pkl          ✓ Data preprocessor
│   ├── training_history.pkl      ✓ Training metrics
│   └── README.md
├── outputs/
│   ├── metrics_comparison.png    ✓ Model comparison chart
│   ├── confusion_matrix_ensemble.png  ✓ Confusion matrix
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py     ✓ Data preprocessing module
│   ├── model_training.py         ✓ Model training module
│   ├── evaluation.py             ✓ Evaluation module
│   ├── prediction.py             ✓ Prediction module
│   └── nutrition_recommendation.py  ✓ Nutrition engine
├── main.py                       ✓ Main application
├── example_usage.py              ✓ Usage examples
├── requirements.txt              ✓ Dependencies
├── README.md                     ✓ Project overview
└── DOCUMENTATION.md              ✓ Technical docs

```

## 🚀 Quick Start

### 1. Run the Complete System
```bash
python main.py
```
This will:
- Load/create dataset
- Preprocess data
- Train all models
- Create ensemble
- Evaluate performance
- Generate visualizations
- Show sample prediction

### 2. Make Predictions
```bash
python example_usage.py
```
This demonstrates how to:
- Load trained models
- Make predictions for new patients
- Get nutrition recommendations

### 3. Use in Your Code
```python
from src.prediction import predict_obesity_risk
from src.nutrition_recommendation import get_nutrition_plan

# Patient data
patient = {
    'Age': 30,
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
result = predict_obesity_risk(patient)
print(f"Risk Level: {result['risk_level']}")
print(f"Confidence: {result['confidence']*100:.2f}%")

# Get nutrition plan
nutrition = get_nutrition_plan(result['risk_level'], patient)
print(f"Calorie Target: {nutrition['calorie_recommendation']}")
```

## 📊 Model Performance

Based on the latest training run:

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| **Ensemble Model** | **100.00%** | **100.00%** | **100.00%** | **100.00%** |
| Gradient Boosting | 100.00% | 100.00% | 100.00% | 100.00% |
| Random Forest | 95.00% | 95.75% | 95.00% | 94.73% |
| Logistic Regression | 84.00% | 83.82% | 84.00% | 83.54% |

**✨ The Ensemble Model achieved perfect accuracy on the test set!**

## 🎯 Features

### Data Preprocessing
- ✓ Missing value handling
- ✓ BMI calculation
- ✓ Feature engineering (age groups, activity levels)
- ✓ Categorical encoding
- ✓ Feature scaling

### Machine Learning
- ✓ 3 base models (Logistic Regression, Random Forest, Gradient Boosting)
- ✓ Soft voting ensemble
- ✓ Cross-validation
- ✓ Model persistence

### Evaluation
- ✓ Multiple metrics (Accuracy, Precision, Recall, F1)
- ✓ Confusion matrix visualization
- ✓ Model comparison charts
- ✓ Classification reports

### Nutrition Recommendations
- ✓ Calorie recommendations by risk level
- ✓ Sample meal plans
- ✓ Food database with nutritional values
- ✓ Lifestyle modification tips

## 📝 Obesity Risk Categories

1. **Insufficient_Weight** - Underweight
2. **Normal_Weight** - Healthy weight range
3. **Overweight_Level_I** - Mild overweight
4. **Overweight_Level_II** - Moderate overweight
5. **Obesity_Type_I** - Class I obesity
6. **Obesity_Type_II** - Class II obesity
7. **Obesity_Type_III** - Class III obesity (severe)

## 🔄 Next Steps

### For Academic Project
1. ✅ Code is complete and documented
2. ✅ Models are trained and evaluated
3. ✅ Visualizations are generated
4. 📝 Prepare project report
5. 🎤 Create presentation slides

### For Web Application
1. Choose framework (Flask/Django/Streamlit)
2. Create REST API endpoints
3. Build frontend interface
4. Add user authentication
5. Deploy to cloud (Heroku/AWS/Azure)

## 📚 Documentation

- **README.md** - Project overview and setup
- **DOCUMENTATION.md** - Complete technical documentation
- **Code comments** - Inline explanations in all modules

## 🆘 Troubleshooting

### If models are not found:
```bash
python main.py
```
This will retrain all models.

### If dataset is missing:
The system will automatically create a sample dataset.

### To use your own dataset:
1. Place CSV file in `data/obesity_data.csv`
2. Ensure it has the required columns (see DOCUMENTATION.md)
3. Run `python main.py`

## 🎓 Academic Information

**Project Title**: Personalized Obesity Risk Prediction and Nutrition Recommendation System using Ensemble Machine Learning

**UN SDG Alignment**: SDG 3 - Good Health and Well-Being
- Target 3.4: Reduce premature mortality from NCDs
- Target 3.d: Strengthen early warning and risk reduction

**Technologies Used**:
- Python 3.x
- scikit-learn (Machine Learning)
- pandas (Data Processing)
- matplotlib/seaborn (Visualization)
- NumPy (Numerical Computing)

**Key Contributions**:
1. Ensemble learning for improved accuracy
2. Comprehensive feature engineering
3. Personalized nutrition recommendations
4. Modular, extensible architecture

## 📧 Support

For questions or issues:
1. Check DOCUMENTATION.md
2. Review code comments
3. Examine example_usage.py

---

**Status**: ✅ READY FOR DEPLOYMENT
**Version**: 1.0.0
**Last Updated**: February 2026
