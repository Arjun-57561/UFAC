# Priority D - Error Handling & Logging Implementation

**Status**: ✅ COMPLETED

**Estimated Effort**: 1-2 hours  
**Actual Effort**: Completed  
**Date**: March 20, 2026

---

## Overview

Implemented comprehensive error handling and structured logging across the entire UFAC Engine. This ensures better debugging, graceful degradation, and clear error messages for users and developers.

---

## Key Improvements

### 1. Custom Exception Hierarchy

Created specific exception classes for better error categorization:

**LLM Errors** (`core/llm_utils.py`):
- `LLMError` - Base exception for all LLM-related errors
- `LLMInitializationError` - Raised when Groq API initialization fails
- `LLMCallError` - Raised when an LLM API call fails

**RAG Errors** (`data/rag_pipeline.py`):
- `RAGError` - Base exception for all RAG-related errors
- `RAGInitializationError` - Raised when RAG initialization fails
- `RAGRetrievalError` - Raised when document retrieval fails

**UFAC Errors** (`core/ufac_engine.py`):
- `UFACError` - Base exception for UFAC assessment failures

### 2. Enhanced LLM Error Handling

**File**: `core/llm_utils.py`

```python
# Better initialization error messages
def init_gemini():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        error_msg = "GROQ_API_KEY environment variable not set. Please add it to .env file."
        logger.error(error_msg)
        raise LLMInitializationError(error_msg)
```

**Features**:
- Clear error messages with actionable guidance
- Detailed logging with `exc_info=True` for stack traces
- Retry logic with exponential backoff (2 attempts)
- Timeout handling (15 seconds per call)
- JSON parsing with fallback extraction from markdown blocks
- Debug logging for troubleshooting

### 3. Enhanced RAG Error Handling

**File**: `data/rag_pipeline.py`

**Features**:
- Validation of data directory and PDF files
- Detailed error messages for each failure point
- Graceful handling of missing PDFs
- Proper exception propagation with context
- Status checking with error details

```python
# Example: Better error messages
if not pdf_files:
    warning_msg = f"⚠️  No PDF files found in {DATA_DIR}"
    logger.warning(warning_msg)
    raise RAGInitializationError(warning_msg)
```

### 4. UFAC Engine Resilience

**File**: `core/ufac_engine.py`

**Features**:
- Batch execution with `return_exceptions=True`
- Individual agent failure handling
- Graceful fallbacks for failed agents
- Detailed logging of each batch execution
- Comprehensive error propagation

```python
# Batch 1 with exception handling
fact_result, assumption_result, unknown_result = await asyncio.gather(
    extract_known_facts(user_data),
    detect_assumptions(user_data),
    detect_unknowns(user_data, PM_KISAN_RULES),
    return_exceptions=True  # Don't fail entire batch if one agent fails
)

# Handle individual exceptions
if isinstance(fact_result, Exception):
    logger.error(f"Fact agent failed: {str(fact_result)}")
    fact_result = {"facts": [], "consensus": 0.0}  # Graceful fallback
```

### 5. FastAPI Request/Response Logging

**File**: `api/app.py`

