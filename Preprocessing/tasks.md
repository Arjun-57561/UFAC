# Implementation Plan: UFAC Engine

## Overview

This implementation plan breaks down the UFAC Engine into discrete coding tasks following the architecture: Core Data Models → LLM Utilities → Ingestion Pipeline → Vector Store & RAG → Agent Orchestration → Watcher Service → REST API → Testing. Each task builds incrementally, with property-based tests integrated throughout to catch errors early.

## Tasks

- [ ] 1. Set up project structure and core data models
  - Create directory structure: `ufac_engine/`, `tests/unit/`, `tests/property/`, `tests/fixtures/`
  - Create `pyproject.toml` with dependencies: google-generativeai, chromadb, pymupdf, pdfplumber, beautifulsoup4, feedparser, datasets, fastapi, pydantic>=2.0, hypothesis, pytest
  - Implement Pydantic v2 data models in `ufac_engine/models.py`: SourceType, StructuredScheme, UserProfile, SchemeChunk, MetadataFilters, Fact, Assumption, MissingInfo, Revision, SchemeMatch, ConfidenceScore, NextSteps, SafetyFlag, ResponseMetadata, Change, ChangeReport, SchemeVersion
  - Implement logging models: AgentLog, CouncilLog, RAGLog, CriticLog
  - Implement configuration models: SystemConfig, IngestionConfig
  - _Requirements: 6.1, 6.2, 6.3_

- [ ]* 1.1 Write property test for schema validation
  - **Property 11: Schema Validation**
  - **Validates: Requirements 6.2, 6.3, 6.4**

- [ ] 2. Implement LLM utilities and Inner Council
  - Create `ufac_engine/llm/gemini_client.py` with GeminiClient class for API calls
  - Implement retry logic with exponential backoff for rate limiting
  - Implement circuit breaker pattern (10 failures in 1 min → 5 min cooldown)
  - Create `ufac_engine/llm/inner_council.py` with InnerCouncil class
  - Implement parallel execution of 3 Gemini calls using asyncio
  - Implement consensus voting: majority vote, or highest confidence if all differ
  - Implement disagreement logging to CouncilLog
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ]* 2.1 Write property test for Inner Council consensus
  - **Property 25: Inner Council Consensus**
  - **Validates: Requirements 11.1, 11.2, 11.3, 11.4**

- [ ]* 2.2 Write property test for council disagreement logging
  - **Property 26: Council Disagreement Logging**
  - **Validates: Requirements 11.5**

- [ ] 3. Implement PDF parser with fallback strategy
  - Create `ufac_engine/ingestion/pdf_parser.py` with PDFParser class
  - Implement primary extraction using pymupdf
  - Implement fallback to pdfplumber if < 100 chars extracted
  - Implement scanned PDF detection (check if text extraction yields < 50 chars)
  - Implement table extraction using pdfplumber
  - Implement URL download support with retry logic (3 attempts)
  - Handle corrupted PDFs with descriptive error messages
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 26.1, 26.2, 26.3, 26.4_

- [ ]* 3.1 Write property test for PDF text extraction
  - **Property 1: PDF Text Extraction**
  - **Validates: Requirements 1.1, 1.2**

- [ ]* 3.2 Write property test for PDF error handling
  - **Property 2: PDF Error Handling**
  - **Validates: Requirements 1.3**

- [ ]* 3.3 Write property test for PDF structure preservation
  - **Property 3: PDF Structure Preservation**
  - **Validates: Requirements 1.4**

- [ ]* 3.4 Write property test for PDF parser fallback strategy
  - **Property 49: PDF Parser Fallback Strategy**
  - **Validates: Requirements 26.1, 26.2**

- [ ]* 3.5 Write property test for scanned PDF detection
  - **Property 50: Scanned PDF Detection**
  - **Validates: Requirements 26.3**

- [ ]* 3.6 Write property test for table structure preservation
  - **Property 51: Table Structure Preservation**
  - **Validates: Requirements 26.4**

- [ ]* 3.7 Write property test for PDF round-trip
  - **Property 52: PDF Round-Trip**
  - **Validates: Requirements 26.5**

