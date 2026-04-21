# Requirements Document

## Introduction

The UFAC Engine (Uncertainty-First Agent Council) is a multi-agent AI system designed to help Indian citizens discover and apply for central government agriculture schemes. The system ingests scheme data from multiple sources, processes it into a vector store, and uses a council of specialized AI agents to provide accurate, confidence-calibrated recommendations about scheme eligibility. The system emphasizes transparency by explicitly surfacing uncertainties, assumptions, and missing information rather than hiding them.

## Glossary

- **UFAC_Engine**: The complete multi-agent system for agriculture scheme discovery and eligibility assessment
- **Scheme**: A central government agriculture program (e.g., PM-KISAN, AIF, PMFBY, PMEGP, PMKSY, SMAM)
- **Ingestion_Module**: Component that accepts and processes scheme data from multiple sources
- **Vector_Store**: ChromaDB database storing embedded scheme documents for semantic search
- **RAG_System**: Retrieval-Augmented Generation system that retrieves relevant scheme chunks from Vector_Store
- **Planner_Agent**: Agent that routes queries to appropriate specialized agents
- **Fact_Agent**: Agent that extracts confirmed facts from user queries and scheme data
- **Assumption_Agent**: Agent that identifies implicit assumptions in eligibility assessment
- **Unknown_Agent**: Agent that flags missing critical information and can trigger additional RAG queries
- **Temporal_Agent**: Agent that detects scheme rule revisions and temporal validity
- **Scheme_Matcher_Agent**: Agent that scores eligibility for each scheme
- **Confidence_Agent**: Agent that provides calibrated confidence scores (0-100)
- **Decision_Agent**: Agent that generates actionable next steps for users
- **Critic_Agent**: Agent that performs final review and score calibration before output
- **Inner_Council**: Three parallel Gemini API calls per agent that vote on consensus
- **User_Profile**: Structured data extracted from user query (occupation, land, state, income, etc.)
- **Watcher_Service**: Background service that monitors government portals for scheme updates
- **Scheme_Chunk**: Embedded text segment from scheme documents stored in Vector_Store
- **Confidence_Score**: Calibrated 0-100 score indicating certainty of eligibility assessment
- **Safety_Flag**: Boolean indicator for potentially harmful or incorrect recommendations
- **Portal_Link**: Official government URL for scheme application
- **Query_API**: FastAPI REST endpoint for user eligibility queries
- **PDF_Parser**: Component using pymupdf and pdfplumber to extract text from PDF files
- **HTML_Scraper**: Component using beautifulsoup4 to extract scheme data from web pages
- **RSS_Monitor**: Component using feedparser to track PIB announcements
- **HF_Dataset_Loader**: Component that loads shrijayan/gov_myscheme dataset from HuggingFace
- **Change_Detector**: Component that uses SHA-256 hashing to detect scheme document changes
- **Embedding_Model**: Model that converts text into vector representations for Vector_Store
- **Top_K_Retrieval**: Process of retrieving K most semantically similar scheme chunks from Vector_Store

## Requirements

### Requirement 1: Ingest PDF Scheme Documents

**User Story:** As a system administrator, I want to ingest scheme data from PDF files, so that the system can process official government scheme documents.

#### Acceptance Criteria

1. WHEN a local PDF file path is provided, THE PDF_Parser SHALL extract all text content from the PDF
2. WHEN a PDF URL is provided, THE PDF_Parser SHALL download and extract all text content from the PDF
3. IF a PDF file is corrupted or unreadable, THEN THE PDF_Parser SHALL return a descriptive error message
4. THE PDF_Parser SHALL preserve document structure including headings, lists, and tables
5. WHEN PDF text is extracted, THE Ingestion_Module SHALL convert it to structured JSON format
6. THE Ingestion_Module SHALL include metadata fields: source_type, source_url, ingestion_timestamp, document_hash

### Requirement 2: Ingest REST API Scheme Data

**User Story:** As a system administrator, I want to ingest scheme data from REST APIs, so that the system can access live government scheme databases.

#### Acceptance Criteria

