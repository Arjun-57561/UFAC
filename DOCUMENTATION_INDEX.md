# UFAC Engine - Documentation Index

**File**: `DOCUMENTATION_INDEX.md`

Complete guide to all documentation files in the UFAC Engine project.

---

## Quick Start

**New to the project?** Start here:
1. Read `README.md` - Project overview
2. Read `SETUP_GUIDE.md` - Installation and setup
3. Read `PRIORITY_C_SUMMARY.md` - UI overview
4. Run `python -m uvicorn api.app:app --reload` - Start the server

---

## Project Documentation

### Overview & Setup
- **`README.md`** - Project overview, features, and quick start
- **`SETUP_GUIDE.md`** - Complete installation and setup instructions
- **`INDEX.md`** - Original project index
- **`DEPLOYMENT.md`** - Deployment guide (in progress)

### Progress & Status
- **`PROGRESS_REPORT.md`** - Current progress on all priorities (80% complete)
- **`COMPLETION_SUMMARY.md`** - Summary of completed work
- **`README_PRIORITIES.md`** - Quick reference for all priorities

---

## Priority Documentation

### Priority A: RAG Caching ✅ COMPLETE
- **`PRIORITY_A_SUMMARY.md`** - Comprehensive technical documentation
  - Singleton retriever pattern
  - Memory caching implementation
  - Performance improvements (4.5x faster)
  - Testing and verification

### Priority B: RAG Validation ✅ COMPLETE
- **`PRIORITY_B_SUMMARY.md`** - Comprehensive technical documentation
  - Startup validation
  - Health check endpoints
  - Graceful degradation
  - Setup script usage

### Priority C: UI React Flow ✅ COMPLETE
- **`PRIORITY_C_SUMMARY.md`** - Comprehensive technical documentation
  - React Flow visualization
  - 5-agent architecture display
  - API integration
  - Real-time assessment

### Priority D: Error Handling & Logging ✅ COMPLETE
- **`PRIORITY_D_SUMMARY.md`** - Comprehensive technical documentation
  - Custom exception hierarchy
  - Error handling patterns
  - Structured logging
  - Graceful degradation
- **`ERROR_HANDLING_GUIDE.md`** - Quick reference guide
  - Exception hierarchy
  - Error handling patterns
  - Common error scenarios
  - Debugging tips
- **`PRIORITY_D_CHANGES.md`** - Detailed changes summary
  - Files modified
  - New files created
  - Error handling improvements
  - Logging improvements
- **`COMPLETION_PRIORITY_D.md`** - Completion report
  - What was accomplished
  - Testing results
  - Performance impact
  - How to use

---

## Technical Documentation

### Architecture
- **`core/ufac_engine.py`** - 5-agent UFAC architecture
  - Batch 1: Fact, Assumption, Unknown agents
  - Batch 2: Confidence, Decision agents
  - Parallel execution with asyncio
  - Error handling and fallbacks

### Agents
- **`core/fact_agent.py`** - Fact extraction agent
- **`core/assumption_agent.py`** - Assumption detection agent
- **`core/unknown_agent.py`** - Unknown detection agent
- **`core/confidence_agent.py`** - Confidence calculation agent
- **`core/decision_agent.py`** - Decision generation agent

### Data & RAG
- **`data/rag_pipeline.py`** - RAG pipeline with caching
  - Singleton retriever pattern
  - ChromaDB integration
  - Error handling
- **`data/pm_kisan_rules.py`** - PM-KISAN eligibility rules
- **`setup_rag.py`** - RAG setup script

### API
- **`api/app.py`** - FastAPI application
  - Lifespan management
  - Request/response logging
  - Error handling
  - Health check endpoints

### UI
- **`UI/components/agent-flow-visualization.tsx`** - React Flow visualization
- **`UI/hooks/useUFACAssessment.ts`** - API integration hook
- **`UI/app/agent-flow/page.tsx`** - Agent flow page