- [ ] 4. Implement REST API client for government portals
  - Create `ufac_engine/ingestion/api_client.py` with APIClient class
  - Implement myscheme.gov.in API integration
  - Implement data.gov.in API integration
  - Implement exponential backoff retry (3 attempts: 2s, 4s, 8s)
  - Handle invalid JSON responses with error logging
  - Handle rate limiting (429) with exponential backoff + jitter
  - Handle authentication errors (401/403) with critical logging
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ]* 4.1 Write property test for API retry with exponential backoff
  - **Property 6: API Retry with Exponential Backoff**
  - **Validates: Requirements 2.3, 4.4**

- [ ]* 4.2 Write property test for invalid JSON handling
  - **Property 7: Invalid JSON Handling**
  - **Validates: Requirements 2.4**

- [ ] 5. Implement HTML scraper
  - Create `ufac_engine/ingestion/html_scraper.py` with HTMLScraper class
  - Implement beautifulsoup4-based content extraction
  - Remove navigation, headers, footers, ads using CSS selectors
  - Preserve scheme titles, descriptions, eligibility, links
  - Detect JavaScript-required pages (check for empty content after parsing)
  - Implement network timeout handling with 3 retries
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ]* 5.1 Write property test for HTML content cleaning
  - **Property 8: HTML Content Cleaning**
  - **Validates: Requirements 3.2, 3.3**

- [ ]* 5.2 Write property test for JavaScript page detection
  - **Property 9: JavaScript Page Detection**
  - **Validates: Requirements 3.4**

- [ ] 6. Implement HuggingFace dataset loader
  - Create `ufac_engine/ingestion/hf_loader.py` with HFDatasetLoader class
  - Load shrijayan/gov_myscheme dataset using datasets library
  - Filter for agriculture-related schemes using keywords
  - Implement retry logic (3 attempts) for download failures
  - _Requirements: 4.1, 4.2, 4.4_

- [ ] 7. Implement RSS feed monitor
  - Create `ufac_engine/ingestion/rss_monitor.py` with RSSMonitor class
  - Fetch PIB agriculture RSS feed using feedparser
  - Filter entries by keywords: scheme, agriculture, farmer, PM-KISAN, PMFBY
  - Extract announcement text and metadata
  - _Requirements: 5.1, 5.2, 5.3_

- [ ]* 7.1 Write property test for agriculture scheme filtering
  - **Property 10: Agriculture Scheme Filtering**
  - **Validates: Requirements 4.2, 5.2**

- [ ] 8. Implement data extractor and ingestion orchestration
  - Create `ufac_engine/ingestion/data_extractor.py` with DataExtractor class
  - Implement conversion from all source formats to StructuredScheme
  - Implement schema validation using Pydantic
  - Assign unique scheme_id using UUID
  - Add metadata: source_type, timestamp, document_hash (SHA-256)
  - Create `ufac_engine/ingestion/ingestion_module.py` with IngestionModule class
  - Implement source router to dispatch to appropriate parser
  - Implement pretty_print function for human-readable output
  - _Requirements: 1.5, 1.6, 2.5, 2.6, 3.5, 3.6, 4.3, 4.5, 5.4, 5.5, 6.5, 27.1, 27.2, 27.3, 27.4_

- [ ]* 8.1 Write property test for unified JSON conversion
  - **Property 4: Unified JSON Conversion**
  - **Validates: Requirements 1.5, 2.5, 3.5, 4.3, 5.4**

- [ ]* 8.2 Write property test for metadata completeness
  - **Property 5: Metadata Completeness**
  - **Validates: Requirements 1.6, 2.6, 3.6, 4.5, 5.5**

- [ ]* 8.3 Write property test for unique scheme ID assignment
  - **Property 12: Unique Scheme ID Assignment**
  - **Validates: Requirements 6.5**

- [ ]* 8.4 Write property test for pretty-print content completeness
  - **Property 53: Pretty-Print Content Completeness**
  - **Validates: Requirements 27.2, 27.3, 27.4**

- [ ]* 8.5 Write property test for JSON round-trip
  - **Property 54: JSON Round-Trip**
  - **Validates: Requirements 27.5**

