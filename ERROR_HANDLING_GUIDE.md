# Error Handling & Logging Guide

**File**: `ERROR_HANDLING_GUIDE.md`

Quick reference for understanding and debugging the UFAC Engine error handling system.

---

## Exception Hierarchy

### LLM Errors (`core/llm_utils.py`)

```
LLMError (base)
├── LLMInitializationError
│   └── Raised when: GROQ_API_KEY not set or Groq client creation fails
│   └── HTTP Status: 503 Service Unavailable
│   └── Example: "GROQ_API_KEY environment variable not set"
│
└── LLMCallError
    └── Raised when: API call fails, timeout, or invalid response
    └── HTTP Status: 503 Service Unavailable
    └── Example: "API call failed: Connection timeout"
```

### RAG Errors (`data/rag_pipeline.py`)

```
RAGError (base)
├── RAGInitializationError
│   └── Raised when: ChromaDB setup fails, PDFs missing, embeddings fail
│   └── HTTP Status: 500 Internal Server Error
│   └── Example: "No PDF files found in /path/to/data"
│
└── RAGRetrievalError
    └── Raised when: Document retrieval fails
    └── HTTP Status: 500 Internal Server Error
    └── Example: "Failed to retrieve documents from ChromaDB"
```

### UFAC Errors (`core/ufac_engine.py`)

```
UFACError (base)
└── Raised when: Assessment fails after all retries
    └── HTTP Status: 500 Internal Server Error
    └── Example: "Assessment failed: All agents returned empty results"
```

---

## Error Handling Patterns

### Pattern 1: Initialization Errors

**Location**: `api/app.py` lifespan startup

```python
try:
    init_gemini()
    logger.info("✅ Groq API initialized successfully")
except LLMInitializationError as e:
    logger.error(f"❌ Failed to initialize Groq API: {str(e)}")
    raise  # Fail fast on initialization
```

**Behavior**: Startup fails if Groq API cannot be initialized

**Recovery**: User must fix `.env` file and restart

---

### Pattern 2: Graceful Degradation

**Location**: `api/app.py` lifespan startup

```python
try:
    logger.info("Initializing RAG pipeline...")
    retriever = get_retriever()
    status = get_vectorstore_status()
except RAGError as e:
    logger.warning(f"⚠️  RAG pipeline initialization failed: {str(e)}")
    logger.info("Continuing without RAG (using hardcoded rules)")
    rag_status["error"] = str(e)
```

**Behavior**: Startup continues even if RAG fails

**Recovery**: System uses hardcoded PM-KISAN rules instead of RAG context

---

### Pattern 3: Batch Execution with Fallbacks

**Location**: `core/ufac_engine.py`

```python
fact_result, assumption_result, unknown_result = await asyncio.gather(
    extract_known_facts(user_data),
    detect_assumptions(user_data),
    detect_unknowns(user_data, PM_KISAN_RULES),
    return_exceptions=True  # Don't fail entire batch
)

# Handle individual exceptions
if isinstance(fact_result, Exception):
    logger.error(f"Fact agent failed: {str(fact_result)}")
    fact_result = {"facts": [], "consensus": 0.0}  # Graceful fallback
```

**Behavior**: If one agent fails, others continue and failed agent returns empty result

**Recovery**: Assessment completes with partial data from working agents

---

### Pattern 4: Request/Response Logging

**Location**: `api/app.py` middleware

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

**Behavior**: All requests logged with ID, method, path, status, and duration

**Recovery**: Errors logged with full stack trace for debugging

---

## Logging Levels

### DEBUG
**When**: Development and troubleshooting

**Examples**:
```
DEBUG - Using cached retriever
DEBUG - Run 1 attempt 1/2
DEBUG - Successfully extracted JSON from code block
```

**Enable**: Set `LOG_LEVEL=DEBUG` in `.env`

---

### INFO
**When**: Normal operation (default)

**Examples**:
```
INFO - ✅ Groq API initialized successfully
INFO - ✅ RAG pipeline ready: 1250 chunks indexed
INFO - [req-12345] POST /check
INFO - UFAC assessment completed: confidence=75, risk=LOW
```

**Enable**: Default level

---

### WARNING
**When**: Potential issues that don't stop execution

**Examples**:
```
WARNING - ⚠️  RAG initialized but no chunks found
WARNING - ⚠️  RAG pipeline initialization failed: No PDF files found
WARNING - Run 1 attempt 1 timed out after 15s
```

**Action**: Check configuration or data

---

### ERROR
**When**: Failures that need attention

**Examples**:
```
ERROR - GROQ_API_KEY environment variable not set
ERROR - Fact agent failed: LLMCallError('API call failed: Connection timeout')
ERROR - [req-12346] Request failed: UFACError('Assessment failed: ...')
```

**Action**: Fix the issue and restart

---

## Common Error Scenarios

### Scenario 1: Missing GROQ_API_KEY

**Error**:
```
ERROR - GROQ_API_KEY environment variable not set. Please add it to .env file.
ERROR - Failed to initialize Groq API: GROQ_API_KEY environment variable not set...
```