---

## Configuration Files

- **`.env.example`** - Environment template
  - GROQ_API_KEY configuration
  - Optional settings
- **`requirements.txt`** - Python dependencies
- **`UI/package.json`** - Node.js dependencies
- **`UI/tsconfig.json`** - TypeScript configuration

---

## Extra Documentation

### In Extra Files Folder
- **`Extra Files/START_HERE.md`** - Getting started guide
- **`Extra Files/GETTING_STARTED.md`** - Detailed getting started
- **`Extra Files/PROJECT_STRUCTURE.md`** - Project structure overview
- **`Extra Files/QUICKSTART.md`** - Quick start guide
- **`Extra Files/IMPROVEMENTS.md`** - Suggested improvements
- **`Extra Files/CHANGES_SUMMARY.md`** - Summary of changes
- **`Extra Files/UPGRADE_SUMMARY.md`** - Upgrade summary
- **`Extra Files/FINAL_SUMMARY.txt`** - Final summary

---

## How to Navigate

### By Task
1. **Setting up the project**: `SETUP_GUIDE.md`
2. **Understanding the architecture**: `PRIORITY_C_SUMMARY.md`
3. **Debugging errors**: `ERROR_HANDLING_GUIDE.md`
4. **Checking progress**: `PROGRESS_REPORT.md`
5. **Deploying**: `DEPLOYMENT.md`

### By Priority
1. **Priority A (RAG Caching)**: `PRIORITY_A_SUMMARY.md`
2. **Priority B (RAG Validation)**: `PRIORITY_B_SUMMARY.md`
3. **Priority C (UI React Flow)**: `PRIORITY_C_SUMMARY.md`
4. **Priority D (Error Handling)**: `PRIORITY_D_SUMMARY.md` + `ERROR_HANDLING_GUIDE.md`
5. **Priority E (Caching Layer)**: Coming soon
6. **Priority F (Testing)**: Coming soon
7. **Priority G (Monitoring)**: Coming soon
8. **Priority H (Deployment)**: Coming soon

### By Component
1. **Backend**: `core/`, `data/`, `api/`
2. **Frontend**: `UI/`
3. **Configuration**: `.env.example`, `requirements.txt`
4. **Documentation**: All `.md` files

---

## Key Concepts

### UFAC Architecture
- **Fact Agent**: Extracts confirmed facts
- **Assumption Agent**: Identifies assumptions
- **Unknown Agent**: Detects missing information
- **Confidence Agent**: Calculates confidence score
- **Decision Agent**: Generates next steps

### Error Handling
- **LLMError**: LLM-related errors
- **RAGError**: RAG-related errors
- **UFACError**: Assessment failures
- **Graceful Degradation**: System continues despite failures

### Logging
- **DEBUG**: Detailed information for debugging
- **INFO**: General information (default)
- **WARNING**: Potential issues
- **ERROR**: Failures that need attention

---

## Common Tasks

### Start the Server
```bash
python -m uvicorn api.app:app --reload
```

### Run Setup
```bash
python setup_rag.py
```

### Check Health
```bash
curl http://localhost:8000/health | jq
```

### Check RAG Status
```bash
curl http://localhost:8000/rag-status | jq
```

### Test Eligibility Check
```bash
curl -X POST http://localhost:8000/check \
  -H "Content-Type: application/json" \
  -d '{"occupation": "farmer", "land_ownership": "yes"}'
```

### Enable Debug Logging
```bash
export LOG_LEVEL=DEBUG
python -m uvicorn api.app:app --reload
```

---

## File Organization

