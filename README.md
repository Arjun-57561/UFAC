<div align="center">

<img src="https://img.shields.io/badge/UFAC-Engine-16a34a?style=for-the-badge&logo=leaf&logoColor=white" alt="UFAC Engine"/>

# 🌾 UFAC Engine
### *AI-Powered PM-KISAN Eligibility Assessment*

<p align="center">
  <a href="https://ufac.vercel.app"><img src="https://img.shields.io/badge/🚀%20Live%20Demo-ufac.vercel.app-16a34a?style=for-the-badge" alt="Live Demo"/></a>
  &nbsp;
  <a href="https://ufac-api.onrender.com/docs"><img src="https://img.shields.io/badge/📖%20API%20Docs-Swagger%20UI-0ea5e9?style=for-the-badge" alt="API Docs"/></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Version-2.0.0-f59e0b?style=for-the-badge" alt="Version"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=nextdotjs" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi" />
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-LLaMA3-FF6B35?style=flat-square" />
  <img src="https://img.shields.io/badge/ChromaDB-RAG-7C3AED?style=flat-square" />
  <img src="https://img.shields.io/badge/Deployed-Vercel-black?style=flat-square&logo=vercel" />
</p>

<br/>

> **UFAC** (Unknown · Fact · Assumption · Confidence) is a multi-agent LLM reasoning framework
> that determines a farmer's eligibility for India's **PM-KISAN** ₹6,000/year direct benefit scheme
> using a council of 5 specialized AI agents working in parallel.

