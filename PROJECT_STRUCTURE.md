# Project Structure

## Directory Tree

```
UFAC/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # 5-minute setup guide
├── 📄 IMPROVEMENTS.md              # Detailed improvements
├── 📄 DEPLOYMENT.md                # Production deployment
├── 📄 CHANGES_SUMMARY.md           # Summary of changes
├── 📄 PROJECT_STRUCTURE.md         # This file
│
├── 📄 main.py                      # CLI entry point (test cases)
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env                         # Environment variables (create this!)
├── 📄 .env.example                 # Environment template
│
├── 📁 api/                         # REST API
│   └── 📄 app.py                   # FastAPI application
│
├── 📁 core/                        # Core UFAC engine
│   ├── 📄 __init__.py              # Package initialization
│   ├── 📄 ufac_engine.py           # Main orchestration engine
│   ├── 📄 llm_utils.py             # Gemini API utilities
│   ├── 📄 schema.py                # Pydantic response schema
│   │
│   ├── 📄 fact_agent.py            # Fact extraction agent
│   ├── 📄 assumption_agent.py      # Assumption detection agent
│   ├── 📄 unknown_agent.py         # Unknown detection agent
│   ├── 📄 confidence_agent.py      # Confidence calculation agent
│   └── 📄 decision_agent.py        # Decision guidance agent
│
├── 📁 data/                        # Data and rules
│   └── 📄 pm_kisan_rules.py        # PM-KISAN eligibility rules
│
├── 📁 tests/                       # Test suite (empty, ready for tests)
│
└── 📁 .git/                        # Git repository
```

---

## File Descriptions

### Root Level

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point with 3 test cases |
| `requirements.txt` | Python package dependencies |
| `.env` | Environment variables (create from `.env.example`) |
| `.env.example` | Template for `.env` file |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Complete project documentation |
| `QUICKSTART.md` | 5-minute setup and usage guide |
| `IMPROVEMENTS.md` | Detailed list of improvements made |
| `DEPLOYMENT.md` | Production deployment guide |
| `CHANGES_SUMMARY.md` | Summary of all changes |
| `PROJECT_STRUCTURE.md` | This file |

### API (`api/`)

| File | Purpose |
|------|---------|
| `app.py` | FastAPI application with REST endpoints |

### Core Engine (`core/`)

| File | Purpose |
|------|---------|
| `ufac_engine.py` | Main orchestration engine |
| `llm_utils.py` | Google Gemini API utilities |
| `schema.py` | Pydantic response schema |
| `fact_agent.py` | Extracts confirmed facts |
| `assumption_agent.py` | Detects implicit assumptions |
| `unknown_agent.py` | Identifies missing information |
| `confidence_agent.py` | Calculates confidence score |
| `decision_agent.py` | Generates next steps |

### Data (`data/`)

| File | Purpose |
|------|---------|
| `pm_kisan_rules.py` | PM-KISAN eligibility rules |

### Tests (`tests/`)

Empty directory ready for unit tests.

---

## Data Flow

```
User Input
    ↓
main.py / api/app.py
    ↓
core/ufac_engine.py (Orchestrator)
    ├→ fact_agent.py (Extract facts)
    ├→ assumption_agent.py (Detect assumptions)
    ├→ unknown_agent.py (Identify unknowns)
    ├→ confidence_agent.py (Calculate confidence)
    └→ decision_agent.py (Generate next steps)
    ↓
core/llm_utils.py (Gemini API calls)
    ↓
core/schema.py (Format response)
    ↓
UFACResponse (JSON output)
```

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    UFAC Engine                          │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Fact Agent   │  │Assumption    │  │ Unknown      │ │
│  │              │  │ Agent        │  │ Agent        │ │
│  │ Extracts     │  │              │  │              │ │
│  │ confirmed    │  │ Identifies   │  │ Identifies   │ │
│  │ facts        │  │ assumptions  │  │ missing info │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         ↓                  ↓                  ↓         │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │ Confidence   │  │ Decision     │                    │
│  │ Agent        │  │ Agent        │                    │
│  │              │  │              │                    │
│  │ Calculates   │  │ Generates    │                    │
│  │ confidence   │  │ next steps   │                    │
│  └──────────────┘  └──────────────┘                    │
│         ↓                  ↓                            │
│  ┌─────────────────────────────────────────────────┐  │
│  │         LLM Council (Gemini API)                │  │
│  │  Each agent runs 3 times with different temps  │  │
│  │  Responses aggregated by consensus voting      │  │
│  └─────────────────────────────────────────────────┘  │
│         ↓                                              │
│  ┌─────────────────────────────────────────────────┐  │
│  │         UFACResponse (Structured Output)        │  │
│  │  - answer, confidence, facts, assumptions      │  │
│  │  - unknowns, risk_level, next_steps            │  │
│  │  - consensus scores for each agent             │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## API Endpoints

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Server                       │
│                                                         │
│  GET  /                                                 │
│  └─ API information and endpoint listing               │
│                                                         │
│  GET  /health                                           │
│  └─ Health check (for monitoring)                      │
│                                                         │
│  POST /check                                            │
│  ├─ Input: EligibilityCheckRequest                     │
│  └─ Output: UFACResponse                               │
│                                                         │
│  GET  /docs                                             │
│  └─ Interactive Swagger UI documentation              │
│                                                         │
│  GET  /redoc                                            │
│  └─ ReDoc documentation                                │
└─────────────────────────────────────────────────────────┘
```

---

## Configuration Files

### `.env` (Create from `.env.example`)
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### `requirements.txt`
```
google-generativeai>=0.3.0
pydantic>=2.0.0
python-dotenv>=1.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
```

---

## Usage Paths

### Path 1: CLI Testing
```
main.py
  ↓
