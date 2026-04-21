# 🚀 START HERE - Connect Your Frontend & Backend

## What This Is

Your PM-KISAN UFAC Engine has two parts:
1. **Backend** (FastAPI) - The AI brain with 5 agents
2. **Frontend** (Next.js) - The user interface

They need to talk to each other. This guide shows you how.

## ⚡ Super Quick Start (3 Steps)

### 1️⃣ Setup Backend (2 minutes)

```bash
# Copy and edit .env file
cp .env.example .env
# Add your Groq API key to .env

# Install and start
pip install -r requirements.txt
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at: http://localhost:8000

### 2️⃣ Setup Frontend (2 minutes)

Open a NEW terminal:

```bash
cd UI
npm install
npm run dev
```

✅ Frontend running at: http://localhost:3000

### 3️⃣ Test It (1 minute)

1. Open: http://localhost:3000/eligibility
2. Fill the form with any data
3. Click "Check Eligibility"
4. See AI-powered results! 🎉

## 📚 Documentation Guide

Choose your path:

### 🏃 I Want to Start NOW
→ [QUICK_START.md](QUICK_START.md) - 5-minute setup guide

### 📋 I Want a Checklist
→ [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Step-by-step checklist

### 📖 I Want Details
→ [CONNECT_FRONTEND_BACKEND.md](CONNECT_FRONTEND_BACKEND.md) - Complete guide

### 🎨 I Want to See Architecture
→ [CONNECTION_DIAGRAM.md](CONNECTION_DIAGRAM.md) - Visual diagrams

### 📊 I Want the Summary
→ [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md) - What was done

### 📚 I Want Everything
→ [README.md](README.md) - Full documentation

## 🎯 What You Need

- Python 3.8+ (`python --version`)
- Node.js 18+ (`node --version`)
- Groq API key (free at https://console.groq.com/keys)
- 10 minutes of your time

## 🔥 Quick Commands

### Start Backend
```bash
# Windows
start_backend.bat

# Linux/Mac
bash start_backend.sh
```

### Start Frontend
```bash
cd UI

# Windows
start_frontend.bat

# Linux/Mac
bash start_frontend.sh
```

## 🎬 What Happens

```
┌─────────────┐
│  You fill   │
│  the form   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Frontend   │ ───> │   Backend   │ ───> │  5 AI       │
│  (React)    │      │  (FastAPI)  │      │  Agents     │
└─────────────┘      └─────────────┘      └──────┬──────┘
       ▲                                          │
       │                                          │
       └──────────────────────────────────────────┘
              Results with AI analysis
```

## ✅ Success Looks Like

- ✅ Backend shows: "UFAC Engine ready for requests"
- ✅ Frontend shows: "Ready"
- ✅ Form submission works
- ✅ Results display with AI insights
- ✅ No errors in console

## ❌ Common Problems

### "GROQ_API_KEY not found"
→ Create `.env` file and add your API key

### "Port already in use"
→ Kill the process or use different port

### "Cannot connect to backend"
→ Make sure backend is running on port 8000

### "Module not found"
→ Run `pip install -r requirements.txt` or `npm install`

## 🆘 Need Help?

1. Check [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Detailed troubleshooting
2. Check [CONNECT_FRONTEND_BACKEND.md](CONNECT_FRONTEND_BACKEND.md) - Full guide
3. Check browser console (F12) for errors
4. Check terminal for error messages

## 🎓 Learn More

### For Developers
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

### For Users
- Eligibility Check: http://localhost:3000/eligibility
- Agent Flow: http://localhost:3000/agent-flow
- About: http://localhost:3000/about

## 🚀 Next Steps After Setup

1. **Test different scenarios** - Try various farmer profiles
2. **Explore the API** - Visit /docs endpoint
3. **Customize the UI** - Edit components
4. **Add more rules** - Enhance eligibility logic
5. **Deploy to production** - See deployment guide

## 📦 What Was Created

New files for you:
- `UI/.env.local` - Frontend config
- `QUICK_START.md` - Quick guide
- `SETUP_CHECKLIST.md` - Detailed checklist
- `CONNECT_FRONTEND_BACKEND.md` - Full documentation
- `CONNECTION_DIAGRAM.md` - Architecture diagrams
- `INTEGRATION_SUMMARY.md` - What changed
- `START_HERE.md` - This file
- `start_backend.bat/.sh` - Backend startup scripts
- `UI/start_frontend.bat/.sh` - Frontend startup scripts

Modified files:
- `UI/app/eligibility/page.tsx` - Now uses real API
- `UI/components/eligibility-results.tsx` - Shows UFAC data
- `README.md` - Updated with new guides

## 🎉 You're Ready!

Pick a guide above and start connecting your frontend to backend.

**Recommended path:**
1. Read [QUICK_START.md](QUICK_START.md)
2. Follow [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
3. Test at http://localhost:3000/eligibility
4. Celebrate! 🎊

---

**Questions?** Check the documentation files above or open an issue.

**Ready to start?** → [QUICK_START.md](QUICK_START.md)