1. WHEN myscheme.gov.in API is queried, THE Ingestion_Module SHALL retrieve all agriculture scheme records
2. WHEN data.gov.in API is queried, THE Ingestion_Module SHALL retrieve all agriculture scheme datasets
3. IF an API request fails, THEN THE Ingestion_Module SHALL retry up to 3 times with exponential backoff
4. IF an API returns invalid JSON, THEN THE Ingestion_Module SHALL log the error and skip that record
5. THE Ingestion_Module SHALL convert API responses to structured JSON format
6. THE Ingestion_Module SHALL include metadata fields: api_endpoint, query_timestamp, response_status

### Requirement 3: Ingest HTML Scheme Pages

**User Story:** As a system administrator, I want to scrape scheme data from government portal HTML pages, so that the system can access schemes not available via APIs.

#### Acceptance Criteria

1. WHEN a government portal URL is provided, THE HTML_Scraper SHALL extract scheme information from the page
2. THE HTML_Scraper SHALL remove navigation elements, headers, footers, and advertisements
3. THE HTML_Scraper SHALL preserve scheme titles, descriptions, eligibility criteria, and application links
4. IF a page requires JavaScript rendering, THEN THE HTML_Scraper SHALL return an error indicating manual intervention needed
5. WHEN HTML content is extracted, THE Ingestion_Module SHALL convert it to structured JSON format
6. THE Ingestion_Module SHALL include metadata fields: source_url, scrape_timestamp, page_title

### Requirement 4: Ingest HuggingFace Dataset

**User Story:** As a system administrator, I want to load the shrijayan/gov_myscheme dataset from HuggingFace, so that the system can leverage pre-curated scheme data.

#### Acceptance Criteria

1. WHEN the system initializes, THE HF_Dataset_Loader SHALL download the shrijayan/gov_myscheme dataset
2. THE HF_Dataset_Loader SHALL filter records to include only agriculture-related schemes
3. THE HF_Dataset_Loader SHALL convert dataset records to structured JSON format
4. IF the dataset download fails, THEN THE HF_Dataset_Loader SHALL retry up to 3 times
5. THE Ingestion_Module SHALL include metadata fields: dataset_name, dataset_version, load_timestamp

### Requirement 5: Ingest RSS Feed Announcements

**User Story:** As a system administrator, I want to monitor PIB RSS feeds for scheme announcements, so that the system can capture newly announced schemes.

#### Acceptance Criteria

1. WHEN the RSS_Monitor runs, THE RSS_Monitor SHALL fetch all entries from the PIB agriculture RSS feed
2. THE RSS_Monitor SHALL filter entries containing keywords: "scheme", "agriculture", "farmer", "PM-KISAN", "PMFBY"
3. WHEN a new RSS entry is detected, THE Ingestion_Module SHALL extract the announcement text
4. THE Ingestion_Module SHALL convert RSS entries to structured JSON format
5. THE Ingestion_Module SHALL include metadata fields: rss_feed_url, publication_date, entry_id

### Requirement 6: Convert Scheme Data to Structured JSON

**User Story:** As a developer, I want all ingested scheme data in a consistent JSON format, so that downstream processing is uniform.

#### Acceptance Criteria

1. THE Ingestion_Module SHALL define a JSON schema with fields: scheme_name, description, eligibility_criteria, benefits, application_process, portal_link, state_specific, income_limit, land_requirement, occupation_requirement
2. WHEN scheme data is ingested from any source, THE Ingestion_Module SHALL map it to the defined JSON schema
3. IF a required field is missing, THEN THE Ingestion_Module SHALL populate it with null
4. THE Ingestion_Module SHALL validate all JSON outputs against the schema before storage
5. THE Ingestion_Module SHALL assign a unique scheme_id to each scheme record

### Requirement 7: Embed Scheme Documents into Vector Store

**User Story:** As a developer, I want scheme documents embedded into ChromaDB, so that semantic search can retrieve relevant schemes.

#### Acceptance Criteria