<br/>

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🤖 The 5 Agents](#-the-5-agents)
- [📊 Performance](#-performance)
- [🚀 Quick Start](#-quick-start)
- [🔌 API Reference](#-api-reference)
- [📁 Project Structure](#-project-structure)
- [🔒 Security](#-security)
- [🧪 Testing](#-testing)
- [⚙️ Configuration](#️-configuration)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [👥 Team](#-team)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🧠 AI & Intelligence
- **5-Agent parallel reasoning** — Fact, Assumption, Unknown, Confidence, Decision
- **RAG pipeline** — ChromaDB vector search over PM-KISAN rulebook
- **LLaMA 3.3 70B** via Groq for sub-10s responses
- **Confidence scoring** — 0–100 with consensus across agents
- **Graceful degradation** — falls back to hardcoded rules if RAG fails

</td>
<td width="50%">

### ⚡ Performance
- **8–10s** first request (4.5x faster than v1)
- **0.1s** cached request (450x faster)
- **80%+** cache hit rate in production
- **Parallel agent execution** via asyncio
- **Singleton RAG** — loaded once, reused always

</td>
</tr>
<tr>
<td width="50%">

### 🔒 Security
- CORS lockdown with environment-based origins
- Rate limiting — 10 req/min on `/check`
- Input sanitization & injection detection
- Security headers (XSS, clickjacking, MIME)
- Circuit breaker — 5 failures → 60s auto-recovery

</td>
<td width="50%">

### 🎨 Frontend
- **Next.js 15** with App Router
- Dark/light mode with system preference
- Animated agent flow visualization
- Real-time backend status indicator
- Fully responsive — mobile to 4K

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│              Next.js 15  ·  ufac.vercel.app                     │
└────────────────────────────┬────────────────────────────────────┘
                             │  POST /check
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                             │
│              Rate Limiting  ·  CORS  ·  Cache                   │
└────────┬────────────────────────────────────────┬──────────────┘
         │                                        │
         ▼                                        ▼
┌────────────────────┐                  ┌─────────────────────┐
│    UFAC Engine     │                  │    RAG Pipeline     │
│   Orchestrator     │◄────────────────►│  ChromaDB + Rules   │
└────────┬───────────┘                  └─────────────────────┘
         │
         ▼  asyncio parallel execution
┌────────────────────────────────────────────────────────────────┐
│                    AGENT COUNCIL                               │
│                                                                │
│  BATCH 1 (parallel)              BATCH 2 (parallel)           │
│  ┌──────────┐ ┌────────────┐     ┌────────────┐ ┌──────────┐ │
│  │  Fact    │ │ Assumption │     │ Confidence │ │Decision  │ │
│  │  Agent   │ │   Agent    │     │   Agent    │ │  Agent   │ │
│  └──────────┘ └────────────┘     └────────────┘ └──────────┘ │
│  ┌──────────┐                                                  │
│  │ Unknown  │                                                  │
│  │  Agent   │                                                  │
│  └──────────┘                                                  │
└────────────────────────────────────────────────────────────────┘
         │
         ▼
   UFAC Response: answer · confidence · facts · assumptions ·
                  unknowns · risk_level · next_steps · consensus
```

---

## 🤖 The 5 Agents

| Agent | Role | Output |
|-------|------|--------|
| 🔍 **Fact Agent** | Extracts confirmed, objective facts from the user's input | `known_facts[]` |
| 💭 **Assumption Agent** | Identifies implicit assumptions being made | `assumptions[]` |
| ❓ **Unknown Agent** | Detects missing critical information that could change the verdict | `unknowns[]` |
| 📊 **Confidence Agent** | Calculates a 0–100 confidence score based on available data | `confidence` score |
| ✅ **Decision Agent** | Generates the final verdict and actionable next steps | `answer`, `next_steps[]` |

Each agent runs 3× independently and the results are **consensus-aggregated** — meaning the final answer reflects agreement across all runs, reducing hallucination.

---

## 📊 Performance

```
                  v1.0        v2.0       Improvement
                ─────────   ─────────   ──────────────
First request    45s          8–10s      🟢  4.5×  faster
Cached request   45s          0.1s       🟢  450×  faster
RAG load time    10s          2s         🟢  5×    faster
Avg (80% cache)  45s          0.5s       🟢  90×   faster
Cache hit rate   0%           80%+       🟢  ∞     improvement
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Groq API key → [console.groq.com/keys](https://console.groq.com/keys)

### 1. Clone & Configure

```bash
git clone https://github.com/Arjun-57561/UFAC.git
cd UFAC

# Copy and fill in your API key
cp .env.example .env
# Edit .env → add GROQ_API_KEY=gsk_...
```

### 2. Backend

```bash
# Install dependencies
pip install -r requirements.txt

# (Optional) Setup RAG vector database
python setup_rag.py

# Start API server
python -m uvicorn api.app:app --reload
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

### 3. Frontend

```bash
cd UI
npm install
npm run dev
# → http://localhost:3000
```

> 💡 **That's it.** Open `http://localhost:3000`, fill in the form, and watch the 5 agents assess eligibility in real-time.

---

## 🔌 API Reference

### `POST /check` — Run Assessment

**Request:**
```json
{
  "occupation": "farmer",
  "land_ownership": "yes",
  "aadhaar_linked": true,
  "aadhaar_ekyc": true,
  "bank_account": true,
  "annual_income": 180000,
  "income_tax_payer": false,
  "government_employee": false,
  "monthly_pension_above_10k": false,
  "practicing_professional": false,
  "constitutional_post": false
}
```

**Response:**
```json
{
  "answer": "ELIGIBLE for PM-KISAN",
  "confidence": 92,
  "known_facts": ["User is a farmer", "User owns agricultural land"],
  "assumptions": ["Land is self-cultivated, not leased out"],
  "unknowns": ["Land size not specified"],
  "risk_level": "LOW",
  "next_steps": ["Register at pmkisan.gov.in", "Submit land records (Khasra/Khatauni)"],
  "fact_consensus": 0.91,
  "confidence_consensus": 0.88
}
```

### Other Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check + RAG status |
| `GET` | `/metrics` | Request counts, latency, errors |
| `GET` | `/cache-stats` | Hit rate, memory usage |
| `GET` | `/circuit-status` | Circuit breaker state |
| `GET` | `/history` | Past assessments (paginated) |
| `GET` | `/history/{id}` | Full assessment by ID |
| `POST` | `/cache-clear` | Flush all caches |
| `GET` | `/docs` | Swagger UI |

---

## 📁 Project Structure

```
UFAC/
├── 📂 api/
│   └── app.py                  # FastAPI app — routing, middleware, rate limiting
│
├── 📂 core/
│   ├── fact_agent.py           # Agent: extracts known facts
│   ├── assumption_agent.py     # Agent: identifies assumptions
│   ├── unknown_agent.py        # Agent: detects missing info
│   ├── confidence_agent.py     # Agent: scores confidence 0–100
│   ├── decision_agent.py       # Agent: final verdict + next steps
│   ├── ufac_engine.py          # Orchestrator — runs agents in parallel
│   ├── llm_utils.py            # Groq API wrapper with retry + circuit breaker
│   ├── cache.py                # In-memory TTL cache
│   ├── metrics.py              # Request/latency/error tracking
│   ├── circuit_breaker.py      # Circuit breaker pattern
│   ├── database.py             # SQLite/PostgreSQL persistence
│   ├── constants.py            # Centralized config (no magic numbers)
│   └── schema.py               # Pydantic response schemas
│
├── 📂 data/
│   ├── rag_pipeline.py         # RAG with singleton + fallback
│   ├── pm_kisan_rules.py       # Hard-coded eligibility rules (fallback)
│   └── chroma_db/              # ChromaDB vector store
│
├── 📂 UI/                      # Next.js 15 frontend
│   ├── app/                    # App Router pages
│   │   ├── page.tsx            # Home / landing
│   │   ├── check/page.tsx      # Eligibility form + results
│   │   ├── flow/page.tsx       # Agent flow visualization
│   │   └── about/page.tsx      # About page
│   ├── components/             # Reusable React components
│   ├── hooks/                  # useUFACAssessment, useBackendStatus
│   └── lib/                    # API client, constants, utils
│
├── 📂 tests/                   # 30+ unit tests
├── 📄 requirements.txt
├── 📄 .env.example
└── 📄 README.md
```

---

## 🔒 Security

| Feature | Implementation | Status |
|---------|---------------|--------|
| CORS lockdown | `ALLOWED_ORIGINS` env var | ✅ |
| Rate limiting | 10 req/min on `/check` | ✅ |
| Input sanitization | Injection pattern regex | ✅ |
| Security headers | X-Frame, XSS, MIME | ✅ |
| Circuit breaker | 5 failures → 60s pause | ✅ |
| Exponential backoff | 3 retries with tenacity | ✅ |
| No secrets in logs | Env-based config only | ✅ |

---

## 🧪 Testing

```bash
# Run full test suite
pytest tests/ -v

# With coverage report
pytest tests/ --cov=core --cov=api --cov-report=html

# Individual test files
pytest tests/test_cache.py          # Cache layer
pytest tests/test_error_handling.py # Error handling
pytest tests/test_api.py            # API endpoints
```

> 30+ unit tests across cache, error handling, and API endpoints.

---

## ⚙️ Configuration

Create a `.env` file (copy from `.env.example`):

```bash
# ── Required ──────────────────────────────────────
GROQ_API_KEY=gsk_your_key_here

# ── Security ──────────────────────────────────────
ALLOWED_ORIGINS=http://localhost:3000,https://ufac.vercel.app

# ── Performance ───────────────────────────────────
LLM_TIMEOUT_SECONDS=15.0
CACHE_TTL_ASSESSMENT=3600   # 1 hour
CACHE_TTL_RAG=7200          # 2 hours
CACHE_TTL_LLM=3600          # 1 hour

# ── Database ──────────────────────────────────────
DATABASE_URL=sqlite+aiosqlite:///./ufac_engine.db

# ── Development ───────────────────────────────────
DEV_MODE=true               # Uses 1 LLM call instead of 3
LOG_LEVEL=INFO
```

---

## 🛠️ Troubleshooting

<details>
<summary><b>❌ Backend won't start</b></summary>

- Check `GROQ_API_KEY` is set correctly in `.env`
- Verify port 8000 is free: `lsof -i :8000`
- Check `ALLOWED_ORIGINS` includes your frontend URL
</details>

<details>
<summary><b>❌ Rate limit errors (HTTP 429)</b></summary>

- Wait 60 seconds between bursts
- Check current counts at `GET /metrics`
- Use `DEV_MODE=true` during development
</details>

<details>
<summary><b>❌ Circuit breaker open</b></summary>

- Check `GET /circuit-status`
- Verify your Groq API key is valid and has quota
- Circuit auto-recovers after 60 seconds
</details>

<details>
<summary><b>❌ RAG not working</b></summary>

- Run `python setup_rag.py` to build the vector DB
- Check `GET /rag-status` for details
- System falls back to hardcoded rules automatically
</details>

<details>
<summary><b>❌ Frontend shows blank page</b></summary>

- Check browser console for errors
- Ensure backend is running on port 8000
- Verify `NEXT_PUBLIC_API_URL` in `UI/.env.local`
</details>

---

## 👥 Team

<div align="center">

**BTech AIML · PBL-2 Project · 2023–2027 Batch**

| Role | Contribution |
|------|--------------|
| 🧑‍💻 Backend & AI Architecture | UFAC engine, agents, RAG pipeline, FastAPI |
| 🎨 Frontend Development | Next.js UI, components, animations |
| 📊 Data & Rules | PM-KISAN ruleset, ChromaDB, preprocessing |
| 🧪 Testing & DevOps | Test suite, Vercel deployment, CI |

</div>

---

<div align="center">

**UFAC Engine v2.0** — Production-ready since April 2026

<a href="https://ufac.vercel.app">🌐 Live Site</a> &nbsp;·&nbsp;
<a href="https://ufac-api.onrender.com/docs">📖 API Docs</a> &nbsp;·&nbsp;
<a href="https://github.com/Arjun-57561/UFAC/issues">🐛 Report Bug</a>

<br/>

![Made with ❤️ for Indian Farmers](https://img.shields.io/badge/Made%20with%20%E2%9D%A4%EF%B8%8F%20for-Indian%20Farmers-ff6b35?style=flat-square)

</div>