```
UFAC Engine/
├── README.md                          # Project overview
├── SETUP_GUIDE.md                     # Setup instructions
├── PROGRESS_REPORT.md                 # Progress tracking
├── DOCUMENTATION_INDEX.md             # This file
│
├── PRIORITY_A_SUMMARY.md              # RAG Caching
├── PRIORITY_B_SUMMARY.md              # RAG Validation
├── PRIORITY_C_SUMMARY.md              # UI React Flow
├── PRIORITY_D_SUMMARY.md              # Error Handling
├── ERROR_HANDLING_GUIDE.md            # Error handling reference
├── PRIORITY_D_CHANGES.md              # Detailed changes
├── COMPLETION_PRIORITY_D.md           # Completion report
│
├── .env.example                       # Environment template
├── requirements.txt                   # Python dependencies
│
├── core/                              # Backend agents
│   ├── ufac_engine.py                # Main engine
│   ├── fact_agent.py                 # Fact agent
│   ├── assumption_agent.py           # Assumption agent
│   ├── unknown_agent.py              # Unknown agent
│   ├── confidence_agent.py           # Confidence agent
│   ├── decision_agent.py             # Decision agent
│   ├── llm_utils.py                  # LLM utilities
│   └── schema.py                     # Data schemas
│
├── data/                              # Data & RAG
│   ├── rag_pipeline.py               # RAG pipeline
│   ├── pm_kisan_rules.py             # PM-KISAN rules
│   ├── *.pdf                         # PDF documents
│   └── chroma_db/                    # ChromaDB storage
│
├── api/                               # FastAPI
│   └── app.py                        # Main API
│
├── UI/                                # React frontend
│   ├── app/                          # Next.js app
│   ├── components/                   # React components
│   ├── hooks/                        # React hooks
│   ├── lib/                          # Utilities
│   └── package.json                  # Dependencies
│
└── Extra Files/                       # Additional documentation
    ├── START_HERE.md
    ├── GETTING_STARTED.md
    ├── PROJECT_STRUCTURE.md
    └── ...
```

---

## Documentation Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| README.md | ✅ Current | March 2026 |
| SETUP_GUIDE.md | ✅ Current | March 2026 |
| PROGRESS_REPORT.md | ✅ Current | March 20, 2026 |
| PRIORITY_A_SUMMARY.md | ✅ Complete | March 2026 |
| PRIORITY_B_SUMMARY.md | ✅ Complete | March 2026 |
| PRIORITY_C_SUMMARY.md | ✅ Complete | March 2026 |
| PRIORITY_D_SUMMARY.md | ✅ Complete | March 20, 2026 |
| ERROR_HANDLING_GUIDE.md | ✅ Complete | March 20, 2026 |
| DEPLOYMENT.md | ⏳ In Progress | - |

---

## Getting Help

### For Setup Issues
- Read `SETUP_GUIDE.md`
- Check `.env.example` for configuration
- Run `python setup_rag.py` for RAG setup

### For Error Debugging
- Read `ERROR_HANDLING_GUIDE.md`
- Check logs with `tail -f app.log`
- Enable debug logging with `LOG_LEVEL=DEBUG`

### For Architecture Questions
- Read `PRIORITY_C_SUMMARY.md` for UI architecture
- Read `core/ufac_engine.py` for agent architecture
- Read `PRIORITY_A_SUMMARY.md` for RAG architecture

### For API Usage
- Check `/docs` endpoint (Swagger UI)
- Check `/redoc` endpoint (ReDoc)
- Read `PRIORITY_D_SUMMARY.md` for error handling

---

## Contributing

When adding new documentation:
1. Follow the existing format
2. Include code examples where relevant
3. Add to this index
4. Update PROGRESS_REPORT.md if needed

---

## Summary

This documentation provides comprehensive coverage of:
- ✅ Project setup and installation
- ✅ Architecture and design
- ✅ API endpoints and usage
- ✅ Error handling and debugging
- ✅ Progress tracking
- ✅ Deployment guide (in progress)

For any questions, refer to the appropriate documentation file above.

---

*Last updated: March 20, 2026*  
*UFAC Engine v2.0 - Documentation Index*