1. WHEN structured JSON scheme data is created, THE Embedding_Model SHALL generate vector embeddings for the text content
2. THE UFAC_Engine SHALL store embeddings in the Vector_Store with associated metadata
3. THE Vector_Store SHALL support metadata filtering by: state, scheme_type, income_range, land_range
4. THE Vector_Store SHALL chunk long scheme documents into segments of maximum 512 tokens
5. FOR ALL scheme documents, embedding then retrieval SHALL return the original document (round-trip property)
6. THE Vector_Store SHALL persist embeddings to disk for recovery after system restart

### Requirement 8: Extract User Profile from Query

**User Story:** As a citizen, I want the system to understand my situation from my natural language query, so that I receive personalized scheme recommendations.

#### Acceptance Criteria

1. WHEN a user query is received, THE Planner_Agent SHALL extract User_Profile fields: occupation, land_size, state, district, income, age, gender, caste_category
2. THE Planner_Agent SHALL handle queries in English and Hindi
3. IF a critical field is missing from the query, THEN THE Unknown_Agent SHALL flag it as missing information
4. THE Planner_Agent SHALL normalize extracted values (e.g., "5 acres" → 5.0, "Uttar Pradesh" → "UP")
5. THE Planner_Agent SHALL store the extracted User_Profile for use by downstream agents

### Requirement 9: Retrieve Top-K Matching Schemes via RAG

**User Story:** As a developer, I want the system to retrieve the most relevant schemes from the vector store, so that agents can assess eligibility accurately.

#### Acceptance Criteria

1. WHEN a User_Profile is extracted, THE RAG_System SHALL generate a search query from the profile
2. THE RAG_System SHALL retrieve the top 10 most semantically similar Scheme_Chunks from the Vector_Store
3. THE RAG_System SHALL apply metadata filters based on User_Profile (state, income range, land range)
4. THE RAG_System SHALL return Scheme_Chunks with similarity scores above 0.6
5. IF fewer than 3 Scheme_Chunks are retrieved, THEN THE RAG_System SHALL log a warning and broaden the search

### Requirement 10: Route Query Through Planner Agent

**User Story:** As a developer, I want queries routed to the appropriate specialized agents, so that each agent focuses on its expertise.

#### Acceptance Criteria

1. WHEN a query is received, THE Planner_Agent SHALL determine which specialized agents are needed
2. THE Planner_Agent SHALL route eligibility queries to: Fact_Agent, Assumption_Agent, Unknown_Agent, Scheme_Matcher_Agent, Confidence_Agent, Decision_Agent
3. THE Planner_Agent SHALL route temporal queries (e.g., "has this scheme changed?") to the Temporal_Agent
4. THE Planner_Agent SHALL execute agents in dependency order: Fact → Assumption → Unknown → Scheme_Matcher → Confidence → Decision
5. THE Planner_Agent SHALL pass outputs from each agent as inputs to subsequent agents

### Requirement 11: Implement Inner LLM Council with Consensus Voting

**User Story:** As a developer, I want each agent to call Gemini 3 times and vote on consensus, so that agent outputs are more reliable.

#### Acceptance Criteria

1. WHEN an agent processes a task, THE agent SHALL make 3 parallel calls to the Gemini API with identical prompts
2. THE agent SHALL collect all 3 responses from the Inner_Council
3. THE agent SHALL implement majority voting: if 2 or more responses agree, that response is selected
4. IF all 3 responses differ, THEN THE agent SHALL select the response with the highest confidence score
5. THE agent SHALL log disagreements between Inner_Council members for monitoring

### Requirement 12: Extract Confirmed Facts

**User Story:** As a citizen, I want the system to identify confirmed facts from my query, so that I know what information was understood correctly.

#### Acceptance Criteria

1. WHEN the Fact_Agent processes a query, THE Fact_Agent SHALL extract all explicitly stated facts from the User_Profile
2. THE Fact_Agent SHALL distinguish between stated facts (e.g., "I own 5 acres") and inferred facts
3. THE Fact_Agent SHALL return a list of confirmed facts with source references (user query or scheme document)
4. THE Fact_Agent SHALL flag contradictions between user-stated facts and scheme requirements

### Requirement 13: Identify Implicit Assumptions

**User Story:** As a citizen, I want the system to surface assumptions it's making about my eligibility, so that I can correct misunderstandings.

