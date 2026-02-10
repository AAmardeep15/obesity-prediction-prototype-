# 🚀 Deployment Guide
## How to Deploy Your Obesity Prediction Web Application

This guide covers multiple deployment options from easiest to most advanced.

---

## 📋 Table of Contents
1. [Quick Deploy - Render (Easiest, FREE)](#option-1-render-easiest-free)
2. [PythonAnywhere (FREE, Simple)](#option-2-pythonanywhere-free)
3. [Heroku (Popular, Easy)](#option-3-heroku-popular)
4. [Streamlit Cloud (Alternative, FREE)](#option-4-streamlit-cloud-alternative)
5. [AWS/Azure (Advanced)](#option-5-awsazure-advanced)

---

## ⭐ Option 1: Render (Easiest, FREE)

**Best for**: Quick deployment, free hosting, automatic HTTPS

### Step 1: Prepare Your Project

Create a `render.yaml` file:
```yaml
services:
  - type: web
    name: obesity-prediction
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

Create a `gunicorn_config.py` file:
```python
bind = "0.0.0.0:10000"
workers = 2
threads = 4
timeout = 120
```

Update `requirements.txt` to include:
```
gunicorn>=21.2.0
```

### Step 2: Deploy

1. **Create a GitHub account** (if you don't have one)
2. **Create a new repository** on GitHub
3. **Push your code**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/obesity-prediction.git
   git push -u origin main
   ```

4. **Go to [Render.com](https://render.com)**
5. **Sign up** with GitHub
6. **Click "New +"** → **"Web Service"**
7. **Connect your repository**
8. **Configure**:
   - Name: `obesity-prediction`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
9. **Click "Create Web Service"**

**Done!** Your app will be live at: `https://obesity-prediction.onrender.com`

---

## 🐍 Option 2: PythonAnywhere (FREE)

**Best for**: Beginners, no credit card needed

### Step 1: Sign Up
1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Create a **FREE** account

### Step 2: Upload Your Files
1. Click **"Files"** tab
2. Create folder: `obesity_prediction`
3. Upload all your files:
   - `app.py`
   - `requirements.txt`
   - `src/` folder
   - `models/` folder
   - `templates/` folder
   - `static/` folder

### Step 3: Install Dependencies
1. Click **"Consoles"** tab
2. Start a **Bash console**
3. Run:
   ```bash
   cd obesity_prediction
   pip install --user -r requirements.txt
   ```

### Step 4: Configure Web App
1. Click **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Choose **"Python 3.10"**
5. In **WSGI configuration file**, replace content with:
   ```python
   import sys
   path = '/home/YOUR_USERNAME/obesity_prediction'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
6. In **"Static files"** section, add:
   - URL: `/static/`
   - Directory: `/home/YOUR_USERNAME/obesity_prediction/static/`

### Step 5: Reload
1. Click **"Reload YOUR_USERNAME.pythonanywhere.com"**
2. Visit: `https://YOUR_USERNAME.pythonanywhere.com`

**Done!** Your app is live!

---

## 🔷 Option 3: Heroku (Popular)

**Best for**: Professional deployment, easy scaling

### Step 1: Prepare Files

Create `Procfile` (no extension):
```
web: gunicorn app:app
```

Create `runtime.txt`:
```
python-3.11.0
```

Update `requirements.txt`:
```
gunicorn>=21.2.0
```

### Step 2: Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 3: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create obesity-prediction-app

# Deploy
git init
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

**Done!** Your app is at: `https://obesity-prediction-app.herokuapp.com`

---

## 🎨 Option 4: Streamlit Cloud (Alternative)

**Note**: This requires converting your Flask app to Streamlit

### Step 1: Create Streamlit Version

Create `streamlit_app.py`:
```python
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.prediction import ObesityPredictor
from src.nutrition_recommendation import NutritionRecommender

# Initialize
predictor = ObesityPredictor(
    model_path='models/ensemble_model.pkl',
    preprocessor_path='models/preprocessor.pkl'
)
predictor.load_model()
predictor.load_preprocessor()
recommender = NutritionRecommender()

# UI
st.title("🏥 Obesity Risk Prediction System")
st.write("Personalized Health Assessment & Nutrition Recommendations")

# Form
with st.form("patient_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", 10, 100, 30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (m)", 1.0, 2.5, 1.75, 0.01)
        weight = st.number_input("Weight (kg)", 30, 200, 70, 1)
    
    with col2:
        family_history = st.selectbox("Family History", ["yes", "no"])
        favc = st.selectbox("High Caloric Food", ["yes", "no"])
        # ... add more fields
    
    submitted = st.form_submit_button("Analyze Health Risk")
    
    if submitted:
        patient_data = {
            'Age': age, 'Gender': gender, 'Height': height, 'Weight': weight,
            # ... all fields
        }
        
        result = predictor.predict_single(patient_data)
        
        st.success(f"Risk Level: {result['risk_level']}")
        st.metric("BMI", f"{result['bmi']:.2f}")
        st.metric("Confidence", f"{result['confidence']*100:.2f}%")
```

### Step 2: Deploy
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

---

## ☁️ Option 5: AWS/Azure (Advanced)

### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 obesity-prediction

# Create environment
eb create obesity-prediction-env

# Deploy
eb deploy

# Open
eb open
```

### Azure App Service

```bash
# Install Azure CLI
# Download from: https://aka.ms/installazurecliwindows

# Login
az login

# Create resource group
az group create --name obesity-rg --location eastus

# Create app service plan
az appservice plan create --name obesity-plan --resource-group obesity-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group obesity-rg --plan obesity-plan --name obesity-prediction --runtime "PYTHON:3.11"

# Deploy
az webapp up --name obesity-prediction --resource-group obesity-rg
```

---

## 📦 Pre-Deployment Checklist

Before deploying, make sure you have:

- [ ] `requirements.txt` with all dependencies
- [ ] `app.py` as the main Flask file
- [ ] All model files in `models/` directory
- [ ] `templates/` and `static/` folders
- [ ] `.gitignore` file (see below)

### Create `.gitignore`:
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.log
.DS_Store
.env
*.db
```

---

## 🎯 Recommended Option for Students

**For Academic Projects**: Use **Render** or **PythonAnywhere**
- ✅ FREE
- ✅ Easy to set up
- ✅ No credit card needed
- ✅ Professional URL
- ✅ HTTPS included

**For Portfolio/Resume**: Use **Heroku** or **Render**
- ✅ Professional
- ✅ Scalable
- ✅ Industry-standard

---

## 🔧 Production Configuration

For production, update `app.py`:

```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False') == 'True'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
```

---

## 🌐 Custom Domain (Optional)

After deployment, you can add a custom domain:

1. **Buy a domain** (Namecheap, GoDaddy, etc.)
2. **In your hosting platform**:
   - Render: Settings → Custom Domain
   - Heroku: Settings → Domains
   - PythonAnywhere: Web → Add custom domain (paid plans)
3. **Update DNS** records to point to your app

---

## 📊 Monitoring & Logs

### Render
- Dashboard → Logs tab

### Heroku
```bash
heroku logs --tail
```

### PythonAnywhere
- Web tab → Log files

---

## 💡 Tips for Successful Deployment

1. **Test locally first**: Make sure everything works on `localhost`
2. **Use environment variables**: For sensitive data
3. **Enable HTTPS**: Most platforms do this automatically
4. **Monitor logs**: Check for errors after deployment
5. **Set up error tracking**: Use Sentry or similar
6. **Optimize model size**: Compress if needed
7. **Add loading states**: For better UX
8. **Set timeouts**: For long-running predictions

---

## 🆘 Troubleshooting

### "Application Error" or "502 Bad Gateway"
- Check logs for errors
- Verify all dependencies are installed
- Check if models are loading correctly

### "Module not found"
- Ensure `requirements.txt` is complete
- Check Python version compatibility

### "Out of memory"
- Reduce model size
- Use smaller instance/plan
- Optimize code

### "Timeout"
- Increase timeout settings
- Optimize prediction speed
- Use async processing

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **PythonAnywhere Help**: https://help.pythonanywhere.com
- **Heroku Docs**: https://devcenter.heroku.com
- **Flask Deployment**: https://flask.palletsprojects.com/en/2.3.x/deploying/

---

## ✅ Quick Start (Recommended)

**Fastest way to deploy RIGHT NOW:**

1. **Create files** (I'll do this for you):
   - `Procfile`
   - `runtime.txt`
   - `.gitignore`

2. **Push to GitHub**

3. **Deploy on Render** (5 minutes)

Would you like me to set this up for you? Just say "yes" and I'll create all the necessary deployment files!

---

**Status**: 📖 Guide Complete  
**Recommended**: Render or PythonAnywhere  
**Difficulty**: Easy  
**Cost**: FREE
