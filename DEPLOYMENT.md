# NEET AI Agent - Deployment Guide

## 🚀 Quick Deployment Steps

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `neet-ai-agent`
3. **Do NOT initialize** with README (we already have code)

### Step 2: Push Code to GitHub

```bash
cd c:\AI\Antigravity\neet_ai_agent
git init
git add .
git commit -m "Initial commit - NEET AI Agent with Physics content"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/neet-ai-agent.git
git push -u origin main
```

---

### Step 3: Deploy Backend to Render

1. **Go to Render**: https://render.com
2. **Sign up/Login** with GitHub
3. Click **"New +"** → **"Web Service"**
4. **Connect Repository**: Select `neet-ai-agent`
5. **Configure**:
   - **Name**: `neet-ai-backend`
   - **Region**: Choose closest to India (Singapore recommended)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

6. **Environment Variables** (Click "Advanced" → "Add Environment Variable"):
   - `GEMINI_API_KEY`: `YOUR_GEMINI_API_KEY`
   - `PINECONE_API_KEY`: `YOUR_PINECONE_API_KEY`

7. Click **"Create Web Service"**
8. **Wait 5-10 minutes** for initial deployment
9. **Copy the URL**: e.g., `https://neet-ai-backend.onrender.com`

---

### Step 4: Update Frontend with Backend URL

1. Edit `frontend/.env.production`:
   ```
   VITE_API_URL=https://neet-ai-backend.onrender.com
   ```

2. Commit and push:
   ```bash
   git add frontend/.env.production
   git commit -m "Update backend URL for production"
   git push
   ```

---

### Step 5: Deploy Frontend to Vercel

1. **Go to Vercel**: https://vercel.com
2. **Sign up/Login** with GitHub
3. Click **"Add New..."** → **"Project"**
4. **Import Repository**: Select `neet-ai-agent`
5. **Configure**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   
6. **Environment Variables**:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://neet-ai-backend.onrender.com`
   - **Environment**: Production

7. Click **"Deploy"**
8. **Wait 2-3 minutes**
9. **Your app is live!** e.g., `https://neet-ai-agent.vercel.app`

---

## ✅ Verification

Visit your Vercel URL and:
1. Wait for "Online" indicator
2. Ask: "What is Newton's second law?"
3. Verify answer appears with sources

**Note**: First request may take 30-60 seconds (Render cold start)

---

## 🔧 Post-Deployment

### Optional: Setup Custom Domain
- In Vercel → Settings → Domains
- Add your custom domain (e.g., `neet-tutor.com`)

### Optional: Prevent Cold Starts
- Use https://uptimerobot.com (free)
- Ping `https://neet-ai-backend.onrender.com/health` every 10 minutes

### Monitor Usage
- **Render**: Check logs and metrics
- **Vercel**: Monitor bandwidth
- **Gemini**: Track API calls at https://aistudio.google.com

---

## 🎓 Share with Students

```
🎓 Free NEET Physics AI Tutor
📚 Complete NCERT Class 11 & 12 Physics
🔗 https://neet-ai-agent.vercel.app

Ask me anything about:
• Newton's Laws
• Work & Energy
• Thermodynamics
• Waves & Optics
• Modern Physics
• And more!
```

---

## 🆘 Troubleshooting

**Problem**: CORS errors
- **Fix**: Update CORS in `backend/main.py` with your Vercel URL

**Problem**: Backend not responding
- **Check**: Render logs for errors
- **Fix**: Verify environment variables

**Problem**: "API key invalid"
- **Fix**: Re-check environment variables in Render dashboard