**Features**:
- Request ID tracking for tracing
- HTTP middleware for all requests
- Response time measurement
- Status code logging
- Exception logging with stack traces
- Structured logging format

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    request_id = request.headers.get("x-request-id", "unknown")
    
    logger.info(f"[{request_id}] {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"[{request_id}] {response.status_code} - {process_time:.3f}s")
        return response
    except Exception as e:
        logger.error(f"[{request_id}] Request failed: {str(e)}", exc_info=True)
        raise
```

### 6. Enhanced Error Endpoints

**File**: `api/app.py`

**Features**:
- Specific HTTP status codes for different error types
- Detailed error messages
- RAG status endpoint with error details
- Health check with RAG status

```python
@app.post("/check", response_model=UFACResponse)
async def check_eligibility(request: EligibilityCheckRequest):
    try:
        result = await run_ufac(user_data)
        return result
    except UFACError as e:
        logger.error(f"UFAC assessment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")
    except LLMError as e:
        logger.error(f"LLM error: {str(e)}")
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")
```

### 7. Structured Logging Configuration

**File**: `api/app.py`

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Log Levels**:
- `DEBUG` - Detailed information for debugging (cached retriever usage, retry attempts)
- `INFO` - General information (startup, requests, completions)
- `WARNING` - Warning messages (RAG not initialized, missing PDFs)
- `ERROR` - Error messages (API failures, exceptions)

---

## Files Modified

### Backend Files

1. **`core/llm_utils.py`**
   - Added custom exception classes
   - Enhanced error messages
   - Better retry logic with logging
   - Improved JSON parsing with fallbacks

2. **`data/rag_pipeline.py`**
   - Added custom exception classes
   - Validation of data directory and PDFs
   - Detailed error messages
   - Better error propagation

3. **`core/ufac_engine.py`**
   - Added UFACError exception
   - Batch execution with exception handling
   - Graceful fallbacks for failed agents
   - Comprehensive logging

4. **`api/app.py`**
   - Added request/response logging middleware
   - Structured logging configuration
   - Enhanced error handling in endpoints
   - Specific HTTP status codes for different errors
   - Better startup/shutdown logging

5. **`.env.example`**
   - Updated to use GROQ_API_KEY instead of GEMINI_API_KEY
   - Added DEV_MODE configuration option
   - Added logging configuration option

---

## Error Handling Flow

### Initialization Phase

```
FastAPI Startup
  ├─ Initialize Groq API
  │  ├─ Check GROQ_API_KEY env var
  │  ├─ Create Groq client
  │  └─ Log success or raise LLMInitializationError
  │
  └─ Initialize RAG Pipeline
     ├─ Load embeddings model
     ├─ Check ChromaDB exists
     ├─ Load or build vectorstore
     └─ Log status or raise RAGInitializationError
```

### Request Processing Phase

```
POST /check
  ├─ Log request with ID
  ├─ Run UFAC Assessment
  │  ├─ Batch 1 (Fact, Assumption, Unknown)
  │  │  ├─ Execute in parallel with return_exceptions=True
  │  │  ├─ Handle individual exceptions
  │  │  └─ Use graceful fallbacks
  │  │
  │  └─ Batch 2 (Confidence, Decision)
  │     ├─ Execute in parallel with return_exceptions=True
  │     ├─ Handle individual exceptions
  │     └─ Use graceful fallbacks
  │
  ├─ Return response or raise HTTPException
  └─ Log response with status code and duration
```

---

## Logging Examples

### Successful Startup

```
2026-03-20 10:30:45,123 - api.app - INFO - ======================================================================
2026-03-20 10:30:45,124 - api.app - INFO - 🚀 Starting UFAC Engine v2.0...
2026-03-20 10:30:45,125 - api.app - INFO - ======================================================================
2026-03-20 10:30:45,200 - core.llm_utils - INFO - ✅ Groq API initialized successfully with model: llama-3.3-70b-versatile
2026-03-20 10:30:45,201 - api.app - INFO - ✅ Groq API initialized successfully
2026-03-20 10:30:45,202 - api.app - INFO - Initializing RAG pipeline...
2026-03-20 10:30:47,500 - data.rag_pipeline - INFO - Loading SentenceTransformer embeddings model...
2026-03-20 10:30:50,000 - data.rag_pipeline - INFO - ✅ Embeddings model loaded successfully
2026-03-20 10:30:50,100 - data.rag_pipeline - INFO - Loading retriever from ChromaDB...
2026-03-20 10:30:50,200 - data.rag_pipeline - INFO - ✅ Retriever loaded and cached
2026-03-20 10:30:50,300 - api.app - INFO - ✅ RAG pipeline ready: 1250 chunks indexed
2026-03-20 10:30:50,400 - api.app - INFO - ======================================================================
2026-03-20 10:30:50,401 - api.app - INFO - ✅ UFAC Engine ready for requests
2026-03-20 10:30:50,402 - api.app - INFO - ======================================================================
```

### Successful Request

```
2026-03-20 10:31:00,100 - api.app - INFO - [req-12345] POST /check
2026-03-20 10:31:00,101 - api.app - INFO - Processing eligibility check with fields: ['occupation', 'land_ownership', 'aadhaar_linked']
2026-03-20 10:31:00,102 - core.ufac_engine - INFO - Starting UFAC assessment with data: ['occupation', 'land_ownership', 'aadhaar_linked']
2026-03-20 10:31:00,103 - core.ufac_engine - DEBUG - Running Batch 1 agents (Fact, Assumption, Unknown)...
2026-03-20 10:31:05,500 - core.ufac_engine - DEBUG - Running Batch 2 agents (Confidence, Decision)...
2026-03-20 10:31:08,000 - core.ufac_engine - INFO - UFAC assessment completed: confidence=75, risk=LOW
2026-03-20 10:31:08,001 - api.app - INFO - Eligibility check completed: confidence=75, risk=LOW
2026-03-20 10:31:08,002 - api.app - INFO - [req-12345] 200 - 7.902s
```

### Error Handling

```
2026-03-20 10:32:00,100 - api.app - INFO - [req-12346] POST /check
2026-03-20 10:32:00,101 - api.app - INFO - Processing eligibility check with fields: ['occupation']
2026-03-20 10:32:00,102 - core.ufac_engine - INFO - Starting UFAC assessment with data: ['occupation']
2026-03-20 10:32:00,103 - core.ufac_engine - DEBUG - Running Batch 1 agents (Fact, Assumption, Unknown)...
2026-03-20 10:32:02,500 - core.fact_agent - ERROR - Fact agent failed: LLMCallError('API call failed: Connection timeout')
2026-03-20 10:32:02,501 - core.ufac_engine - ERROR - Fact agent failed: LLMCallError('API call failed: Connection timeout')
2026-03-20 10:32:02,502 - core.ufac_engine - DEBUG - Running Batch 2 agents (Confidence, Decision)...
2026-03-20 10:32:05,000 - core.ufac_engine - INFO - UFAC assessment completed: confidence=50, risk=MEDIUM
2026-03-20 10:32:05,001 - api.app - INFO - [req-12346] 200 - 4.900s
```

---

## Testing Error Handling

### Test 1: Missing GROQ_API_KEY

```bash
# Remove GROQ_API_KEY from .env
unset GROQ_API_KEY
python -m uvicorn api.app:app --reload
```

**Expected Output**:
```
ERROR - GROQ_API_KEY environment variable not set. Please add it to .env file.
ERROR - Failed to initialize Groq API: GROQ_API_KEY environment variable not set...
```

### Test 2: Missing PDF Files

```bash
# Remove all PDFs from data/ directory
rm data/*.pdf
python -m uvicorn api.app:app --reload
```

**Expected Output**:
```
WARNING - ⚠️  No PDF files found in /path/to/data
WARNING - ⚠️  RAG pipeline initialization failed: No PDF files found...
INFO - Continuing without RAG (using hardcoded rules)
```

### Test 3: Agent Failure Handling

```bash
# Simulate agent failure by temporarily breaking an agent
# The system should gracefully handle it and continue
curl -X POST http://localhost:8000/check \
  -H "Content-Type: application/json" \
  -d '{"occupation": "farmer", "land_ownership": "yes"}'
```

**Expected Output**:
```
INFO - Processing eligibility check with fields: ['occupation', 'land_ownership']
INFO - UFAC assessment completed: confidence=75, risk=LOW
```

---

## Configuration

### Environment Variables

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
DEV_MODE=true  # Reduces LLM calls from 3 to 1 for faster testing
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

### Logging Levels

- **DEBUG**: Detailed information for debugging (use for development)
- **INFO**: General information (default for production)
- **WARNING**: Warning messages (RAG issues, missing data)
- **ERROR**: Error messages (failures, exceptions)

---

## Next Steps

### Priority E - Caching Layer (2-3 hours)

- Implement request-level caching for identical assessments
- Add Redis support for distributed caching
- Cache RAG retrieval results
- Cache LLM responses for common queries

### Priority F - Testing Suite (3-4 hours)

- Unit tests for each agent
- Integration tests for UFAC engine
- API endpoint tests
- Error handling tests
- Performance benchmarks

### Priority G - Monitoring (2-3 hours)

- Prometheus metrics
- Request latency tracking
- Error rate monitoring
- RAG performance metrics
- LLM API usage tracking

### Priority H - Deployment (2-3 hours)

- Docker containerization
- Kubernetes deployment
- CI/CD pipeline
- Production configuration
- Monitoring and alerting

---

## Summary

Priority D successfully implements comprehensive error handling and structured logging across the UFAC Engine. The system now:

✅ Provides clear, actionable error messages  
✅ Gracefully handles failures with fallbacks  
✅ Logs all requests and responses with timing  
✅ Tracks errors with full stack traces  
✅ Supports debugging with debug-level logging  
✅ Maintains service availability despite individual component failures  

The error handling ensures that the system is resilient and maintainable, making it easier to debug issues and understand system behavior in production.
