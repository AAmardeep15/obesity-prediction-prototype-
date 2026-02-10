"""
Nutrition Recommendation Module
================================
This module provides personalized nutrition recommendations based on obesity risk prediction.
"""

import pandas as pd
import numpy as np


class NutritionRecommender:
    """Personalized nutrition recommendation system."""
    
    def __init__(self):
        """Initialize nutrition database and recommendation rules."""
        self.calorie_recommendations = {
            'Insufficient_Weight': {'min': 2500, 'max': 3000, 'goal': 'Weight Gain'},
            'Normal_Weight': {'min': 2000, 'max': 2500, 'goal': 'Weight Maintenance'},
            'Overweight_Level_I': {'min': 1800, 'max': 2200, 'goal': 'Moderate Weight Loss'},
            'Overweight_Level_II': {'min': 1600, 'max': 2000, 'goal': 'Weight Loss'},
            'Obesity_Type_I': {'min': 1500, 'max': 1800, 'goal': 'Significant Weight Loss'},
            'Obesity_Type_II': {'min': 1400, 'max': 1700, 'goal': 'Major Weight Loss'},
            'Obesity_Type_III': {'min': 1200, 'max': 1500, 'goal': 'Intensive Weight Loss'}
        }
        
        # Healthy food database with nutritional values
        self.food_database = self._create_food_database()
    
    def _create_food_database(self):
        """Create a database of healthy foods with nutritional information."""
        foods = [
            # Proteins
            {'name': 'Grilled Chicken Breast', 'category': 'Protein', 'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0},
            {'name': 'Salmon Fillet', 'category': 'Protein', 'calories': 206, 'protein': 22, 'carbs': 0, 'fat': 13, 'fiber': 0},
            {'name': 'Boiled Eggs (2)', 'category': 'Protein', 'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0},
            {'name': 'Greek Yogurt', 'category': 'Protein', 'calories': 100, 'protein': 17, 'carbs': 6, 'fat': 0.7, 'fiber': 0},
            {'name': 'Lentils (cooked)', 'category': 'Protein', 'calories': 230, 'protein': 18, 'carbs': 40, 'fat': 0.8, 'fiber': 16},
            
            # Vegetables
            {'name': 'Broccoli (steamed)', 'category': 'Vegetable', 'calories': 55, 'protein': 3.7, 'carbs': 11, 'fat': 0.6, 'fiber': 5},
            {'name': 'Spinach Salad', 'category': 'Vegetable', 'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2},
            {'name': 'Mixed Vegetables', 'category': 'Vegetable', 'calories': 65, 'protein': 2.5, 'carbs': 13, 'fat': 0.3, 'fiber': 4},
            {'name': 'Cucumber Salad', 'category': 'Vegetable', 'calories': 16, 'protein': 0.7, 'carbs': 3.6, 'fat': 0.1, 'fiber': 0.5},
            
            # Carbohydrates
            {'name': 'Brown Rice', 'category': 'Carbohydrate', 'calories': 215, 'protein': 5, 'carbs': 45, 'fat': 1.8, 'fiber': 3.5},
            {'name': 'Quinoa', 'category': 'Carbohydrate', 'calories': 222, 'protein': 8, 'carbs': 39, 'fat': 3.6, 'fiber': 5},
            {'name': 'Sweet Potato', 'category': 'Carbohydrate', 'calories': 180, 'protein': 4, 'carbs': 41, 'fat': 0.3, 'fiber': 6.6},
            {'name': 'Oatmeal', 'category': 'Carbohydrate', 'calories': 150, 'protein': 5, 'carbs': 27, 'fat': 3, 'fiber': 4},
            
            # Fruits
            {'name': 'Apple', 'category': 'Fruit', 'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'fiber': 4.4},
            {'name': 'Banana', 'category': 'Fruit', 'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4, 'fiber': 3.1},
            {'name': 'Berries Mix', 'category': 'Fruit', 'calories': 70, 'protein': 1, 'carbs': 17, 'fat': 0.5, 'fiber': 4},
            {'name': 'Orange', 'category': 'Fruit', 'calories': 62, 'protein': 1.2, 'carbs': 15, 'fat': 0.2, 'fiber': 3.1},
            
            # Healthy Fats
            {'name': 'Avocado (half)', 'category': 'Healthy Fat', 'calories': 120, 'protein': 1.5, 'carbs': 6, 'fat': 11, 'fiber': 5},
            {'name': 'Almonds (handful)', 'category': 'Healthy Fat', 'calories': 164, 'protein': 6, 'carbs': 6, 'fat': 14, 'fiber': 3.5},
            {'name': 'Olive Oil (1 tbsp)', 'category': 'Healthy Fat', 'calories': 119, 'protein': 0, 'carbs': 0, 'fat': 13.5, 'fiber': 0}
        ]
        
        return pd.DataFrame(foods)
    
    def get_calorie_recommendation(self, risk_level, patient_data=None):
        """
        Get personalized calorie recommendation based on obesity risk.
        
        Parameters:
        -----------
        risk_level : str
            Predicted obesity risk level
        patient_data : dict
            Additional patient information (age, gender, activity level)
            
        Returns:
        --------
        dict : Calorie recommendations
        """
        base_rec = self.calorie_recommendations.get(risk_level, self.calorie_recommendations['Normal_Weight'])
        
        # Adjust for gender and activity level if provided
        if patient_data:
            adjustment = 0
            
            # Gender adjustment
            if patient_data.get('Gender') == 'Male':
                adjustment += 200
            
            # Activity level adjustment
            faf = patient_data.get('FAF', 0)
            if faf >= 3:
                adjustment += 200
            elif faf >= 1:
                adjustment += 100
            
            base_rec = {
                'min': base_rec['min'] + adjustment,
                'max': base_rec['max'] + adjustment,
                'goal': base_rec['goal']
            }
        
        return base_rec
    
    def create_meal_plan(self, risk_level, patient_data=None):
        """
        Create a sample daily meal plan based on obesity risk.
        
        Parameters:
        -----------
        risk_level : str
            Predicted obesity risk level
        patient_data : dict
            Patient information
            
        Returns:
        --------
        dict : Meal plan with breakfast, lunch, dinner, and snacks
        """
        calorie_rec = self.get_calorie_recommendation(risk_level, patient_data)
        target_calories = (calorie_rec['min'] + calorie_rec['max']) / 2
        
        # Meal distribution: Breakfast 25%, Lunch 35%, Dinner 30%, Snacks 10%
        meal_plan = {
            'breakfast': self._suggest_meal('breakfast', target_calories * 0.25),
            'lunch': self._suggest_meal('lunch', target_calories * 0.35),
            'dinner': self._suggest_meal('dinner', target_calories * 0.30),
            'snacks': self._suggest_meal('snacks', target_calories * 0.10)
        }
        
        return meal_plan
    
    def _suggest_meal(self, meal_type, target_calories):
        """Suggest foods for a specific meal type."""
        suggestions = []
        
        if meal_type == 'breakfast':
            # Balanced breakfast
            suggestions.append(self.food_database[self.food_database['name'] == 'Oatmeal'].iloc[0].to_dict())
            suggestions.append(self.food_database[self.food_database['name'] == 'Boiled Eggs (2)'].iloc[0].to_dict())
            suggestions.append(self.food_database[self.food_database['name'] == 'Banana'].iloc[0].to_dict())
        
        elif meal_type == 'lunch':
            # Protein-rich lunch
            suggestions.append(self.food_database[self.food_database['name'] == 'Grilled Chicken Breast'].iloc[0].to_dict())
            suggestions.append(self.food_database[self.food_database['name'] == 'Brown Rice'].iloc[0].to_dict())
            suggestions.append(self.food_database[self.food_database['name'] == 'Broccoli (steamed)'].iloc[0].to_dict())
            suggestions.append(self.food_database[self.food_database['name'] == 'Mixed Vegetables'].iloc[0].to_dict())
        
        elif meal_type == 'dinner':
            # Light dinner
            suggestions.append(self.food_database[self.food_database['name'] == 'Salmon Fillet'].iloc[0].to_dict())
            suggestions.append(self.food_database[self.food_database['name'] == 'Quinoa'].iloc[0].to_dict())
            suggestions.append(self.food_database[self.food_database['name'] == 'Spinach Salad'].iloc[0].to_dict())
        
        else:  # snacks
            suggestions.append(self.food_database[self.food_database['name'] == 'Greek Yogurt'].iloc[0].to_dict())
            suggestions.append(self.food_database[self.food_database['name'] == 'Apple'].iloc[0].to_dict())
        
        total_calories = sum(item['calories'] for item in suggestions)
        
        return {
            'items': suggestions,
            'total_calories': total_calories,
            'target_calories': target_calories
        }
    
    def get_lifestyle_recommendations(self, risk_level, patient_data=None):
        """Get lifestyle modification recommendations."""
        recommendations = {
            'Insufficient_Weight': [
                'Increase calorie intake with nutrient-dense foods',
                'Include healthy fats and proteins in every meal',
                'Eat frequent small meals (5-6 times daily)',
                'Strength training to build muscle mass',
                'Consult a nutritionist for personalized guidance'
            ],
            'Normal_Weight': [
                'Maintain balanced diet with variety of nutrients',
                'Regular physical activity (150 min/week)',
                'Stay hydrated (8-10 glasses of water daily)',
                'Get adequate sleep (7-9 hours)',
                'Monitor weight regularly'
            ],
            'Overweight_Level_I': [
                'Reduce portion sizes gradually',
                'Increase vegetable and fruit intake',
                'Limit processed foods and sugary drinks',
                'Exercise 30-45 minutes daily',
                'Track food intake and calories'
            ],
            'Overweight_Level_II': [
                'Create a structured meal plan',
                'Eliminate high-calorie snacks',
                'Increase physical activity to 45-60 minutes daily',
                'Consider consulting a dietitian',
                'Join a support group or fitness program'
            ],
            'Obesity_Type_I': [
                'Seek medical supervision for weight loss',
                'Follow a medically supervised diet plan',
                'Engage in regular moderate exercise',
                'Monitor blood pressure and blood sugar',
                'Consider behavioral therapy for eating habits'
            ],
            'Obesity_Type_II': [
                'Immediate medical consultation required',
                'Comprehensive weight management program',
                'Supervised exercise regimen',
                'Regular health monitoring',
                'Possible medication or surgical options'
            ],
            'Obesity_Type_III': [
                'Urgent medical intervention needed',
                'Multidisciplinary treatment approach',
                'Bariatric surgery evaluation',
                'Intensive lifestyle modification program',
                'Regular medical monitoring and support'
            ]
        }
        
        return recommendations.get(risk_level, recommendations['Normal_Weight'])
    
    def generate_nutrition_report(self, risk_level, patient_data=None):
        """Generate comprehensive nutrition recommendation report."""
        calorie_rec = self.get_calorie_recommendation(risk_level, patient_data)
        meal_plan = self.create_meal_plan(risk_level, patient_data)
        lifestyle_tips = self.get_lifestyle_recommendations(risk_level, patient_data)
        
        report = {
            'risk_level': risk_level,
            'calorie_recommendation': calorie_rec,
            'daily_meal_plan': meal_plan,
            'lifestyle_recommendations': lifestyle_tips,
            'bmi': patient_data.get('BMI') if patient_data else None
        }
        
        return report


def get_nutrition_plan(risk_level, patient_data=None):
    """
    Convenience function to get nutrition recommendations.
    
    Parameters:
    -----------
    risk_level : str
        Predicted obesity risk level
    patient_data : dict
        Patient information
        
    Returns:
    --------
    dict : Comprehensive nutrition plan
    """
    recommender = NutritionRecommender()
    return recommender.generate_nutrition_report(risk_level, patient_data)


# Example usage
if __name__ == "__main__":
    print("Nutrition Recommendation Module - Test Mode\n")
    
    recommender = NutritionRecommender()
    
    # Test for different risk levels
    test_patient = {
        'Gender': 'Male',
        'Age': 30,
        'FAF': 2,
        'BMI': 28.5
    }
    
    risk_level = 'Overweight_Level_I'
    
    print(f"Generating nutrition plan for: {risk_level}\n")
    
    report = recommender.generate_nutrition_report(risk_level, test_patient)
    
    print(f"Calorie Recommendation: {report['calorie_recommendation']['min']}-{report['calorie_recommendation']['max']} kcal/day")
    print(f"Goal: {report['calorie_recommendation']['goal']}\n")
    
    print("Sample Breakfast:")
    for item in report['daily_meal_plan']['breakfast']['items']:
        print(f"  - {item['name']}: {item['calories']} kcal")
    
    print("\n✓ Nutrition recommendation module loaded successfully!")
