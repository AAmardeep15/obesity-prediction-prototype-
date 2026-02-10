// JavaScript for Obesity Prediction Web Application

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading spinner
        document.getElementById('loadingSpinner').style.display = 'block';
        document.getElementById('resultsSection').style.display = 'none';
        
        // Scroll to loading spinner
        document.getElementById('loadingSpinner').scrollIntoView({ behavior: 'smooth' });
        
        // Get form data
        const formData = new FormData(form);
        
        try {
            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayResults(data);
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('An error occurred: ' + error.message);
        } finally {
            // Hide loading spinner
            document.getElementById('loadingSpinner').style.display = 'none';
        }
    });
});

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    
    // Display prediction results
    const riskLevel = document.getElementById('riskLevel');
    riskLevel.textContent = data.prediction.risk_level.replace(/_/g, ' ');
    
    // Set risk level color
    if (data.prediction.risk_level.includes('Normal') || data.prediction.risk_level.includes('Insufficient')) {
        riskLevel.className = 'risk-level risk-normal';
    } else if (data.prediction.risk_level.includes('Overweight')) {
        riskLevel.className = 'risk-level risk-overweight';
    } else {
        riskLevel.className = 'risk-level risk-obese';
    }
    
    document.getElementById('bmiValue').textContent = data.prediction.bmi;
    document.getElementById('confidenceValue').textContent = data.prediction.confidence + '%';
    document.getElementById('riskDescription').textContent = data.prediction.description;
    
    // Display nutrition recommendations
    document.getElementById('calorieRange').textContent = 
        data.nutrition.calorie_min + ' - ' + data.nutrition.calorie_max + ' kcal/day';
    document.getElementById('nutritionGoal').textContent = 'Goal: ' + data.nutrition.goal;
    
    // Display meal plan
    displayMealItems('breakfastItems', data.nutrition.meal_plan.breakfast);
    displayMealItems('lunchItems', data.nutrition.meal_plan.lunch);
    displayMealItems('dinnerItems', data.nutrition.meal_plan.dinner);
    displayMealItems('snackItems', data.nutrition.meal_plan.snacks);
    
    // Display lifestyle tips
    const tipsContainer = document.getElementById('lifestyleTips');
    tipsContainer.innerHTML = '';
    data.nutrition.lifestyle_tips.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        tipsContainer.appendChild(li);
    });
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayMealItems(containerId, items) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    let totalCalories = 0;
    items.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${item.name}</span>
            <span><strong>${item.calories} kcal</strong></span>
        `;
        container.appendChild(li);
        totalCalories += item.calories;
    });
    
    // Add total
    const totalLi = document.createElement('li');
    totalLi.innerHTML = `
        <span><strong>Total</strong></span>
        <span><strong>${totalCalories} kcal</strong></span>
    `;
    totalLi.style.borderTop = '2px solid #2563eb';
    totalLi.style.marginTop = '8px';
    totalLi.style.paddingTop = '8px';
    container.appendChild(totalLi);
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('resultsSection').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
