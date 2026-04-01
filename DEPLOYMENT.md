# StyleAI Deployment Guide 🚀

Deploy your StyleAI Flask application to multiple platforms for live hosting.

---

## 📌 Deployment Directory
All deployment configurations are ready in this folder:
- ✅ `vercel.json` - Vercel configuration
- ✅ `Procfile` - Heroku/Render configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `.vercelignore` - Files to exclude from Vercel deployment

---

## 🔹 Option 1: Deploy to Vercel (Recommended)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
vercel --prod
```

### Step 4: Add Environment Variables
In your Vercel dashboard at **Settings → Environment Variables**, add:
```
GROQ_API_KEY=your_groq_api_key_here
```

**Vercel Link:** https://vercel.com/new

---

## 🔹 Option 2: Deploy to Render.com

### Step 1: Go to Render Dashboard
https://dashboard.render.com

### Step 2: Create New Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Name: `StyleAI`
- Runtime: Python 3.11
- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`

### Step 3: Add Environment Variables
In the Environment section, add:
```
GROQ_API_KEY=your_groq_api_key_here
```

### Step 4: Deploy
Click "Create Web Service" and wait for deployment.

**Render Link:** https://render.com

---

## 🔹 Option 3: Deploy to Railway.app (Easiest!)

### Step 1: Go to Railway
https://railway.app

### Step 2: Create New Project
- Click "Start a New Project"
- Select "Deploy from GitHub"
- Choose your StyleAI repository

### Step 3: Add Environment Variables
- Go to Variables tab
- Add: `GROQ_API_KEY=your_groq_api_key_here`

### Step 4: Deploy
Railway auto-deploys! Your app will be live in 1-2 minutes.

**Railway Link:** https://railway.app

---

## 🔹 Option 4: Deploy to Heroku (Classic)

### Step 1: Install Heroku CLI
```bash
https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login
```bash
heroku login
```

### Step 3: Create App
```bash
heroku create your-app-name
```

### Step 4: Set Environment Variables
```bash
heroku config:set GROQ_API_KEY=your_groq_api_key_here
```

### Step 5: Deploy
```bash
git push heroku main
```

**Heroku Link:** https://www.heroku.com

---

## 🔹 Option 5: Deploy to PythonAnywhere

### Step 1: Sign Up
https://www.pythonanywhere.com

### Step 2: Upload Your Code
- Create a new web app
- Upload your project files via Git
- Configure Python version to 3.11

### Step 3: Set Web App Configuration
- Source code: `/home/your-username/StyleAI`
- WSGI configuration: Configure Flask
- Set environment variables in web app settings

### Step 4: Reload
Click "Reload Web App" and it's live!

**PythonAnywhere Link:** https://www.pythonanywhere.com

---

## ⚡ Quick Comparison

| Platform | Cost | Setup Time | Performance | Recommendation |
|----------|------|-----------|-------------|----------------|
| **Vercel** | Free tier | 5 min | ⭐⭐⭐⭐⭐ | Best for static + serverless |
| **Railway** | Free ₹2500/mo | 2 min | ⭐⭐⭐⭐⭐ | ✅ Easiest & fastest |
| **Render** | Free tier | 5 min | ⭐⭐⭐⭐ | Good free tier |
| **Heroku** | Paid only | 5 min | ⭐⭐⭐⭐ | Classic option |
| **PythonAnywhere** | Free tier | 10 min | ⭐⭐⭐ | Good for beginners |

---

## 🔐 Important Security Notes

1. **NEVER commit `.env` file** - It's in `.gitignore` ✅
2. **Always use Environment Variables** for API keys on hosting platforms
3. **Enable HTTPS** on all platforms (automatic)
4. **Set strong secret keys** in production

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Port not available" error
Your app will auto-detect the port. Ensure your `app.py` uses:
```python
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
```

### "Image upload not working"
Ensure your platform supports `/uploads` directory or use cloud storage (AWS S3, Cloudinary)

---

## 📊 Next Steps

1. **Pick a platform** (Railway recommended for beginners)
2. **Push to GitHub** ✅ Already done!
3. **Connect repository** to your chosen platform
4. **Set API Key** in environment variables
5. **Deploy** and share your live link!

---

## 🎉 Once Live

Your app will be accessible at:
- **Vercel:** `https://your-app.vercel.app`
- **Railway:** `https://your-app.railway.app`
- **Render:** `https://your-app.onrender.com`
- **Heroku:** `https://your-app.herokuapp.com`
- **PythonAnywhere:** `https://your-username.pythonanywhere.com`

---

**Happy Deploying! 🚀**