- [ ] 9. Checkpoint - Ensure ingestion pipeline tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Implement embedding model and vector store
  - Create `ufac_engine/vector_store/embedding_model.py` with EmbeddingModel class
  - Generate embeddings using sentence-transformers or Gemini embedding API
  - Implement document chunking (512 tokens max per chunk)
  - Create `ufac_engine/vector_store/vector_store.py` with VectorStore class wrapping ChromaDB
  - Implement add_scheme with embeddings and metadata
  - Implement query with metadata filtering (state, income_range, land_range, scheme_type)
  - Implement get_versions for temporal queries
  - Implement archive_version for versioning
  - Implement persist for disk storage
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [ ]* 10.1 Write property test for embedding generation
  - **Property 13: Embedding Generation**
  - **Validates: Requirements 7.1**

- [ ]* 10.2 Write property test for embedding storage with metadata
  - **Property 14: Embedding Storage with Metadata**
  - **Validates: Requirements 7.2, 7.3**

- [ ]* 10.3 Write property test for document chunking
  - **Property 15: Document Chunking**
  - **Validates: Requirements 7.4**

- [ ]* 10.4 Write property test for vector store round-trip
  - **Property 16: Vector Store Round-Trip**
  - **Validates: Requirements 7.5**

- [ ]* 10.5 Write property test for vector store persistence
  - **Property 17: Vector Store Persistence**
  - **Validates: Requirements 7.6**

- [ ] 11. Implement RAG system
  - Create `ufac_engine/rag/rag_system.py` with RAGSystem class
  - Implement generate_query to convert UserProfile to search query
  - Implement apply_filters to build MetadataFilters from UserProfile
  - Implement retrieve to get top-10 chunks with similarity > 0.6
  - Implement rank_results combining semantic + metadata scores
  - Implement broadening logic if < 3 chunks retrieved
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 29.1, 29.2, 29.3, 29.4, 29.5_

- [ ]* 11.1 Write property test for user profile extraction
  - **Property 18: User Profile Extraction**
  - **Validates: Requirements 8.1, 8.4, 8.5**

- [ ]* 11.2 Write property test for multilingual query support
  - **Property 19: Multilingual Query Support**
  - **Validates: Requirements 8.2**

- [ ]* 11.3 Write property test for RAG query generation and retrieval
  - **Property 20: RAG Query Generation and Retrieval**
  - **Validates: Requirements 9.1, 9.2, 9.3, 9.4**

- [ ]* 11.4 Write property test for metadata-based filtering
  - **Property 21: Metadata-Based Filtering**
  - **Validates: Requirements 29.1, 29.2, 29.3, 29.4**

- [ ]* 11.5 Write property test for combined ranking
  - **Property 22: Combined Ranking**
  - **Validates: Requirements 29.5**

- [ ] 12. Checkpoint - Ensure vector store and RAG tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 13. Implement base agent class
  - Create `ufac_engine/agents/base_agent.py` with BaseAgent abstract class
  - Define abstract process method
  - Implement invoke_with_consensus using InnerCouncil
  - Implement error handling for agent exceptions
  - _Requirements: 25.4_

- [ ] 14. Implement Planner Agent
  - Create `ufac_engine/agents/planner_agent.py` with PlannerAgent class
  - Implement extract_profile to parse natural language queries (English/Hindi)
  - Implement value normalization (acres, state codes, income)
  - Implement route_agents to determine agent execution order
  - Store extracted UserProfile for downstream agents
  - _Requirements: 8.1, 8.2, 8.4, 8.5, 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ]* 14.1 Write property test for agent routing
  - **Property 23: Agent Routing**
  - **Validates: Requirements 10.1, 10.4**

- [ ]* 14.2 Write property test for agent data flow
  - **Property 24: Agent Data Flow**
  - **Validates: Requirements 10.5**

- [ ] 15. Implement Fact Agent
  - Create `ufac_engine/agents/fact_agent.py` with FactAgent class
  - Extract explicitly stated facts from UserProfile
  - Distinguish stated vs inferred facts
  - Return facts with source references
  - Flag contradictions between user facts and scheme requirements
  - _Requirements: 12.1, 12.2, 12.3, 12.4_

