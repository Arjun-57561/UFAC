# Napkin AI Flowchart Prompt - UFAC Engine Architecture

## Detailed Prompt for Napkin AI

```
Create a comprehensive flowchart for the UFAC Engine (Unknown-Fact-Assumption-Confidence) 
PM-KISAN Eligibility Assessment System. The flowchart should show the complete data flow 
and processing pipeline.

SYSTEM OVERVIEW:
The UFAC Engine is a FastAPI-based eligibility assessment system that uses 5 AI agents 
working in parallel batches to evaluate PM-KISAN (Pradhan Mantri Kisan Samman Nidhi) 
scheme eligibility.

FLOWCHART REQUIREMENTS:

1. START POINT:
   - User submits eligibility check request via POST /check endpoint
   - Request contains user data (occupation, land ownership, Aadhaar status, etc.)

2. CACHE CHECK (First Decision Diamond):
   - Check if identical request exists in Assessment Cache
   - If HIT: Return cached result immediately (0.1s response)
   - If MISS: Continue to processing

3. BATCH 1 - PARALLEL PROCESSING (3 Agents):
   Show these 3 agents running in parallel:
   
   a) FACT AGENT:
      - Input: User data
      - Process: Extract confirmed, objective facts
      - RAG Retrieval: Query cached retriever for PM-KISAN facts
      - Output: List of facts + consensus score
   
   b) ASSUMPTION AGENT:
      - Input: User data
      - Process: Identify implicit assumptions
      - RAG Retrieval: Query for assumption-related guidelines
      - Output: List of assumptions + consensus score
   
   c) UNKNOWN AGENT:
      - Input: User data + PM-KISAN rules
      - Process: Detect missing critical information
      - RAG Retrieval: Query for required documents/verifications
      - Output: List of unknowns + consensus score

4. BATCH 2 - PARALLEL PROCESSING (2 Agents):
   Show these 2 agents running in parallel (after Batch 1 completes):
   
   a) CONFIDENCE AGENT:
      - Input: Known facts + Unknowns from Batch 1
      - Process: Calculate confidence score (0-100)
      - Logic: Start at 100, subtract for unknowns, add for facts
      - Output: Confidence score (0-100) + consensus
   
   b) DECISION AGENT:
      - Input: Unknowns from Batch 1
      - Process: Generate actionable next steps
      - RAG Retrieval: Query for application process steps
      - Output: List of next steps + consensus

5. ANSWER DETERMINATION:
   - Input: Confidence score, unknowns, known facts
   - Decision Logic (show as nested if-else):
     * If confidence >= 80 AND unknowns == 0: "Likely ELIGIBLE"
     * Else if confidence >= 65 AND unknowns <= 2: "Possibly eligible"
     * Else if "e-KYC" or "Aadhaar" in unknowns: "Cannot confirm - e-KYC missing"
     * Else if "land" in unknowns: "Cannot confirm - land not verified"
     * Else: "Cannot confirm - too many unknowns"
   - Also check for disqualifiers in facts: "Likely INELIGIBLE"

6. RISK LEVEL ASSIGNMENT:
   - If confidence < 40: HIGH risk
   - If confidence 40-70: MEDIUM risk
   - If confidence >= 70: LOW risk

7. RESPONSE ASSEMBLY:
   - Combine all results into UFACResponse object:
     * answer (string)
     * confidence (0-100)
     * known_facts (list)
     * assumptions (list)
     * unknowns (list)
     * risk_level (LOW/MEDIUM/HIGH)
     * next_steps (list)
     * All 5 agent consensus scores

8. CACHE STORAGE:
   - Store response in Assessment Cache (TTL: 1 hour)

9. END POINT:
   - Return UFACResponse to user
   - Response time: 8-10 seconds (first request) or 0.1s (cached)

SUPPORTING SYSTEMS (Show as side boxes):

A) RAG PIPELINE (Retrieval-Augmented Generation):
   - Input: Query string
   - Process: Singleton retriever with caching
   - ChromaDB: Vector database with PM-KISAN PDFs
   - Output: Top 4 relevant document chunks
   - Cache: 2-hour TTL for RAG results

B) CACHING LAYER:
   - Assessment Cache: 1 hour TTL
   - RAG Cache: 2 hour TTL
   - LLM Cache: 1 hour TTL
   - Shows cache hit/miss statistics

C) ERROR HANDLING:
   - Show graceful fallbacks:
     * If RAG fails: Use empty context (hardcoded rules)
     * If any agent fails: Use default values
     * If LLM fails: Return 503 Service Unavailable

D) MONITORING:
   - Metrics collection (requests, latency, errors)
   - Cache statistics
   - Agent performance tracking

VISUAL STYLE REQUIREMENTS:
- Use clear rectangular boxes for processes
- Use diamond shapes for decision points
- Use parallelogram shapes for input/output
- Use different colors for:
  * Blue: API endpoints
  * Green: Processing agents
  * Yellow: Cache operations
  * Red: Error handling
  * Purple: RAG pipeline
- Use arrows to show data flow
- Label all arrows with data type/description
- Show parallel processes side-by-side with synchronization point
- Include timing information (0.1s for cache, 8-10s for full processing)

LAYOUT PREFERENCE:
- Top to bottom main flow
- Batch 1 agents side-by-side in middle
- Batch 2 agents side-by-side below Batch 1
- Supporting systems (RAG, Cache, Monitoring) as side panels
- Clear separation between request processing and response generation

ANNOTATIONS TO INCLUDE:
- "Parallel Execution" labels on Batch 1 and Batch 2
- "Cached Retriever" label on RAG pipeline
- "TTL: 1 hour" on cache boxes
- "Consensus Score" on agent outputs
- "Graceful Fallback" on error paths
- Performance metrics (0.1s vs 8-10s)

EXAMPLE DATA FLOW LABELS:
- "User Data (occupation, land, Aadhaar, etc.)"
- "PM-KISAN Rules & Requirements"
- "RAG Query Results (top 4 chunks)"
- "Confidence Score (0-100)"
- "Risk Level (LOW/MEDIUM/HIGH)"
- "UFACResponse Object"

Make the flowchart professional, clear, and suitable for:
- Technical documentation
- Architecture presentations
- Developer onboarding
- System design reviews
```