#### Acceptance Criteria

1. WHEN the Assumption_Agent processes a query, THE Assumption_Agent SHALL identify all implicit assumptions made during eligibility assessment
2. THE Assumption_Agent SHALL categorize assumptions as: demographic, geographic, temporal, or financial
3. THE Assumption_Agent SHALL return assumptions with explanations (e.g., "Assuming you are a small farmer because land < 2 hectares")
4. THE Assumption_Agent SHALL flag high-risk assumptions that could significantly affect eligibility

### Requirement 14: Flag Missing Critical Information

**User Story:** As a citizen, I want the system to tell me what information is missing, so that I can provide it for a more accurate assessment.

#### Acceptance Criteria

1. WHEN the Unknown_Agent processes a query, THE Unknown_Agent SHALL identify missing fields required for eligibility assessment
2. THE Unknown_Agent SHALL categorize missing information by priority: critical, important, optional
3. THE Unknown_Agent SHALL return a list of missing information with explanations of why it's needed
4. WHERE missing information prevents accurate assessment, THE Unknown_Agent SHALL trigger additional Top_K_Retrieval from the RAG_System to find alternative schemes

### Requirement 15: Detect Scheme Rule Revisions

**User Story:** As a citizen, I want to know if scheme rules have changed recently, so that I don't rely on outdated information.

#### Acceptance Criteria

1. WHEN the Temporal_Agent processes a query, THE Temporal_Agent SHALL check if retrieved schemes have multiple versions in the Vector_Store
2. THE Temporal_Agent SHALL identify the most recent version of each scheme based on ingestion_timestamp
3. IF a scheme has been revised within the last 90 days, THEN THE Temporal_Agent SHALL flag it as recently updated
4. THE Temporal_Agent SHALL return revision dates and summaries of changes when available

### Requirement 16: Score Scheme Eligibility

**User Story:** As a citizen, I want to know how well I match each scheme's eligibility criteria, so that I can prioritize applications.

#### Acceptance Criteria

1. WHEN the Scheme_Matcher_Agent processes retrieved schemes, THE Scheme_Matcher_Agent SHALL calculate an eligibility score (0-100) for each scheme
2. THE Scheme_Matcher_Agent SHALL base scores on: matching criteria count, missing criteria severity, User_Profile completeness
3. THE Scheme_Matcher_Agent SHALL return schemes ranked by eligibility score in descending order
4. THE Scheme_Matcher_Agent SHALL include per-criterion match status (met, not met, unknown)

### Requirement 17: Calculate Calibrated Confidence Scores

**User Story:** As a citizen, I want to know how confident the system is in its recommendations, so that I can assess reliability.

#### Acceptance Criteria

1. WHEN the Confidence_Agent processes scheme matches, THE Confidence_Agent SHALL calculate a Confidence_Score (0-100) for each recommendation
2. THE Confidence_Agent SHALL base confidence on: User_Profile completeness, scheme document clarity, Inner_Council agreement, RAG retrieval similarity
3. THE Confidence_Agent SHALL reduce confidence by 20 points for each critical missing field
4. THE Confidence_Agent SHALL reduce confidence by 10 points for each high-risk assumption
5. THE Confidence_Agent SHALL return confidence scores with explanations of factors affecting confidence

### Requirement 18: Generate Actionable Next Steps

**User Story:** As a citizen, I want clear next steps for applying to schemes, so that I know exactly what to do.

#### Acceptance Criteria

1. WHEN the Decision_Agent processes scheme matches, THE Decision_Agent SHALL generate a prioritized list of next steps for each scheme
2. THE Decision_Agent SHALL include steps for: gathering missing documents, visiting portals, contacting offices, verifying eligibility
3. THE Decision_Agent SHALL provide Portal_Links for online applications
4. THE Decision_Agent SHALL estimate time required for each step
5. THE Decision_Agent SHALL sequence steps in logical order (e.g., gather documents before visiting portal)

### Requirement 19: Perform Final Review and Calibration

**User Story:** As a developer, I want a final review of all agent outputs before returning to the user, so that errors are caught.