- [ ]* 15.1 Write property test for fact extraction and classification
  - **Property 27: Fact Extraction and Classification**
  - **Validates: Requirements 12.1, 12.2, 12.3, 12.4**

- [ ] 16. Implement Assumption Agent
  - Create `ufac_engine/agents/assumption_agent.py` with AssumptionAgent class
  - Identify implicit assumptions in eligibility assessment
  - Categorize: demographic, geographic, temporal, financial
  - Return assumptions with explanations
  - Flag high-risk assumptions
  - _Requirements: 13.1, 13.2, 13.3, 13.4_

- [ ]* 16.1 Write property test for assumption identification
  - **Property 28: Assumption Identification**
  - **Validates: Requirements 13.1, 13.2, 13.3, 13.4**

- [ ] 17. Implement Unknown Agent
  - Create `ufac_engine/agents/unknown_agent.py` with UnknownAgent class
  - Identify missing required fields from UserProfile
  - Categorize by priority: critical, important, optional
  - Return missing info with explanations
  - Trigger additional RAG queries when critical info missing
  - _Requirements: 8.3, 14.1, 14.2, 14.3, 14.4_

- [ ]* 17.1 Write property test for missing information detection
  - **Property 29: Missing Information Detection**
  - **Validates: Requirements 8.3, 14.1, 14.2, 14.3, 14.4**

- [ ] 18. Implement Temporal Agent
  - Create `ufac_engine/agents/temporal_agent.py` with TemporalAgent class
  - Check for multiple scheme versions in VectorStore
  - Identify most recent version by ingestion_timestamp
  - Flag schemes revised within 90 days
  - Return revision dates and change summaries
  - _Requirements: 15.1, 15.2, 15.3, 15.4_

- [ ]* 18.1 Write property test for temporal version checking
  - **Property 30: Temporal Version Checking**
  - **Validates: Requirements 15.1, 15.2, 15.3, 15.4**

- [ ] 19. Implement Scheme Matcher Agent
  - Create `ufac_engine/agents/scheme_matcher_agent.py` with SchemeMatcherAgent class
  - Calculate eligibility score (0-100) per scheme
  - Base score on: matching criteria count, missing criteria severity, profile completeness
  - Return schemes ranked by score (descending)
  - Include per-criterion match status: met, not met, unknown
  - _Requirements: 16.1, 16.2, 16.3, 16.4_

- [ ]* 19.1 Write property test for eligibility scoring
  - **Property 31: Eligibility Scoring**
  - **Validates: Requirements 16.1, 16.2, 16.3, 16.4**

- [ ] 20. Implement Confidence Agent
  - Create `ufac_engine/agents/confidence_agent.py` with ConfidenceAgent class
  - Calculate calibrated confidence score (0-100) per recommendation
  - Base confidence on: profile completeness, document clarity, council agreement, RAG similarity
  - Reduce confidence by 20 points per critical missing field
  - Reduce confidence by 10 points per high-risk assumption
  - Return confidence with explanatory factors
  - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

- [ ]* 20.1 Write property test for confidence calibration
  - **Property 32: Confidence Calibration**
  - **Validates: Requirements 17.1, 17.2, 17.3, 17.4, 17.5**

- [ ] 21. Implement Decision Agent
  - Create `ufac_engine/agents/decision_agent.py` with DecisionAgent class
  - Generate prioritized next steps per scheme
  - Include: gather documents, visit portals, contact offices, verify eligibility
  - Provide Portal_Links for online applications
  - Estimate time per step
  - Sequence steps logically
  - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

- [ ]* 21.1 Write property test for next steps generation
  - **Property 33: Next Steps Generation**
  - **Validates: Requirements 18.1, 18.2, 18.3, 18.4, 18.5**

- [ ] 22. Implement Critic Agent
  - Create `ufac_engine/agents/critic_agent.py` with CriticAgent class
  - Review all agent outputs for consistency
  - Verify confidence scores align with unknowns/assumptions
  - Check for logical contradictions
  - Set Safety_Flag for concerning recommendations (e.g., high confidence + ineligible)
  - Approve final output or request agent re-processing
  - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5_

