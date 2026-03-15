# Quick Start Guide

## 1. Setup (2 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

## 2. Test It (1 minute)

```bash
# Run the CLI test
python main.py
```

You'll see 3 test cases with detailed UFAC assessments.

## 3. Run API Server (1 minute)

```bash
# Start FastAPI server
uvicorn api.app:app --reload

# Open browser to http://localhost:8000/docs
# Try the /check endpoint with sample data
```

## Sample Request

```json
{
  "occupation": "farmer",
  "land_ownership": "yes",
  "aadhaar_linked": true,
  "bank_account": true,
  "state": "Punjab"
}
```

## What You Get

- **Confidence Score**: 0-100 reliability of assessment
- **Known Facts**: What we confirmed from your data
- **Assumptions**: What we're assuming (not stated)
- **Unknowns**: What's missing for full assessment
- **Risk Level**: HIGH/MEDIUM/LOW based on confidence
- **Next Steps**: Actions to complete eligibility check

## Key Files

- `main.py` - CLI entry point
- `api/app.py` - REST API
- `core/ufac_engine.py` - Main orchestration
- `core/*_agent.py` - Individual agents
- `.env` - Your API key (create this!)

## Troubleshooting

**"GEMINI_API_KEY not set"**
→ Create `.env` file with your API key

**"JSON decode error"**
→ Gemini response format issue, check API key validity

**Slow responses**
→ Normal (10-30s), Gemini API latency

## Next Steps

1. Customize PM-KISAN rules in `data/pm_kisan_rules.py`
2. Add more test cases in `main.py`
3. Deploy API to production
4. Integrate with your application

## Need Help?

Check `README.md` for detailed documentation.
