# Web Application Guide

## 🌐 Running the Web Application

### 1. Install Flask (if not already installed)
```bash
pip install flask
```

### 2. Start the Web Server
```bash
python app.py
```

### 3. Open Your Browser
Navigate to: **http://127.0.0.1:5000**

---

## 📱 Using the Web Application

### Step 1: Fill in Patient Information
The form is organized into sections:
- **Personal Details**: Age, Gender, Height, Weight
- **Family History & Lifestyle**: Family history, smoking habits
- **Eating Habits**: Food consumption patterns
- **Physical Activity**: Exercise frequency, transportation

### Step 2: Submit for Analysis
Click the **"🔍 Analyze Health Risk"** button

### Step 3: View Results
You'll see:
- **Obesity Risk Level** with confidence score
- **BMI Calculation**
- **Personalized Nutrition Plan**
  - Daily calorie target
  - Sample meal plan (breakfast, lunch, dinner, snacks)
  - Lifestyle recommendations

### Step 4: New Assessment
Click **"🔄 New Assessment"** to analyze another patient

---

## 🎨 Features

✅ **Modern, Responsive Design** - Works on desktop, tablet, and mobile  
✅ **Real-time Predictions** - Instant results using trained ML models  
✅ **Personalized Recommendations** - Custom nutrition plans  
✅ **Beautiful Visualizations** - Clean, professional interface  
✅ **Easy to Use** - Intuitive form layout  

---

## 📂 Web Application Structure

```
mini_project/
├── app.py                    # Flask application (backend)
├── templates/
│   └── index.html           # Main page (frontend)
├── static/
│   ├── style.css            # Styling
│   └── script.js            # JavaScript logic
└── models/                  # Trained ML models
```

---

## 🔧 API Endpoints

### GET /
- **Description**: Main application page
- **Returns**: HTML form

### POST /predict
- **Description**: Make obesity risk prediction
- **Input**: Form data (patient information)
- **Returns**: JSON with prediction and nutrition recommendations

---

## 🎯 Example Usage

1. **Enter Patient Data**:
   - Age: 30
   - Gender: Male
   - Height: 1.75 m
   - Weight: 85 kg
   - (fill in other fields)

2. **Click "Analyze Health Risk"**

3. **Get Results**:
   - Risk Level: Overweight Level I
   - BMI: 27.76
   - Confidence: 85%
   - Calorie Target: 1800-2200 kcal/day
   - Meal plan and lifestyle tips

---

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production Deployment

#### Option 1: Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

#### Option 2: PythonAnywhere
1. Upload files to PythonAnywhere
2. Configure WSGI file
3. Set up virtual environment

#### Option 3: AWS/Azure
- Deploy using Elastic Beanstalk (AWS)
- Deploy using App Service (Azure)

---

## 🛠️ Customization

### Change Colors
Edit `static/style.css` - modify CSS variables:
```css
:root {
    --primary-color: #2563eb;  /* Change this */
    --success-color: #10b981;  /* And this */
}
```

### Add New Features
- Edit `app.py` for backend logic
- Edit `templates/index.html` for UI
- Edit `static/script.js` for interactivity

---

## 📊 Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Models**: scikit-learn (Ensemble)
- **Styling**: Custom CSS with gradients
- **AJAX**: Fetch API for async requests

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Models Not Found
Make sure you've run `python main.py` first to train models

### CSS Not Loading
Check that `static/` folder exists and contains `style.css`

---

**Status**: ✅ Web Application Ready!  
**Access**: http://127.0.0.1:5000
