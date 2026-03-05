# 🔐 Fix Git Credentials Issue

## Problem
Git is trying to use `AAmardeep15` credentials instead of `514jester`.

Error: `Permission to 514jester/obesity-prediction.git denied to AAmardeep15`

## ✅ Solutions

### Solution 1: Clear Git Credentials (Recommended)

Run this command to clear cached credentials:

```bash
git credential-manager delete https://github.com
```

Or try:

```bash
git config --global --unset credential.helper
```

Then push again:

```bash
git push -u origin main
```

It will ask for credentials - use:
- Username: `514jester`
- Password: Your Personal Access Token

---

### Solution 2: Use Personal Access Token in URL

Update the remote URL to include authentication:

```bash
git remote set-url origin https://YOUR_TOKEN@github.com/514jester/obesity-prediction.git
```

Replace `YOUR_TOKEN` with your GitHub Personal Access Token.

Then push:

```bash
git push -u origin main
```

---

### Solution 3: Use GitHub Desktop (Easiest!)

1. **Download GitHub Desktop**: https://desktop.github.com
2. **Install and sign in** with your `514jester` account
3. **Add existing repository**: File → Add Local Repository
4. **Browse** to: `C:\Users\KIIT0001\Desktop\mini_project`
5. **Publish repository** or **Push** with one click!

This automatically handles authentication! ✨

---

### Solution 4: Windows Credential Manager

1. Press **Windows Key**
2. Type: **Credential Manager**
3. Click **Windows Credentials**
4. Find entries for `git:https://github.com`
5. **Remove** or **Edit** them
6. Try pushing again

---

## 🔑 Create Personal Access Token

If you don't have a token yet:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Name**: "Obesity Prediction Deploy"
4. **Expiration**: 90 days (or your choice)
5. **Select scopes**: Check **"repo"** (all sub-items)
6. Click **"Generate token"**
7. **COPY THE TOKEN** immediately (you won't see it again!)

---

## 📝 Step-by-Step Fix

### Option A: Clear Credentials (Quick)

```bash
# 1. Clear credentials
git credential-manager delete https://github.com

# 2. Push (will ask for credentials)
git push -u origin main

# 3. When prompted:
#    Username: 514jester
#    Password: YOUR_PERSONAL_ACCESS_TOKEN
```

### Option B: Use GitHub Desktop (Easiest)

1. Download and install GitHub Desktop
2. Sign in with `514jester` account
3. Add your repository
4. Push with one click!

---

## ✅ Recommended: Use GitHub Desktop

This is the **easiest** solution for Windows users!

**Download**: https://desktop.github.com

After installing:
1. Sign in with your GitHub account (`514jester`)
2. File → Add Local Repository
3. Select: `C:\Users\KIIT0001\Desktop\mini_project`
4. Click "Publish repository" or "Push origin"
5. Done! ✨

---

**Try one of these solutions and let me know which one works for you!**