**Fix**:
```bash
# Add to .env
GROQ_API_KEY=your_groq_api_key_here

# Restart
python -m uvicorn api.app:app --reload
```

---

### Scenario 2: Missing PDF Files

**Error**:
```
WARNING - ⚠️  No PDF files found in /path/to/data
WARNING - ⚠️  RAG pipeline initialization failed: No PDF files found...
INFO - Continuing without RAG (using hardcoded rules)
```

**Fix**:
```bash
# Add PDF files to data/ directory
cp /path/to/pm_kisan_guidelines.pdf data/

# Rebuild RAG
python setup_rag.py

# Restart
python -m uvicorn api.app:app --reload
```

---

### Scenario 3: LLM API Timeout

**Error**:
```
WARNING - Run 1 attempt 1 timed out after 15s
WARNING - Run 1 attempt 2 timed out after 15s
ERROR - Run 1 failed after 2 attempts
```

**Fix**:
```bash
# Check Groq API status
# Increase timeout in core/llm_utils.py (currently 15s)
# Retry the request

# If persistent, check network connectivity
ping api.groq.com
```

---

### Scenario 4: Agent Failure

**Error**:
```
ERROR - Fact agent failed: LLMCallError('API call failed: ...')
ERROR - Fact agent failed: LLMCallError('API call failed: ...')
INFO - UFAC assessment completed: confidence=50, risk=MEDIUM
```

**Fix**:
```bash
# System gracefully handles this
# Assessment completes with partial data
# Check logs for specific agent error
# Retry the request
```

---

## Debugging Tips

### 1. Enable Debug Logging

```bash
# In .env
LOG_LEVEL=DEBUG

# Or via environment
export LOG_LEVEL=DEBUG
python -m uvicorn api.app:app --reload
```

### 2. Check Request ID

```bash
# Send request with custom ID
curl -X POST http://localhost:8000/check \
  -H "x-request-id: my-test-123" \
  -H "Content-Type: application/json" \
  -d '{"occupation": "farmer"}'

# Find all logs for this request
grep "my-test-123" app.log
```

### 3. Test Individual Components

```bash
# Test Groq API
python -c "from core.llm_utils import init_gemini; init_gemini(); print('✅ Groq API OK')"

# Test RAG
python -c "from data.rag_pipeline import get_retriever; r = get_retriever(); print('✅ RAG OK')"

# Test UFAC engine
python -c "from core.ufac_engine import run_ufac; import asyncio; asyncio.run(run_ufac({'occupation': 'farmer'}))"
```

### 4. Check Health Endpoints

```bash
# Health check
curl http://localhost:8000/health | jq

# RAG status
curl http://localhost:8000/rag-status | jq
```

### 5. Review Error Stack Traces

```bash
# Errors logged with full stack trace
# Look for "Traceback" in logs
# Check the "exc_info=True" logs for full details
```

---

## HTTP Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Assessment completed successfully |
| 400 | Bad Request | Invalid request format |
| 500 | Internal Server Error | UFAC assessment failed |
| 503 | Service Unavailable | LLM API error |

---

## Best Practices

### 1. Always Check Logs

```bash
# Follow logs in real-time
tail -f app.log

# Search for errors
grep ERROR app.log

# Search for specific request
grep "req-12345" app.log
```

### 2. Use Request IDs

```bash
# Send with request
curl -X POST http://localhost:8000/check \
  -H "x-request-id: unique-id" \
  -H "Content-Type: application/json" \
  -d '{...}'

# Track through logs
grep "unique-id" app.log
```

### 3. Monitor Error Rates

```bash
# Count errors per hour
grep ERROR app.log | cut -d' ' -f1-2 | sort | uniq -c

# Count by error type
grep ERROR app.log | grep -o "Error: [^,]*" | sort | uniq -c
```

### 4. Test Error Scenarios

```bash
# Test missing API key
unset GROQ_API_KEY
python -m uvicorn api.app:app --reload

# Test missing PDFs
rm data/*.pdf
python -m uvicorn api.app:app --reload

# Test invalid request
curl -X POST http://localhost:8000/check \
  -H "Content-Type: application/json" \
  -d '{invalid json}'
```

---

## Configuration

### Environment Variables

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
DEV_MODE=true   # Reduces LLM calls from 3 to 1
```

### Logging Configuration

**File**: `api/app.py`

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## Summary

The UFAC Engine error handling system provides:

✅ **Clear error messages** with actionable guidance  
✅ **Graceful degradation** when components fail  
✅ **Comprehensive logging** for debugging  
✅ **Request tracking** with unique IDs  
✅ **Structured exceptions** for different error types  
✅ **Retry logic** with exponential backoff  
✅ **Fallback mechanisms** for failed agents  

This ensures the system is resilient, maintainable, and easy to debug.

---

*Last updated: March 20, 2026*
*UFAC Engine v2.0 - Error Handling & Logging Guide*