- [ ]* 22.1 Write property test for critic review and safety
  - **Property 34: Critic Review and Safety**
  - **Validates: Requirements 19.1, 19.2, 19.3, 19.4, 19.5**

- [ ] 23. Checkpoint - Ensure all agent tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 24. Implement UFAC Engine orchestration
  - Create `ufac_engine/engine.py` with UFACEngine class
  - Wire together: Planner → RAG → Fact → Assumption → Unknown → Temporal → Matcher → Confidence → Decision → Critic
  - Implement graceful degradation (continue if individual agents fail)
  - Return structured response with all required fields
  - Implement query timeout (30s)
  - _Requirements: 20.1, 20.2, 20.3, 20.4, 20.5_

- [ ]* 24.1 Write property test for structured response format
  - **Property 35: Structured Response Format**
  - **Validates: Requirements 20.1, 20.5**

- [ ]* 24.2 Write property test for top-K scheme selection
  - **Property 36: Top-K Scheme Selection**
  - **Validates: Requirements 20.2**

- [ ]* 24.3 Write property test for complete uncertainty reporting
  - **Property 37: Complete Uncertainty Reporting**
  - **Validates: Requirements 20.3**

- [ ]* 24.4 Write property test for global safety flag
  - **Property 38: Global Safety Flag**
  - **Validates: Requirements 20.4**

- [ ]* 24.5 Write property test for agent exception handling
  - **Property 47: Agent Exception Handling**
  - **Validates: Requirements 25.4**

- [ ] 25. Implement Watcher Service
  - Create `ufac_engine/watcher/change_detector.py` with ChangeDetector class
  - Implement calculate_hash using SHA-256
  - Implement detect_changes comparing new vs stored hashes
  - Implement compare_versions identifying changed sections
  - Generate before/after snippets
  - Flag critical changes (eligibility tightened, scheme discontinued)
  - Store change history with temporal metadata
  - Create `ufac_engine/watcher/watcher_service.py` with WatcherService class
  - Implement nightly scheduler (02:00 IST) using APScheduler
  - Implement check_portals for all configured URLs
  - Trigger re-ingestion on hash mismatch
  - _Requirements: 21.1, 21.2, 21.3, 21.4, 21.5, 22.1, 22.2, 22.3, 22.4, 22.5, 23.1, 23.2, 23.3, 23.4, 23.5_

- [ ]* 25.1 Write property test for portal monitoring
  - **Property 39: Portal Monitoring**
  - **Validates: Requirements 21.2, 21.3**

- [ ]* 25.2 Write property test for change detection and re-ingestion
  - **Property 40: Change Detection and Re-ingestion**
  - **Validates: Requirements 21.4, 21.5**

- [ ]* 25.3 Write property test for version comparison
  - **Property 41: Version Comparison**
  - **Validates: Requirements 22.1, 22.2, 22.3, 22.4, 22.5**

- [ ]* 25.4 Write property test for selective re-ingestion with versioning
  - **Property 42: Selective Re-ingestion with Versioning**
  - **Validates: Requirements 23.1, 23.2, 23.3, 23.4**

- [ ] 26. Implement REST API layer
  - Create `ufac_engine/api/app.py` with FastAPI application
  - Define POST /api/v1/query endpoint accepting QueryRequest
  - Implement request validation returning 400 for invalid requests
  - Implement rate limiting middleware (10 req/min per IP) using slowapi
  - Invoke UFACEngine and return QueryResponse
  - Implement error handlers: 503 for Gemini/VectorStore unavailable, 504 for timeout
  - Implement global exception handler (never expose internal errors)
  - Implement query logging with timestamps and response times
  - _Requirements: 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 25.1, 25.2, 25.3, 25.5_

- [ ]* 26.1 Write property test for input validation
  - **Property 43: Input Validation**
  - **Validates: Requirements 24.2**

- [ ]* 26.2 Write property test for engine invocation
  - **Property 44: Engine Invocation**
  - **Validates: Requirements 24.3**

