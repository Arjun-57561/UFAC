# Quick Start Guide - UFAC Engine v2.0

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed
- Groq API key (get from https://console.groq.com/keys)

## 🚀 Quick Start (5 minutes)

### Step 1: Setup Backend

```bash
# 1. Create .env file
cp .env.example .env

# 2. Edit .env and add your Groq API key
# GROQ_API_KEY=your_actual_key_here
# ALLOWED_ORIGINS=http://localhost:3000

# 3. Install Python dependencies (includes new security & resilience packages)
pip install -r requirements.txt
# New packages: slowapi (rate limiting), tenacity (retry logic), sqlalchemy, aiosqlite

# 4. (Optional) Setup RAG pipeline
python setup_rag.py

# 5. Start backend server
# On Windows:
start_backend.bat

# On Linux/Mac:
bash start_backend.sh
# or
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: **http://localhost:8000**

**New in v2.0:**
- ✅ CORS lockdown (environment-based origins)
- ✅ Rate limiting (10 requests/minute on /check)
- ✅ Input sanitization (injection protection)
- ✅ Circuit breaker for API resilience
- ✅ Retry with exponential backoff
- ✅ Configurable cache TTL
- ✅ Database persistence (SQLite/PostgreSQL)
- ✅ Assessment history tracking
- ✅ Enhanced frontend with animations

### Step 2: Setup Frontend

Open a NEW terminal window:

```bash
# 1. Navigate to UI folder
cd UI

# 2. Install dependencies
npm install

# 3. Start frontend server
# On Windows:
start_frontend.bat

# On Linux/Mac:
bash start_frontend.sh
# or
npm run dev
```

Frontend will run at: **http://localhost:3000**

### Step 3: Test the Connection

1. Open browser: http://localhost:3000/eligibility
2. Fill the form with test data
3. Click "Check Eligibility"
4. See results from the UFAC engine!

## 📁 What Changed?

### New Files Created:
- `UI/.env.local` - Frontend environment config
- `CONNECT_FRONTEND_BACKEND.md` - Detailed connection guide
- `start_backend.bat` / `start_backend.sh` - Backend startup scripts
- `UI/start_frontend.bat` / `UI/start_frontend.sh` - Frontend startup scripts

### Modified Files:
- `UI/app/eligibility/page.tsx` - Now calls real API instead of mock data
- `UI/components/eligibility-results.tsx` - Added UFAC response support

## 🔧 How It Works

```
User fills form → Frontend (React) → HTTP POST to /check → Backend (FastAPI)
                                                              ↓
                                                         UFAC Engine
                                                         (5 AI Agents)
                                                              ↓
User sees results ← Frontend ← JSON Response ← Backend ← Assessment
```

## 📊 API Endpoints

| Endpoint | Method | Description | New in v2.0 |
|----------|--------|-------------|-------------|
| `/` | GET | API information | |
| `/health` | GET | Health check | |
| `/check` | POST | Eligibility assessment | ⚡ Rate limited |
| `/rag-status` | GET | RAG pipeline status | |
| `/cache-stats` | GET | Cache statistics | |
| `/metrics` | GET | System metrics | ✨ Enhanced |
| `/circuit-status` | GET | Circuit breaker status | ✅ NEW |
| `/history` | GET | Assessment history | ✅ NEW |
| `/history/{id}` | GET | Assessment details | ✅ NEW |
| `/docs` | GET | Interactive API docs | |

## 🧪 Test API Directly

Visit http://localhost:8000/docs for interactive API testing.

Or use curl:

```bash
# Run assessment
curl -X POST "http://localhost:8000/check" \
  -H "Content-Type: application/json" \
  -d '{
    "occupation": "farmer",
    "land_ownership": "yes",
    "annual_income": 200000,
    "aadhaar_linked": true,
    "bank_account": true
  }'

# View assessment history
curl http://localhost:8000/history

# Check circuit breaker status
curl http://localhost:8000/circuit-status

# View metrics
curl http://localhost:8000/metrics
```

## ❓ Troubleshooting

### Backend won't start
- Check if `.env` file exists with valid `GROQ_API_KEY`
- Check if port 8000 is already in use
- Check Python dependencies: `pip install -r requirements.txt`
- **New**: Verify `ALLOWED_ORIGINS` is set in `.env`

### Frontend won't start
- Check if Node.js is installed: `node --version`
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is already in use

### Connection errors
- Make sure BOTH backend and frontend are running
- Check `UI/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Check browser console for errors (F12)
- Verify backend is accessible: http://localhost:8000/health
- **New**: Check CORS settings if getting 400 errors

### "Failed to connect to assessment service"
- Backend is not running - start it first
- Wrong API URL in `UI/.env.local`
- Firewall blocking connection

### Rate limit errors (429)
- **New in v2.0**: /check endpoint limited to 10 requests/minute
- Wait 60 seconds before retrying
- Check `/metrics` to see request counts

### Circuit breaker open
- **New in v2.0**: After 5 consecutive failures, circuit opens for 60s
- Check `/circuit-status` endpoint
- Wait for recovery or fix underlying issue (API key, network)

### Database errors
- **New in v2.0**: Assessment history stored in SQLite by default
- Check `DATABASE_URL` in `.env` if using custom database
- Database file `ufac_engine.db` created automatically on first run
- View history: `GET /history`
- Get specific assessment: `GET /history/{id}`

## 📚 More Information

- Full connection guide: `CONNECT_FRONTEND_BACKEND.md`
- Project setup: `SETUP_AND_RUN_GUIDE.md`
- Project overview: `README.md`

## 🎯 Next Steps

1. Customize the form fields in `UI/components/eligibility-form.tsx`
2. Map more form data to API in `UI/app/eligibility/page.tsx`
3. Enhance results display in `UI/components/eligibility-results.tsx`
4. Add more validation rules in the backend
5. Deploy to production (see `CONNECT_FRONTEND_BACKEND.md`)