#### Acceptance Criteria

1. WHEN all agents complete processing, THE Critic_Agent SHALL review all outputs for consistency
2. THE Critic_Agent SHALL verify that Confidence_Scores align with identified unknowns and assumptions
3. THE Critic_Agent SHALL check for logical contradictions between agent outputs
4. IF the Critic_Agent detects a Safety_Flag condition (e.g., recommending an ineligible scheme with high confidence), THEN THE Critic_Agent SHALL reduce the Confidence_Score and add a warning
5. THE Critic_Agent SHALL approve the final output or request re-processing by specific agents

### Requirement 20: Return Structured Response

**User Story:** As a citizen, I want a clear, structured response with all relevant information, so that I can make informed decisions.

#### Acceptance Criteria

1. THE UFAC_Engine SHALL return a JSON response with fields: matched_schemes, confidence_scores, safety_flags, unknowns, assumptions, next_steps, portal_links
2. THE UFAC_Engine SHALL include the top 5 matched schemes ranked by eligibility score
3. THE UFAC_Engine SHALL include all identified unknowns and assumptions
4. THE UFAC_Engine SHALL include a global Safety_Flag if any scheme has a safety concern
5. THE UFAC_Engine SHALL include response_metadata: query_timestamp, processing_time_ms, agents_invoked

### Requirement 21: Monitor Government Portals for Updates

**User Story:** As a system administrator, I want the system to automatically check for scheme updates, so that the database stays current.

#### Acceptance Criteria

1. THE Watcher_Service SHALL run nightly at 02:00 IST
2. WHEN the Watcher_Service runs, THE Watcher_Service SHALL check all configured government portal URLs
3. THE Change_Detector SHALL calculate SHA-256 hashes of fetched scheme documents
4. IF a document hash differs from the stored hash, THEN THE Watcher_Service SHALL trigger re-ingestion of that document
5. THE Watcher_Service SHALL log all detected changes with timestamps and change summaries

### Requirement 22: Detect Scheme Document Changes

**User Story:** As a system administrator, I want to know exactly what changed in scheme documents, so that I can review updates.

#### Acceptance Criteria

1. WHEN a document hash changes, THE Change_Detector SHALL compare the old and new document versions
2. THE Change_Detector SHALL identify changed sections: eligibility criteria, benefits, application process, deadlines
3. THE Change_Detector SHALL generate a change summary with before/after snippets
4. THE Change_Detector SHALL flag critical changes (e.g., eligibility criteria tightened, scheme discontinued)
5. THE Change_Detector SHALL store change history in the Vector_Store with temporal metadata

### Requirement 23: Re-ingest Only Changed Schemes

**User Story:** As a system administrator, I want to re-ingest only changed schemes, so that the update process is efficient.

#### Acceptance Criteria

1. WHEN the Watcher_Service detects a changed document, THE Ingestion_Module SHALL re-process only that document
2. THE Ingestion_Module SHALL update the Vector_Store with new embeddings for changed Scheme_Chunks
3. THE Ingestion_Module SHALL preserve the scheme_id and update the version_number
4. THE Ingestion_Module SHALL mark old versions as archived but retain them for temporal queries
5. THE Ingestion_Module SHALL complete re-ingestion within 5 minutes per changed document

### Requirement 24: Expose REST API for Queries

**User Story:** As a frontend developer, I want a REST API to submit user queries, so that I can build user interfaces.

#### Acceptance Criteria

1. THE Query_API SHALL expose a POST endpoint at /api/v1/query accepting JSON with field: user_query
2. WHEN a query is received, THE Query_API SHALL validate the input and return 400 for invalid requests
3. THE Query_API SHALL invoke the UFAC_Engine and return the structured response as JSON
4. THE Query_API SHALL implement rate limiting: 10 requests per minute per IP address
5. THE Query_API SHALL return responses within 10 seconds for 95% of queries
6. THE Query_API SHALL log all queries with timestamps and response times

### Requirement 25: Handle API Errors Gracefully

**User Story:** As a citizen, I want clear error messages when something goes wrong, so that I know how to proceed.

#### Acceptance Criteria

