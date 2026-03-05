# 🔧 Fix Git Remote Repository

## Problem
You committed to the wrong GitHub repository and need to push to:
**https://github.com/514jester**

## ✅ Solution

Follow these steps to change the remote repository:

### Step 1: Check Current Remote
```bash
git remote -v
```

This shows where your code is currently pointing.

### Step 2: Remove Old Remote
```bash
git remote remove origin
```

### Step 3: Add Correct Remote

**Option A: If you already created a repository on GitHub**
```bash
git remote add origin https://github.com/514jester/obesity-prediction.git
```

**Option B: If you haven't created the repository yet**
1. Go to: https://github.com/514jester
2. Click "New repository" (green button)
3. Name it: `obesity-prediction` (or any name you want)
4. Click "Create repository"
5. Then run:
```bash
git remote add origin https://github.com/514jester/REPO_NAME.git
```
(Replace `REPO_NAME` with your actual repository name)

### Step 4: Push to Correct Repository
```bash
git push -u origin main
```

If it asks for authentication, you may need to:
- Use a Personal Access Token (PAT) instead of password
- Or use GitHub Desktop

---

## 🔐 Authentication (If Needed)

If you get an authentication error:

### Method 1: Personal Access Token (Recommended)

1. **Go to GitHub**: https://github.com/settings/tokens
2. **Click**: "Generate new token" → "Generate new token (classic)"
3. **Name**: "Obesity Prediction Deploy"
4. **Select scopes**: Check `repo` (all sub-items)
5. **Generate token** and **COPY IT** (you won't see it again!)
6. **When pushing**, use:
   - Username: `514jester`
   - Password: `YOUR_TOKEN` (paste the token)

### Method 2: GitHub Desktop (Easiest)

1. Download: https://desktop.github.com
2. Install and sign in with your GitHub account
3. Add your repository
4. Push with one click

---

## 📝 Complete Command Sequence

Run these commands in order:

```bash
# 1. Navigate to your project
cd c:\Users\KIIT0001\Desktop\mini_project

# 2. Check current remote
git remote -v

# 3. Remove old remote
git remote remove origin

# 4. Add your correct remote (replace REPO_NAME with your repository name)
git remote add origin https://github.com/514jester/REPO_NAME.git

# 5. Verify it's correct
git remote -v

# 6. Push to your repository
git push -u origin main
```

---

## 🆘 If You Get Errors

### Error: "failed to push some refs"
**Solution**: Force push (only if it's a new repo)
```bash
git push -u origin main --force
```

### Error: "Authentication failed"
**Solution**: Use Personal Access Token (see above)

### Error: "Repository not found"
**Solution**: Make sure you created the repository on GitHub first

---

## ✅ Verification

After pushing, verify:
1. Go to: https://github.com/514jester/REPO_NAME
2. You should see all your files
3. Check that `README.md`, `app.py`, etc. are there

---

## 🎯 Quick Fix (Copy-Paste)

If you want to create a new repository called `obesity-prediction`:

```bash
# Remove old remote
git remote remove origin

# Add new remote to your account
git remote add origin https://github.com/514jester/obesity-prediction.git

# Push
git push -u origin main
```

**Note**: Make sure you've created the `obesity-prediction` repository on GitHub first!

---

## 📱 Create Repository on GitHub

1. Go to: https://github.com/514jester
2. Click the **"+"** icon (top right) → **"New repository"**
3. **Repository name**: `obesity-prediction`
4. **Description**: "Personalized Obesity Risk Prediction System using ML"
5. **Public** or **Private** (your choice)
6. **DON'T** check "Initialize with README" (you already have files)
7. Click **"Create repository"**
8. Copy the URL shown (should be: `https://github.com/514jester/obesity-prediction.git`)
9. Use that URL in the commands above

---

**Ready to fix it?** Just follow the steps above!