core/ufac_engine.py
  ↓
Print results to console
```

### Path 2: API Server
```
uvicorn api.app:app
  ↓
api/app.py
  ↓
core/ufac_engine.py
  ↓
Return JSON response
```

### Path 3: Direct Python
```python
from core.ufac_engine import run_ufac
result = run_ufac(user_data)
```

---

## Development Workflow

```
1. Edit agent prompts in core/*_agent.py
   ↓
2. Test with main.py
   ↓
3. Run API server with uvicorn
   ↓
4. Test endpoints with /docs UI
   ↓
5. Deploy to production
```

---

## Key Files to Modify

### To Customize PM-KISAN Rules
→ Edit `data/pm_kisan_rules.py`

### To Improve Agent Prompts
→ Edit `core/*_agent.py` files

### To Add API Features
→ Edit `api/app.py`

### To Change LLM Behavior
→ Edit `core/llm_utils.py`

### To Adjust Response Format
→ Edit `core/schema.py`

---

## Dependencies Map

```
main.py
  ├─ core/ufac_engine.py
  │   ├─ core/fact_agent.py
  │   ├─ core/assumption_agent.py
  │   ├─ core/unknown_agent.py
  │   ├─ core/confidence_agent.py
  │   ├─ core/decision_agent.py
  │   ├─ core/schema.py
  │   └─ data/pm_kisan_rules.py
  └─ core/llm_utils.py
      └─ google.generativeai

api/app.py
  ├─ fastapi
  ├─ pydantic
  ├─ core/ufac_engine.py
  └─ core/schema.py
```

---

## Environment Setup

```
1. Create .env from .env.example
   ↓
2. Add GEMINI_API_KEY
   ↓
3. Install requirements: pip install -r requirements.txt
   ↓
4. Run: python main.py or uvicorn api.app:app
```

---

## Deployment Structure

```
Production Server
  ├─ Python 3.11+
  ├─ requirements.txt (installed)
  ├─ .env (with API key)
  ├─ api/app.py (running on Uvicorn)
  ├─ core/ (all agent files)
  ├─ data/ (rules)
  └─ Monitoring & Logging
```

---

## File Size Reference

| File | Size | Purpose |
|------|------|---------|
| `main.py` | ~1 KB | CLI tests |
| `api/app.py` | ~3 KB | REST API |
| `core/ufac_engine.py` | ~2 KB | Orchestration |
| `core/llm_utils.py` | ~2 KB | LLM utilities |
| `core/*_agent.py` | ~1 KB each | Individual agents |
| `core/schema.py` | ~0.5 KB | Response schema |
| `data/pm_kisan_rules.py` | ~1 KB | Rules |

**Total**: ~15 KB of code (very lightweight!)

---

## Next Steps

1. **Setup**: Follow `QUICKSTART.md`
2. **Test**: Run `python main.py`
3. **Deploy**: Follow `DEPLOYMENT.md`
4. **Customize**: Edit agent prompts and rules
5. **Monitor**: Track API usage and performance

---

## Quick Reference

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key

# Test CLI
python main.py

# Run API server
uvicorn api.app:app --reload

# Visit API docs
http://localhost:8000/docs

# Deploy
docker build -t ufac-engine .
docker run -e GEMINI_API_KEY=key -p 8000:8000 ufac-engine
```

---

## Support

- **Setup Issues**: See `QUICKSTART.md`
- **API Issues**: See `README.md`
- **Deployment**: See `DEPLOYMENT.md`
- **Changes**: See `CHANGES_SUMMARY.md`
- **Improvements**: See `IMPROVEMENTS.md`