1. IF the Gemini API is unavailable, THEN THE UFAC_Engine SHALL return a 503 error with message "AI service temporarily unavailable"
2. IF the Vector_Store is unavailable, THEN THE UFAC_Engine SHALL return a 503 error with message "Database temporarily unavailable"
3. IF a query times out after 30 seconds, THEN THE UFAC_Engine SHALL return a 504 error with message "Query processing timeout"
4. IF an agent raises an exception, THEN THE UFAC_Engine SHALL log the error and continue with remaining agents
5. THE Query_API SHALL never expose internal error details or stack traces to users

### Requirement 26: Parse PDF Documents with Fallback

**User Story:** As a system administrator, I want robust PDF parsing with fallback methods, so that text extraction succeeds even for complex PDFs.

#### Acceptance Criteria

1. WHEN the PDF_Parser processes a PDF, THE PDF_Parser SHALL first attempt extraction using pymupdf
2. IF pymupdf extraction yields less than 100 characters, THEN THE PDF_Parser SHALL retry using pdfplumber
3. THE PDF_Parser SHALL detect and handle scanned PDFs by returning an error indicating OCR is required
4. THE PDF_Parser SHALL preserve table structures by extracting them as structured data
5. FOR ALL valid PDF files, parsing then pretty-printing then parsing SHALL produce equivalent structured output (round-trip property)

### Requirement 27: Pretty-Print Scheme Data

**User Story:** As a system administrator, I want to export scheme data in human-readable format, so that I can review ingested content.

#### Acceptance Criteria

1. THE Ingestion_Module SHALL provide a pretty-print function that formats structured JSON as readable text
2. THE pretty-print function SHALL include scheme name, eligibility criteria, benefits, and application process
3. THE pretty-print function SHALL format lists and tables with proper indentation
4. THE pretty-print function SHALL include metadata: source, ingestion date, version
5. FOR ALL structured JSON scheme records, parsing then pretty-printing then parsing SHALL produce equivalent data (round-trip property)

### Requirement 28: Validate Configuration on Startup

**User Story:** As a system administrator, I want the system to validate its configuration on startup, so that misconfigurations are caught early.

#### Acceptance Criteria

1. WHEN the UFAC_Engine starts, THE UFAC_Engine SHALL validate that the Gemini API key is present and valid
2. THE UFAC_Engine SHALL validate that the Vector_Store directory is writable
3. THE UFAC_Engine SHALL validate that all required Python packages are installed with correct versions
4. IF any validation fails, THEN THE UFAC_Engine SHALL log a descriptive error and exit with code 1
5. THE UFAC_Engine SHALL log successful startup with version number and configuration summary

### Requirement 29: Support Metadata Filtering in RAG

**User Story:** As a citizen, I want the system to filter schemes by my state and situation, so that I only see relevant schemes.

#### Acceptance Criteria

1. WHEN the RAG_System retrieves schemes, THE RAG_System SHALL apply metadata filters based on User_Profile
2. WHERE a user specifies a state, THE RAG_System SHALL filter to schemes available in that state or nationwide schemes
3. WHERE a user specifies income, THE RAG_System SHALL filter to schemes with income limits above the user's income or no income limit
4. WHERE a user specifies land size, THE RAG_System SHALL filter to schemes with land requirements matching the user's land size
5. THE RAG_System SHALL combine semantic similarity scores with metadata filter matches for final ranking

### Requirement 30: Log Agent Interactions for Debugging

**User Story:** As a developer, I want detailed logs of agent interactions, so that I can debug issues and improve the system.

#### Acceptance Criteria

1. THE UFAC_Engine SHALL log each agent invocation with: agent_name, input_data, output_data, processing_time_ms
2. THE UFAC_Engine SHALL log Inner_Council voting results with: responses, votes, selected_response
3. THE UFAC_Engine SHALL log RAG retrieval results with: query, retrieved_chunks, similarity_scores
4. THE UFAC_Engine SHALL log Critic_Agent reviews with: issues_found, corrections_made, final_confidence
5. THE UFAC_Engine SHALL write logs to a structured JSON log file with daily rotation