---

## Alternative Simplified Prompt (If you want a simpler version)

```
Create a flowchart for the UFAC Engine PM-KISAN Eligibility Assessment System.

MAIN FLOW:
1. User submits request → Check cache
2. If cached: Return result (0.1s)
3. If not cached: Run 5 agents in 2 parallel batches
   - Batch 1 (parallel): Fact Agent, Assumption Agent, Unknown Agent
   - Batch 2 (parallel): Confidence Agent, Decision Agent
4. Determine eligibility answer based on confidence and unknowns
5. Assign risk level (LOW/MEDIUM/HIGH)
6. Cache result and return response (8-10s total)

SUPPORTING SYSTEMS:
- RAG Pipeline: Retrieves PM-KISAN guidelines from ChromaDB
- Caching Layer: Stores assessments, RAG results, LLM responses
- Error Handling: Graceful fallbacks if any component fails

VISUAL STYLE:
- Clear boxes for processes
- Diamonds for decisions
- Different colors for different components
- Show parallel execution clearly
- Include timing information
```

---

## How to Use This Prompt in Napkin AI

1. **Go to**: https://www.napkin.ai/
2. **Click**: "Create New Diagram"
3. **Select**: "Flowchart" template
4. **Paste**: The detailed prompt above into the text input
5. **Click**: "Generate" or "Create"
6. **Refine**: Use Napkin AI's editor to adjust colors, layout, and labels

---

## Expected Flowchart Output

The flowchart should show:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REQUEST                             │
│         POST /check with user data                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │  Check Cache   │
            └────┬───────┬───┘
                 │       │
            HIT  │       │  MISS
                 ▼       ▼
            ┌────────┐  ┌──────────────────────────────┐
            │Return  │  │  BATCH 1: Parallel Agents   │
            │Cached  │  │  ┌──────┬──────┬──────┐     │
            │Result  │  │  │Fact  │Assume│Unknown│    │
            │(0.1s)  │  │  │Agent │Agent │Agent │    │
            └────────┘  │  └──────┴──────┴──────┘     │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │  BATCH 2: Parallel Agents   │
                        │  ┌──────────┬──────────┐    │
                        │  │Confidence│Decision  │    │
                        │  │Agent     │Agent     │    │
                        │  └──────────┴──────────┘    │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │ Determine Answer & Risk      │
                        │ (Based on confidence score)  │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │ Cache Result (TTL: 1 hour)   │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │ Return UFACResponse (8-10s)  │
                        └──────────────────────────────┘
```

---

## Key Points for Napkin AI

- **Emphasize parallelization**: Batch 1 and Batch 2 run in parallel
- **Show caching benefit**: 0.1s vs 8-10s response times
- **Include RAG pipeline**: Shows how PM-KISAN guidelines are retrieved
- **Error handling paths**: Show graceful degradation
- **Color coding**: Different colors for different system components
- **Consensus scores**: Show that each agent produces a consensus score
- **Risk levels**: Show the mapping from confidence to risk

This prompt will generate a professional, clear flowchart suitable for documentation and presentations.
