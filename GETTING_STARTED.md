# Getting Started Checklist

## ✅ Pre-Setup (5 minutes)

- [ ] You have Python 3.8+ installed
- [ ] You have a Google Gemini API key (get from [aistudio.google.com](https://aistudio.google.com/app/apikey))
- [ ] You have git installed
- [ ] You have this repository cloned

---

## ✅ Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd UFAC

# Install Python packages
pip install -r requirements.txt
```

**Verify installation:**
```bash
python -c "import google.generativeai; import fastapi; print('✓ All dependencies installed')"
```

---

## ✅ Step 2: Configure API Key (1 minute)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# On Windows:
notepad .env

# On Mac/Linux:
nano .env
```

**Your .env should look like:**
```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here...
```

**Verify configuration:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✓ API Key loaded' if os.getenv('GEMINI_API_KEY') else '✗ API Key not found')"
```

---

## ✅ Step 3: Test CLI (2 minutes)

```bash
# Run the test script
python main.py
```

**Expected output:**
- 3 test cases with UFAC assessments
- JSON formatted responses
- Confidence scores, facts, assumptions, unknowns, next steps

**If it works:**
```
✓ CLI test successful
✓ Gemini API is working
✓ All agents are functioning
```

---

## ✅ Step 4: Run API Server (1 minute)

```bash
# Start the FastAPI server
uvicorn api.app:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## ✅ Step 5: Test API (2 minutes)

**Option A: Interactive Swagger UI**
1. Open browser: `http://localhost:8000/docs`
2. Click on "POST /check"
3. Click "Try it out"
4. Enter sample data:
```json
{
  "occupation": "farmer",
  "land_ownership": "yes",
  "aadhaar_linked": true,
  "bank_account": true,
  "state": "Punjab"
}
```
5. Click "Execute"
6. See the response

**Option B: cURL**
```bash
curl -X POST "http://localhost:8000/check" \
  -H "Content-Type: application/json" \
  -d '{
    "occupation": "farmer",
    "land_ownership": "yes",
    "aadhaar_linked": true
  }'
```

**Option C: Python**
```python
import requests

response = requests.post(
    "http://localhost:8000/check",
    json={
        "occupation": "farmer",
        "land_ownership": "yes",
        "aadhaar_linked": True
    }
)
print(response.json())
```

---

## ✅ Step 6: Verify Everything Works

Run this verification script:

```bash
# Create verify.py
cat > verify.py << 'EOF'
import os
from dotenv import load_dotenv
import google.generativeai as genai
from core.ufac_engine import run_ufac

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("UFAC Engine Verification")
print("=" * 60)

# Check 1: API Key
if api_key:
    print("✓ API Key loaded")
else:
    print("✗ API Key not found")
    exit(1)

# Check 2: Gemini Connection
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say 'OK'")
    print("✓ Gemini API connection working")
except Exception as e:
    print(f"✗ Gemini API error: {e}")
    exit(1)

# Check 3: UFAC Engine
try:
    result = run_ufac({"occupation": "farmer"})
    print("✓ UFAC Engine working")
    print(f"  - Confidence: {result.confidence}")
    print(f"  - Facts: {len(result.known_facts)}")
    print(f"  - Assumptions: {len(result.assumptions)}")
    print(f"  - Unknowns: {len(result.unknowns)}")
except Exception as e:
    print(f"✗ UFAC Engine error: {e}")
    exit(1)

print("=" * 60)
print("✓ All systems operational!")
print("=" * 60)
EOF

python verify.py
```

---

## ✅ Troubleshooting

### Problem: "GEMINI_API_KEY not set"
**Solution:**
1. Check `.env` file exists
2. Verify API key is in `.env`
3. Run: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"`

### Problem: "ModuleNotFoundError: No module named 'google'"
**Solution:**
```bash
pip install google-generativeai
```

### Problem: "Connection refused" on API
**Solution:**
1. Make sure server is running: `uvicorn api.app:app --reload`
2. Check port 8000 is not in use
3. Try different port: `uvicorn api.app:app --port 8001`

### Problem: "JSON decode error"
**Solution:**
1. Check API key is valid
2. Check internet connection
3. Try again (Gemini API might be temporarily slow)

### Problem: Slow responses (>30 seconds)
**Solution:**
1. This is normal (Gemini API latency)
2. To speed up, reduce `num_runs` in `core/llm_utils.py` from 3 to 2
3. Or use caching for repeated queries

---

## ✅ Next Steps

### Option 1: Explore the Code
- Read `README.md` for full documentation
- Review `core/ufac_engine.py` to understand orchestration
- Check individual agents in `core/*_agent.py`

### Option 2: Customize for Your Use Case
- Edit `data/pm_kisan_rules.py` to add custom rules
- Modify agent prompts in `core/*_agent.py`
- Adjust confidence thresholds in `core/ufac_engine.py`

### Option 3: Deploy to Production
- Follow `DEPLOYMENT.md` for deployment options
- Choose: Docker, Heroku, AWS Lambda, Google Cloud Run, etc.
- Set up monitoring and logging

### Option 4: Integrate with Your App
```python
# In your application
from core.ufac_engine import run_ufac

def check_eligibility(user_data):
    result = run_ufac(user_data)
    return {
        "eligible": result.confidence > 70,
        "confidence": result.confidence,
        "next_steps": result.next_steps
    }
```

---

## ✅ Common Tasks

### Run CLI Tests
```bash
python main.py
```

### Start API Server
```bash
uvicorn api.app:app --reload
```

### Access API Documentation
```
http://localhost:8000/docs
```

### Check API Health
```bash
curl http://localhost:8000/health
```

### Stop Server
```
Press Ctrl+C in terminal
```

---

## ✅ File Checklist

After setup, you should have:

```
UFAC/
├── .env                    ✓ Created (with API key)
├── .env.example            ✓ Exists
├── main.py                 ✓ Exists
├── requirements.txt        ✓ Exists
├── README.md               ✓ Exists
├── QUICKSTART.md           ✓ Exists
├── DEPLOYMENT.md           ✓ Exists
├── IMPROVEMENTS.md         ✓ Exists
├── CHANGES_SUMMARY.md      ✓ Exists
├── PROJECT_STRUCTURE.md    ✓ Exists
├── GETTING_STARTED.md      ✓ Exists (this file)
├── api/app.py              ✓ Exists
├── core/
│   ├── ufac_engine.py      ✓ Exists
│   ├── llm_utils.py        ✓ Exists
│   ├── fact_agent.py       ✓ Exists
│   ├── assumption_agent.py ✓ Exists
│   ├── unknown_agent.py    ✓ Exists
│   ├── confidence_agent.py ✓ Exists
│   ├── decision_agent.py   ✓ Exists
│   └── schema.py           ✓ Exists
└── data/pm_kisan_rules.py  ✓ Exists
```

---

## ✅ Success Indicators

You'll know everything is working when:

1. ✓ `python main.py` runs without errors
2. ✓ API server starts with `uvicorn api.app:app --reload`
3. ✓ `/docs` page loads at `http://localhost:8000/docs`
4. ✓ `/check` endpoint returns valid JSON response
5. ✓ Confidence scores are between 0-100
6. ✓ All agents return non-empty lists

---

## ✅ Performance Expectations

| Operation | Time | Notes |
|-----------|------|-------|
| CLI test | 30-60s | 3 test cases × 5 agents × 3 runs |
| Single API call | 10-30s | Depends on Gemini API latency |
| Health check | <1s | No LLM calls |
| API startup | 2-5s | FastAPI initialization |

---

## ✅ Support Resources

| Issue | Resource |
|-------|----------|
| Setup help | `QUICKSTART.md` |
| API usage | `README.md` |
| Deployment | `DEPLOYMENT.md` |
| Code changes | `IMPROVEMENTS.md` |
| Project structure | `PROJECT_STRUCTURE.md` |
| What changed | `CHANGES_SUMMARY.md` |

---

## ✅ You're Ready!

Congratulations! Your UFAC Engine is now:
- ✓ Installed
- ✓ Configured
- ✓ Tested
- ✓ Running

**Next:** Choose your next step from "Next Steps" section above.

---

## 📞 Quick Help

**Stuck?** Try these:

1. Check `.env` has your API key
2. Run `python main.py` to test
3. Check error messages carefully
4. Read relevant documentation file
5. Verify internet connection
6. Try again (API might be temporarily slow)

**Still stuck?** Review the error message and check the appropriate documentation file above.

---

## 🎉 Welcome to UFAC!

You now have a production-ready PM-KISAN eligibility assessment engine powered by Google Gemini AI.

Happy coding!