- [ ]* 26.3 Write property test for rate limiting
  - **Property 45: Rate Limiting**
  - **Validates: Requirements 24.4**

- [ ]* 26.4 Write property test for query logging
  - **Property 46: Query Logging**
  - **Validates: Requirements 24.6**

- [ ]* 26.5 Write property test for error message security
  - **Property 48: Error Message Security**
  - **Validates: Requirements 25.5**

- [ ] 27. Implement startup validation and logging
  - Create `ufac_engine/utils/startup_validator.py` with StartupValidator class
  - Validate Gemini API key is set
  - Validate vector store directory exists and is writable
  - Validate required package versions
  - Log descriptive errors and exit with code 1 on failure
  - Create `ufac_engine/utils/logger.py` with structured JSON logging
  - Implement daily log rotation with 30-day retention
  - Implement separate log files: ingestion.log, agents.log, api.log, errors.log
  - Log all agent invocations, council votes, RAG retrievals, critic reviews
  - _Requirements: 28.1, 28.2, 28.3, 28.4, 28.5, 30.1, 30.2, 30.3, 30.4, 30.5_

- [ ]* 27.1 Write property test for startup validation failure handling
  - **Property 55: Startup Validation Failure Handling**
  - **Validates: Requirements 28.4**

- [ ]* 27.2 Write property test for comprehensive logging
  - **Property 56: Comprehensive Logging**
  - **Validates: Requirements 30.1, 30.2, 30.3, 30.4, 30.5**

- [ ] 28. Checkpoint - Ensure all integration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 29. Create main entry point and configuration
  - Create `ufac_engine/main.py` with CLI entry point
  - Load SystemConfig and IngestionConfig from environment or config file
  - Initialize all components: VectorStore, RAG, Agents, Watcher, API
  - Run startup validation
  - Start FastAPI server
  - Start Watcher Service scheduler
  - Create `config.example.yaml` with all configuration options documented
  - Create `.env.example` with required environment variables
  - _Requirements: 28.1, 28.2, 28.3, 28.5_

- [ ] 30. Write unit tests for specific examples and edge cases
  - Write unit tests for myscheme.gov.in API integration (Req 2.1)
  - Write unit tests for data.gov.in API integration (Req 2.2)
  - Write unit tests for PIB RSS feed parsing (Req 5.1)
  - Write unit tests for eligibility query routing (Req 10.2)
  - Write unit tests for temporal query routing (Req 10.3)
  - Write unit tests for specific error messages (Req 25.1, 25.2, 25.3)
  - Write unit tests for startup validation (Req 28.1, 28.2, 28.3, 28.5)
  - Write unit tests for API endpoint definition (Req 24.1)
  - Write unit tests for watcher schedule (Req 21.1)
  - Write unit tests for pretty-print function (Req 27.1)
  - Write unit tests for edge cases: empty PDFs, scanned PDFs, no scheme content, missing fields, < 3 RAG results, all council responses differ, rate limit boundaries

- [ ] 31. Create documentation and examples
  - Create `README.md` with installation, configuration, and usage instructions
  - Create `docs/API.md` documenting REST API endpoints and request/response formats
  - Create `docs/ARCHITECTURE.md` explaining system components and data flow
  - Create `examples/sample_queries.py` with example queries in English and Hindi
  - Create `examples/sample_ingestion.py` demonstrating ingestion from all sources
  - Document all 56 correctness properties in `docs/PROPERTIES.md`

- [ ] 32. Final checkpoint - End-to-end validation
  - Run full test suite (unit + property tests)
  - Verify all 56 properties pass with 100+ iterations
  - Test end-to-end flow: ingest sample schemes → query eligibility → verify response
  - Test Watcher Service with simulated document changes
  - Test API with rate limiting and error scenarios
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional property-based tests and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at major milestones
- Property tests validate universal correctness properties using Hypothesis
- Unit tests validate specific examples, edge cases, and integration points
- Implementation follows dependency order: data models → utilities → ingestion → storage → agents → API
- All code uses Python 3.11+ with type hints and Pydantic v2 for validation
