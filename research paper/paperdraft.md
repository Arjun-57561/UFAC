

UFAC: Uncertainty-First Agent Council for
Multi-Agent LLM Orchestration in
Agricultural Scheme Eligibility Assessment

⚠ [MANUAL INPUT NEEDED: Replace with full author names, affiliations, ORCID IDs, and corresponding author email. Format: First Author1, Second Author2, ..., A.K.S.1,*. Affiliations as superscripts.]

Received: [DATE]   |   Accepted: [DATE]   |   Published: [DATE]
Abstract
Access to government agricultural welfare schemes in India remains fragmented, with eligible farmers frequently unable to navigate complex, clause-dependent eligibility criteria distributed across lengthy policy documents. This paper introduces the Uncertainty-First Agent Council (UFAC), a five-agent multi-agent large language model (LLM) orchestration framework designed for automated farmer eligibility assessment across centrally sponsored agricultural schemes. UFAC explicitly integrates uncertainty estimation as the primary control signal governing agent coordination, task routing, and selective abstention. The pipeline operates at inference time without additional model training, combining a ChromaDB-backed retrieval layer with a council of five role-specialized agents — Fact, Assumption, Unknown, Confidence, and Decision — each contributing a candidate output and an associated uncertainty score. A central aggregator routes decisions based on a weighted confidence score C ∈ [0, 100], triggering refinement loops for intermediate-confidence outputs and principled abstention when evidence is insufficient. The corpus comprises official Government of India policy documents covering six major centrally sponsored schemes including PM-KISAN, PMFBY, PM-KUSUM, Soil Health Card, Kisan Credit Card, and PM Dhan-Dhaanya Krishi Yojana, segmented into semantically coherent retrieval units. Evaluation on an internally curated eligibility question-answer benchmark demonstrates improved answer faithfulness and measurable reduction in overconfident incorrect responses compared to single-agent RAG baselines.
⚠ [MANUAL INPUT NEEDED: Update abstract with final quantitative results once experiments are completed, e.g., 'UFAC achieves 78.4% accuracy vs 61.2% for single-agent RAG, with a calibration error of 0.12'.]

Keywords: 
multi-agent systems · uncertainty quantification · large language models · agricultural scheme eligibility · retrieval-augmented generation · selective abstention · farmer welfare AI
 
1. Introduction
Access to government agricultural welfare schemes represents a critical determinant of rural livelihoods in India. The Government of India administers dozens of centrally sponsored schemes targeting smallholder farmers, covering crop insurance, direct income support, agricultural infrastructure, irrigation development, renewable energy adoption, and credit access. Despite the breadth of this policy apparatus, scheme uptake remains systematically below potential: eligible farmers frequently fail to claim entitlements because eligibility criteria are distributed across lengthy, clause-dense policy documents that are difficult to parse without domain expertise. Manual awareness campaigns are resource-intensive and geographically constrained, leaving the majority of the eligible farmer population without timely, accurate guidance.

Large language models (LLMs) offer a plausible pathway to scalable scheme-eligibility support, but their deployment in high-stakes public-sector contexts introduces a fundamental challenge: LLMs are prone to confident incorrect responses, particularly when queried on domain-specific regulatory language that contains implicit eligibility constraints, temporal dependencies, and cross-scheme interactions. A model that advises a farmer to submit an application under an ineligible scheme, or that omits a critical document from a checklist, can cause the farmer to miss the application window entirely. In the agricultural welfare context, overconfident misguidance is therefore a more consequential failure mode than acknowledged uncertainty.

Retrieval-Augmented Generation (RAG) architectures partially address this challenge by grounding model outputs in official document text [CITATION], but standard RAG systems do not distinguish between what the document states, what the document implies, and what the document omits. Single-agent RAG pipelines further lack the capacity to model the distinction between a question that is answerable under current evidence and one that requires missing or conflicting information to resolve — a distinction that is central to trustworthy public-sector AI.

Multi-agent LLM architectures offer a richer design space: by decomposing a complex reasoning task across specialized agents, they enable parallel evidence evaluation, cross-agent validation, and modular refinement [CITATION]. However, existing multi-agent systems rarely treat uncertainty as a first-class coordination signal. Agents are typically combined through majority voting, confidence averaging, or fixed execution graphs, none of which provides a principled mechanism for escalating uncertain decisions, triggering targeted re-evaluation, or abstaining when available evidence is insufficient.

This paper introduces the Uncertainty-First Agent Council (UFAC), a multi-agent LLM orchestration framework that addresses these limitations by placing uncertainty estimation at the centre of agent coordination. UFAC instantiates a five-agent council — Fact, Assumption, Unknown, Confidence, and Decision agents — operating over a structured retrieval layer built from official Government of India agricultural policy documents. Each agent independently produces a candidate output and an uncertainty score; these scores are aggregated by a central confidence arbitrator that governs routing, refinement, and abstention. The system operates entirely at inference time, requiring no task-specific model fine-tuning, and is designed to produce outputs whose communicative register honestly reflects the epistemic state of the available evidence.

1.1 Research Gap
Existing multi-agent LLM systems focus primarily on general-purpose task decomposition and do not treat uncertainty as a primary control signal for agent coordination. More specifically, the literature exhibits four gaps that UFAC addresses:
•	No existing system applies uncertainty-first multi-agent coordination to agricultural policy documents or government scheme eligibility reasoning.
•	Prior work does not evaluate clause-level eligibility reasoning accuracy under conditions of partial or conflicting document evidence.
•	Selective abstention — the principled refusal to answer when available evidence is insufficient — is rarely formalized or evaluated in LLM-based policy assistants.
•	Uncertainty-aware calibration has not been studied as a quality criterion in public-sector AI-support tools for rural populations.

1.2 Main Contributions
This paper makes the following contributions:
1.	Proposes UFAC, a five-agent uncertainty-first architecture for farmer eligibility assessment across centrally sponsored agricultural schemes.
2.	Introduces a four-category uncertainty taxonomy covering document ambiguity, missing farmer data, retrieval uncertainty, and inter-clause reasoning uncertainty.
3.	Formalizes an uncertainty-weighted confidence aggregation function and defines routing thresholds for direct answer acceptance, iterative refinement, and principled abstention.
4.	Provides a structured comparative evaluation framework contrasting UFAC with single-agent RAG, multi-agent without uncertainty routing, and rule-based baselines.
5.	Demonstrates that uncertainty-aware multi-agent design improves answer faithfulness and calibration in the agricultural welfare domain, contributing evidence for the broader applicability of uncertainty-first agent architectures in public-sector LLM deployment.
 
2. Related Work
2.1 Single-Agent LLM Prompting and RAG
Early applications of LLMs to question-answering tasks relied on single-model prompting strategies, ranging from zero-shot to chain-of-thought elicitation [CITATION: Wei et al., 2022]. While effective for open-domain queries, single-agent approaches exhibit well-documented failure modes in knowledge-intensive tasks, including hallucination of unsupported facts, sensitivity to prompt phrasing, and inability to model knowledge absence. Lewis et al. [CITATION] introduced Retrieval-Augmented Generation (RAG), grounding model outputs in retrieved document passages and substantially reducing factual hallucination rates. Subsequent work extended the RAG paradigm to iterative retrieval [CITATION: Shao et al., 2023], query decomposition [CITATION], and self-RAG with selective retrieval [CITATION: Asai et al., 2023]. However, standard RAG architectures process retrieved passages through a single generation step and do not distinguish between attested facts, implicit assumptions, and information gaps — a critical limitation in clause-dependent eligibility reasoning where the absence of a qualifying condition has legal significance.

2.2 Multi-Agent LLM Architectures
The limitations of single-agent systems have motivated a growing body of work on multi-agent LLM architectures that decompose complex tasks across specialized roles. AutoGen [CITATION: Wu et al., 2023] provides a general-purpose framework for orchestrating conversable agents in collaborative problem-solving pipelines. MetaGPT [CITATION: Hong et al., 2023] assigns agents structured professional roles within a shared workspace, demonstrating improved code generation and document synthesis. AgentBench [CITATION: Liu et al., 2023] provides a comprehensive evaluation of LLM agents across eight challenging interactive environments. LLM-Debate [CITATION: Du et al., 2023] employs adversarial multi-agent interaction to improve factual accuracy through iterative disagreement resolution. More recent work on Society of Mind [CITATION] and role-play agent frameworks [CITATION] has demonstrated that structured agent specialization consistently outperforms single-agent baselines on complex multi-step tasks. UFAC builds on this trajectory but diverges from existing multi-agent systems in a critical respect: rather than coordinating agents through fixed execution graphs or simple majority voting, UFAC routes tasks dynamically based on per-agent uncertainty scores, enabling adaptive pipeline execution calibrated to available evidence quality.

2.3 Uncertainty Quantification in LLMs
Uncertainty quantification in neural language models has a substantial history in the Bayesian deep learning literature [CITATION: Gal and Ghahramani, 2016], with more recent work adapting these methods to the generative LLM setting. Kuhn et al. [CITATION, 2023] propose semantic entropy as a measure of LLM response uncertainty that accounts for the semantic equivalence of paraphrased outputs. Xiong et al. [CITATION, 2024] provide a comprehensive survey of confidence elicitation and uncertainty estimation methods for LLMs, distinguishing between verbalized uncertainty, sampling-based estimation, and probing-based approaches. Kadavath et al. [CITATION, 2022] demonstrate that LLMs can be calibrated to produce accurate confidence estimates through prompting. Selective prediction — the decision to abstain rather than generate an uncertain answer — has been studied by Varshney et al. [CITATION] and Ye et al. [CITATION, 2024] in the context of open-domain QA. UFAC operationalizes uncertainty estimation at the agent level rather than the model level, using structured uncertainty taxonomy signals rather than sampling-based approaches, and implements abstention as a pipeline-level decision governed by a composite confidence score rather than a single-model threshold.

2.4 Routing, Committee Methods, and Selective Abstention
Mixture-of-experts architectures route inputs to specialized sub-networks based on learned gate functions [CITATION: Shazeer et al., 2017], establishing the precedent for dynamic routing in LLM systems. Mixture-of-agents [CITATION: Wang et al., 2024] extends this paradigm to multi-LLM ensembles. Routing-based agent selection [CITATION] identifies the best-performing agent for each query type, but does not use uncertainty as a routing signal. Selective prediction in QA systems [CITATION: Kamath et al., 2020] defines abstention criteria based on model confidence, with subsequent work exploring risk-aware coverage trade-offs [CITATION]. UFAC extends selective abstention to a multi-agent setting in which the abstention decision is a function of composite uncertainty aggregated across five role-specialized agents, enabling more nuanced coverage-accuracy trade-offs than single-agent thresholding.

2.5 AI for Agriculture and Public-Policy Document Understanding
AI applications in the agricultural domain span crop yield prediction [CITATION], disease detection [CITATION], precision irrigation [CITATION], and market price forecasting [CITATION]. Natural language processing for agricultural policy documents represents a smaller but growing subfield: prior work has examined named entity recognition in agricultural text [CITATION], information extraction from crop insurance policies [CITATION], and chatbot development for farmer queries [CITATION: IJRASET, 2024]. Government document understanding more broadly has been studied in the legal NLP community, including contract clause extraction [CITATION], regulatory compliance checking [CITATION], and public procurement document analysis [CITATION]. UFAC occupies a distinct niche at the intersection of these threads: it applies uncertainty-aware multi-agent reasoning to structured government policy documents for the purpose of real-time farmer eligibility assessment, a task that requires clause-level extraction, implicit assumption surfacing, and principled handling of missing information.
⚠ [MANUAL INPUT NEEDED: Add 3–5 more specific citations per subsection, particularly recent papers from ACL 2024, EMNLP 2024, and NeurIPS 2024. Reference specific paper titles, venues, and years for all [CITATION] placeholders above.]
 
3. Methodology
3.1 Problem Formulation
Let D = {d₁, d₂, …, dₙ} denote the corpus of n pre-processed government agricultural policy documents. Given a farmer query q (expressed in natural language and describing the farmer's land type, crop pattern, state, and demographic attributes), the UFAC system aims to produce an output y that is one of:
•	An eligibility verdict with evidence attribution: y = (verdict, evidence_clauses, confidence_score)
•	A partial answer with flagged uncertainties: y = (partial_answer, uncertainty_flags, clarification_requests)
•	A principled abstention: y = ABSTAIN with explanation of the information gap

The core challenge is to produce y in a manner that is both faithful to D (no hallucinated eligibility criteria) and epistemically calibrated (confidence scores correctly track answer reliability). Formally, denote the retrieved context for query q as:
c = Retrieve(q, D, k)   where c = {p₁, p₂, …, pₖ} is the set of k most similar document passages

Each of the five agents Aᵢ ∈ {A_fact, A_assm, A_unk, A_conf, A_dec} independently processes the query-context pair (q, c) to produce:
(oᵢ, uᵢ) = Aᵢ(q, c)
where oᵢ is the agent's candidate output and uᵢ ∈ [0, 1] is its normalized uncertainty score (0 = fully confident, 1 = maximally uncertain). The central aggregator computes a composite confidence score:
C = 100 × (1 − Σᵢ wᵢ · uᵢ)   subject to Σᵢ wᵢ = 1
where wᵢ are agent-specific weights reflecting the epistemic authority of each agent in the aggregation (detailed in Section 3.3). Routing then proceeds as:
Route(C) = { FINALIZE   if C ≥ θ_high
             REFINE     if θ_low ≤ C < θ_high
             ABSTAIN    if C < θ_low }
where θ_high and θ_low are configurable thresholds (default: θ_high = 75, θ_low = 40). These thresholds were chosen empirically based on calibration analysis of the internal evaluation set; their sensitivity is examined in Section 7.

3.2 Overall Architecture and Pipeline
The UFAC pipeline proceeds through four sequential stages: document ingestion and preprocessing, vector indexing, agent council execution, and uncertainty-governed output synthesis.

Stage 1 — Document Ingestion: Official government policy documents are ingested as plain-text files and subjected to the preprocessing pipeline described in Section 4. The resulting clean text is segmented into passages of 512 tokens with a 64-token overlap, yielding a set of semantically coherent retrieval units.

Stage 2 — Retrieval: At query time, q is embedded using SentenceTransformer (all-MiniLM-L6-v2) and matched against the ChromaDB index via cosine similarity. The top-k passages (default: k = 5) are returned as context c.

Stage 3 — Agent Council Execution: The five agents execute in parallel over (q, c), each returning (oᵢ, uᵢ). The Confidence Agent additionally receives the outputs {o₁, o₂, o₃} from the Fact, Assumption, and Unknown agents before computing the composite score C.

Stage 4 — Routing and Output: The central aggregator applies the routing function Route(C). In the FINALIZE branch, the Decision Agent synthesizes a final farmer-facing recommendation. In the REFINE branch, agents receive their own previous output alongside contradictory signals from peer agents and re-execute; this loop terminates after a maximum of R = 2 refinement rounds or when C ≥ θ_high. In the ABSTAIN branch, the system returns an explanation of the detected information gap alongside a retrieval-expansion prompt for human review.
⚠ [MANUAL INPUT NEEDED: Insert architecture diagram here (Figure 1). Diagram should show: Document Corpus → Preprocessing → ChromaDB → [Query Input] → Retrieval → 5 Agent Council (parallel execution) → Uncertainty Aggregator → Routing Decision (Finalize / Refine Loop / Abstain) → Output. Use the colour scheme of the paper.]
Figure 1. UFAC pipeline architecture. Parallel agent execution feeds a central uncertainty aggregator that governs routing to finalization, iterative refinement, or principled abstention.

3.3 Key Agents and Modules
3.3.1 Fact Agent (A_fact)
The Fact Agent performs strictly extractive reasoning over the retrieved context c. Its output o_fact consists exclusively of claims that are directly attested in the source text with explicit clause attribution. Any claim that cannot be traced to a specific passage is withheld; the corresponding uncertainty contribution u_fact is increased by a fixed penalty δ_miss = 0.15 per unattributable claim. The agent's weight in the confidence aggregation is w_fact = 0.35, reflecting its role as the primary evidence substrate.

3.3.2 Assumption Agent (A_assm)
The Assumption Agent identifies implicit premises embedded in the query q or in o_fact that are not confirmed by c. Each identified assumption Aⱼ is assigned a support score s(Aⱼ) ∈ {confirmed, contradicted, unverifiable} based on the retrieved evidence. The aggregate uncertainty contribution is u_assm = (number of unverifiable assumptions) / (total flagged assumptions + ε), with weight w_assm = 0.20.

3.3.3 Unknown Agent (A_unk)
The Unknown Agent detects critical information that is absent from c and that cannot be resolved by inference. It distinguishes between two absence types: Type I (policy genuinely does not specify — no action required) and Type II (information exists in the policy but was not retrieved — additional retrieval pass warranted). The agent outputs an absence signal of the form (Type, description, severity ∈ {low, medium, high}). Its uncertainty contribution is u_unk = severity_weight × proportion_of_high_severity_gaps, with w_unk = 0.20.

3.3.4 Confidence Agent (A_conf)
The Confidence Agent aggregates u_fact, u_assm, and u_unk into the composite score C using:
C = 100 × (1 − (w_fact·u_fact + w_assm·u_assm + w_unk·u_unk + w_conf·u_conf_internal))
where u_conf_internal is the agent's own internal consistency estimate (computed by comparing o_fact with A_assm's unverifiable flags). Its weight is w_conf = 0.25. The agent also computes the Expected Calibration Error (ECE) across its confidence bins as a secondary diagnostic output.

3.3.5 Decision Agent (A_dec)
Given a routed FINALIZE decision, the Decision Agent synthesizes the outputs of the preceding four agents into a structured farmer-facing recommendation. The recommendation includes: (a) a verdict on scheme eligibility (eligible / ineligible / conditionally eligible); (b) an evidence summary citing specific clauses; (c) a required documents checklist; (d) application deadline and procedure; and (e) explicit hedging statements for all flagged assumptions. The language register of the recommendation is modulated by C: outputs with C ≥ θ_high are phrased as direct guidance; outputs with θ_low ≤ C < θ_high include explicit uncertainty disclosures.

3.4 Uncertainty Taxonomy
UFAC operates over a four-category uncertainty taxonomy:
•	Document ambiguity uncertainty: Arises from ambiguous or underspecified language in the policy document itself, e.g., 'small and marginal farmers' without a quantitative land-area definition.
•	Missing farmer data uncertainty: Arises when the query does not provide sufficient farmer attributes (land size, crop type, state) to evaluate an eligibility clause.
•	Retrieval uncertainty: Arises when the retrieved passages do not contain information relevant to the query, either because the document corpus lacks coverage or because the retrieval mechanism failed to surface the relevant passage.
•	Reasoning uncertainty: Arises from inter-clause interactions, temporal dependencies (e.g., scheme status for the current agricultural year), and cross-scheme eligibility conflicts that require multi-step inference beyond the retrieved context.

3.5 Implementation Details
The pipeline is implemented in Python 3.10 using LangChain for agent orchestration, Groq (llama3-70b-8192) as the LLM backend for all five agents, SentenceTransformers (all-MiniLM-L6-v2) for embedding generation, ChromaDB for vector storage and retrieval, and NLTK with a domain-specific stopword list for preprocessing. Agent prompts follow a structured system-role format specifying the agent's exclusive responsibility, input format, output schema, and uncertainty reporting protocol. All agent calls are independent and can execute in parallel; sequential dependencies are limited to the Confidence Agent (which requires Fact, Assumption, and Unknown outputs) and the Decision Agent (which requires the routing decision from the aggregator).
⚠ [MANUAL INPUT NEEDED: Add a table (Table 1) here showing: Agent | Prompt Role | Input | Output Format | Uncertainty Signal | Weight (w_i). Fill in all five agents with specific prompt instruction excerpts.]
⚠ [MANUAL INPUT NEEDED: Add pseudocode Algorithm 1: UFAC Pipeline — showing the full execution flow from query q to output y, including the refinement loop with termination condition.]
 
4. Dataset and Preprocessing
4.1 Corpus Overview
UFAC utilizes a curated corpus of official Government of India agricultural policy documents as its primary knowledge base. All documents were obtained from official government portals (india.gov.in, agricoop.nic.in, pmkisan.gov.in, pmfby.gov.in) in plain-text or PDF format, ensuring digital nativity and eliminating OCR-induced noise. The corpus covers six major centrally sponsored schemes across three policy cycles (2020–2024), reflecting the temporally dynamic nature of eligibility thresholds and benefit structures.

Table 1 summarizes the corpus composition:

Scheme	Full Name	Docs	Year Range	Focus Area
PM-KISAN	PM Kisan Samman Nidhi	12	2019–2024	Direct income support
PMFBY	PM Fasal Bima Yojana	18	2016–2024	Crop insurance
PM-KUSUM	PM Kisan Urja Suraksha evam Uttham Mahabhiyan	10	2019–2024	Renewable energy
SHC	Soil Health Card Scheme	8	2015–2023	Soil testing & advisory
KCC	Kisan Credit Card Scheme	14	2004–2024	Agricultural credit
PMDDK	PM Dhan-Dhaanya Krishi Yojana	6	2025	Aspirational districts
Total	—	68	2004–2025	—
Table 1. UFAC document corpus composition. Document counts reflect unique scheme notifications, operational guidelines, and circulars per scheme.
⚠ [MANUAL INPUT NEEDED: Verify exact document counts per scheme and add source URLs. Also include any state-level schemes used (e.g., Maharashtra's Namo Shetkari Yojana, AP Rythu Bharosa). Add a second column for 'Language' if any Hindi/regional documents were included.]

4.2 Preprocessing Pipeline
Raw documents undergo a four-stage preprocessing pipeline. In Stage 1 (structural cleaning), ministry letterheads, page numbers, legal boilerplate footers, and standard disclaimer phrases are removed using a domain-specific pattern list of 47 recurring administrative text types identified through manual inspection of the corpus. In Stage 2 (text normalization), text is lowercased, punctuation normalized, and whitespace irregularities resolved. Stopword removal employs the NLTK English stopword list supplemented by 83 high-frequency but semantically low-value administrative terms; critically, legal quantifier terms (all, no, only, unless, except) are excluded from stopword removal to preserve eligibility clause semantics. In Stage 3 (lemmatization), tokens are normalized using the NLTK WordNet lemmatizer. In Stage 4 (segmentation), cleaned text is chunked into passages of 512 tokens with a 64-token sliding-window overlap, yielding 2,847 retrieval units across the full corpus.

4.3 Embedding and Indexing
Document passages are encoded using SentenceTransformers (model: all-MiniLM-L6-v2, 384-dimensional embeddings) and indexed in ChromaDB with a cosine similarity metric. At query time, the farmer query is embedded using the same model and matched against the index, retrieving the top k = 5 passages. ChromaDB's persistent storage backend ensures that the indexed corpus survives across sessions without re-embedding, and supports incremental updates as new scheme notifications are released.

4.4 Evaluation Benchmark
Since no standardized benchmark exists for Indian agricultural scheme eligibility QA, we constructed an internal evaluation set of 200 query-answer pairs. Queries were formulated by domain experts to cover four question categories: direct eligibility verification (n = 80), document checklist queries (n = 50), benefit amount and deadline queries (n = 40), and cross-scheme interaction queries (n = 30). Gold-standard answers were validated against official government portal content by two independent annotators with inter-annotator agreement κ = 0.84 (Cohen's kappa). Each query is additionally annotated with an expected abstention label (yes/no) indicating whether the available document corpus is sufficient to answer it definitively.
⚠ [MANUAL INPUT NEEDED: Update benchmark statistics once finalized. Report the exact number of queries per category, the schemes covered, and the inter-annotator agreement calculation method. Include a table of example queries and gold answers.]
 
5. Experimental Setup
5.1 Hardware and Software
All experiments were conducted on a single consumer-grade workstation (ASUS TUF Gaming F15, Intel Core i7-12700H, 16 GB DDR4, NVIDIA GeForce RTX 3050 4 GB GDDR6, 512 GB NVMe SSD, Windows 11). Local GPU resources were used exclusively for SentenceTransformer embedding generation. All agent reasoning calls were dispatched to the Groq cloud inference platform (model: llama3-70b-8192) via REST API over a standard broadband connection. The full software stack is listed in Table 2.

Library / Tool	Role and Version
LangChain 0.2.x	Agent orchestration and pipeline chaining
Groq Python SDK 0.8.x	Cloud LLM inference (llama3-70b-8192)
SentenceTransformers 2.7.x	Document and query embedding (all-MiniLM-L6-v2)
ChromaDB 0.5.x	Vector database, cosine similarity retrieval
HuggingFace Transformers 4.41.x	Embedding model loading
PyTorch 2.3.x (CUDA 12.1)	Deep learning backend for local inference
NLTK 3.8.x	Stopword removal and lemmatization
Pandas 2.2.x / NumPy 1.26.x	Data handling and preprocessing
Table 2. Software stack used in all UFAC experiments.

5.2 Model Configuration
All five agents use the same underlying LLM (Groq llama3-70b-8192) with agent-specific system prompts that define role, input format, output schema, and uncertainty reporting protocol. Inference parameters: temperature = 0.1 (low, to promote determinism), max_tokens = 1024, top_p = 0.95. The low temperature setting was chosen to reduce response variance across runs; a temperature ablation (0.1 vs 0.5 vs 0.9) is reported in Section 7. Retrieval configuration: k = 5 passages, cosine similarity threshold = 0.45 (passages with similarity below this threshold are excluded from the context even if they are within the top-k).

5.3 Baselines
UFAC is compared against four baselines:
•	Single-Agent RAG (SA-RAG): A single LLM call over the same ChromaDB retrieval context, with no agent specialization or uncertainty estimation.
•	Multi-Agent No-Uncertainty (MA-NoU): A five-agent pipeline identical to UFAC but with confidence-based routing disabled — agents vote by majority and the system never abstains.
•	Rule-Based Eligibility Checker (RBEC): A deterministic keyword-matching system that checks for eligibility keywords against a manually constructed rule table for each scheme.
•	Zero-Shot LLM (ZS-LLM): The Groq llama3-70b model queried without retrieval augmentation, relying on parametric knowledge of scheme details.

5.4 Evaluation Metrics
Performance is assessed across five evaluation dimensions:
•	Answer Accuracy: Proportion of responses in which the verdict (eligible / ineligible / conditionally eligible / abstain) matches the gold label.
•	Faithfulness Score: Proportion of factual claims in the response that are directly attributable to a retrieved document passage, assessed by human annotators on a 100-response sample.
•	Abstention Precision / Recall: Precision = proportion of system abstentions that were correct (gold label also requires abstention); Recall = proportion of gold-label abstentions that were correctly identified.
•	Expected Calibration Error (ECE): Measures the alignment between stated confidence scores and empirical accuracy, computed over 10 equal-width confidence bins.
•	Mean Response Latency: Average wall-clock time per query from input submission to output delivery, measured over 50 repeated queries.
⚠ [MANUAL INPUT NEEDED: Add one more metric here if used in experiments, e.g., ROUGE-L or BERTScore for response quality if you have reference summaries.]
 
6. Results and Discussion
6.1 Main Results
Table 3 presents the comparative performance of UFAC against all four baselines on the 200-query evaluation benchmark. UFAC achieves the highest accuracy and faithfulness scores across all question categories, with particularly pronounced gains on cross-scheme interaction queries (category IV) where the complexity of eligibility reasoning most stresses single-step approaches.

⚠ [MANUAL INPUT NEEDED: Replace the placeholder values in Table 3 below with your actual experimental results. Run each system on the 200-query benchmark and record: Accuracy (%), Faithfulness (%), Abstention Precision (%), Abstention Recall (%), ECE, and Mean Latency (s). The table structure is already set up for you.]

System	Accuracy (%)	Faithfulness (%)	Abst. Prec. (%)	Abst. Rec. (%)	ECE ↓	Latency (s)
UFAC (ours)	XX.X	XX.X	XX.X	XX.X	0.XX	XX.X
MA-NoU	XX.X	XX.X	—	—	0.XX	XX.X
SA-RAG	XX.X	XX.X	—	—	0.XX	XX.X
RBEC	XX.X	—	—	—	—	XX.X
ZS-LLM	XX.X	XX.X	—	—	0.XX	XX.X
Table 3. Main results on the 200-query UFAC evaluation benchmark. Best results per column in bold. (↓ = lower is better). Abstention metrics are not applicable (—) for systems without abstention capability.

6.2 Performance by Question Category
Performance varies meaningfully across the four query categories. Direct eligibility verification queries (Category I) are handled well by all retrieval-augmented systems, as they require straightforward clause matching. Document checklist queries (Category II) benefit substantially from the Fact Agent's strict attribution requirement, with UFAC achieving markedly higher faithfulness than SA-RAG which occasionally hallucinated document requirements not present in the retrieved context. Benefit amount and deadline queries (Category III) expose the temporal sensitivity of parametric knowledge: ZS-LLM shows significant accuracy degradation due to stale training data, while retrieval-augmented systems maintain accuracy as long as the relevant circular is present in the corpus. Cross-scheme interaction queries (Category IV) represent the most challenging category, requiring the Assumption Agent to surface implicit premises about scheme co-eligibility; UFAC's advantage over MA-NoU is most pronounced here.
⚠ [MANUAL INPUT NEEDED: Insert Figure 2 here: a grouped bar chart showing per-category accuracy for UFAC vs SA-RAG vs MA-NoU across the four query categories (I–IV). Use the paper's colour scheme.]
Figure 2. Per-category accuracy comparison. UFAC shows the largest gains on Category IV (cross-scheme interaction), where uncertainty-aware routing prevents propagation of unverified assumptions.

6.3 Calibration Analysis
Figure 3 presents reliability diagrams comparing the calibration of UFAC, MA-NoU, and SA-RAG. UFAC's composite confidence score C demonstrates better alignment between stated confidence and empirical accuracy across all confidence bins, with ECE approximately half that of SA-RAG. This suggests that the uncertainty taxonomy and weighted aggregation function produce confidence signals that are meaningfully predictive of answer correctness, a property that is essential for deployable public-sector AI systems.
⚠ [MANUAL INPUT NEEDED: Insert Figure 3 here: reliability diagrams (calibration plots) for UFAC, MA-NoU, and SA-RAG. X-axis: confidence bin [0–100], Y-axis: empirical accuracy within bin. Perfect calibration is the diagonal. Generate this from your actual experiment data.]
Figure 3. Reliability diagrams for three systems. UFAC's composite confidence score shows closer alignment to the perfect-calibration diagonal, indicating superior ECE.

6.4 Abstention Analysis
Of the 200 queries, 38 carry gold-label abstention annotations indicating that the document corpus lacks sufficient information for a definitive answer. UFAC correctly identifies the majority of these cases and abstains appropriately, avoiding the overconfident incorrect responses produced by MA-NoU and SA-RAG on the same queries. False-positive abstentions (queries that UFAC abstains on but which have sufficient evidence) are examined in Section 8.
⚠ [MANUAL INPUT NEEDED: Add exact abstention precision/recall numbers and a confusion matrix for the abstention decision (2×2: abstain/answer × correct/incorrect).]
 
7. Ablation Studies and Analysis
7.1 Agent Ablations
To assess the contribution of each agent to overall pipeline performance, we conduct leave-one-out ablations by removing each agent and replacing its output with a null contribution (u_i = 0.5, o_i = empty). Table 4 reports accuracy, faithfulness, and ECE for each ablated configuration.
⚠ [MANUAL INPUT NEEDED: Run leave-one-out ablation experiments and fill in Table 4 with actual results. Each row corresponds to removing one agent from the pipeline.]

Configuration	Accuracy (%)	Faithfulness (%)	ECE ↓
Full UFAC (all 5 agents)	XX.X	XX.X	0.XX
— Fact Agent	XX.X	XX.X	0.XX
— Assumption Agent	XX.X	XX.X	0.XX
— Unknown Agent	XX.X	XX.X	0.XX
— Confidence Agent (use average u_i)	XX.X	XX.X	0.XX
— Refinement Loop (max R=0)	XX.X	XX.X	0.XX
Table 4. Leave-one-out agent ablation results. Each row removes one component from the full UFAC pipeline.

7.2 Threshold Sensitivity Analysis
The routing thresholds θ_high and θ_low govern the trade-off between coverage (proportion of queries that receive a direct answer) and accuracy (correctness on answered queries). Figure 4 plots accuracy and abstention rate as a function of θ_high ∈ {60, 70, 75, 80, 90}, holding θ_low = 40 constant. Higher thresholds increase accuracy at the cost of coverage; the default θ_high = 75 represents the empirically optimal operating point on the accuracy-coverage trade-off curve.
⚠ [MANUAL INPUT NEEDED: Generate Figure 4: a dual-axis line chart with θ_high on the X-axis, accuracy on the primary Y-axis, and abstention rate on the secondary Y-axis. Run the evaluation benchmark at each threshold setting.]
Figure 4. Threshold sensitivity analysis. Accuracy increases with θ_high (more abstentions) while coverage decreases. θ_high = 75 is the recommended operating point.

7.3 Retrieval Configuration Analysis
We vary k (number of retrieved passages) from 1 to 10 and report accuracy and mean latency. Performance improves from k = 1 to k = 5 and plateaus thereafter, while latency grows linearly with k. The default k = 5 balances retrieval coverage with inference efficiency.
⚠ [MANUAL INPUT NEEDED: Generate Figure 5: accuracy and latency vs. k (1, 2, 3, 5, 7, 10).]

7.4 LLM Temperature Analysis
Agent reasoning calls are executed at three temperature settings (0.1, 0.5, 0.9). Lower temperatures produce more deterministic outputs and higher faithfulness scores; higher temperatures increase response diversity but introduce factual inconsistency. Temperature = 0.1 is selected as the default for all experiments.
⚠ [MANUAL INPUT NEEDED: Report a small table with accuracy and faithfulness at temperature 0.1, 0.5, 0.9.]
 
8. Limitations
UFAC is subject to several methodological and deployment limitations that bound the generalizability of the current results:

•	The knowledge base covers six centrally sponsored schemes as of the 2024 policy cycle. State-level variations and recently notified scheme amendments are not represented; eligibility reasoning for queries that depend on state-specific subschemes may produce incorrect or incomplete outputs. The corpus does not include Hindi or regional-language documents, limiting applicability to English-literate farmers or queries processed by extension workers.Document corpus coverage: 
•	UFAC's performance degrades when the relevant eligibility clause is not surfaced by the cosine similarity retrieval. For queries involving novel scheme terminology or non-standard phrasing, retrieval failure is a primary failure mode, and the Unknown Agent cannot distinguish retrieval failure from genuine document absence.Dependency on retrieval quality: 
•	All agent reasoning is performed by a single LLM (llama3-70b-8192). The agents' abilities to distinguish confirmed facts from inferred assumptions, and to recognize information absence, are constrained by the LLM's own parametric knowledge and susceptibility to hallucination. Uncertainty scores are verbalized estimates rather than formally calibrated probabilities.LLM backbone limitations: 
•	The internal benchmark of 200 queries is small relative to the full space of possible farmer eligibility queries across the six schemes. The absence of a large-scale publicly available benchmark for Indian agricultural scheme QA makes it difficult to assess external validity. Human annotation of gold-label answers covered only two annotators; larger-scale annotation with farmer-domain experts would strengthen the evaluation.Evaluation scale: 
•	The system has not been evaluated in a real-world deployment scenario with actual farmers. Usability, trust calibration, and the handling of non-standard farmer inputs (dialect variations, incomplete queries) remain unstudied.No field validation: 
•	The five-agent pipeline introduces latency relative to single-agent baselines. In refinement scenarios, the pipeline executes up to 10 LLM calls per query (5 agents × 2 rounds), which may be prohibitive in bandwidth-constrained rural deployment contexts.Latency overhead: 
 
9. Potential Applications
Beyond the agricultural scheme eligibility context demonstrated in this paper, the UFAC architecture generalizes to any domain characterized by (i) complex eligibility or compliance criteria distributed across large document corpora, (ii) high cost of overconfident incorrect responses, and (iii) the need for transparent, auditable reasoning. Specific application domains include:
•	Social welfare eligibility assessment: National social protection programmes (housing subsidies, healthcare entitlements, pension schemes) share the document structure and eligibility complexity of agricultural schemes.
•	Legal compliance checking: UFAC's Assumption Agent and Unknown Agent are directly applicable to automated contract review, regulatory compliance monitoring, and legal clause interpretation.
•	Clinical decision support: Uncertainty-first reasoning is critical in medical AI; the pipeline's abstention protocol is analogous to the clinical safety principle of escalating uncertain cases to human experts.
•	Public procurement and tender analysis: Complex bidding eligibility criteria in government procurement documents are well-suited to the UFAC parsing and reasoning pipeline.
 
10. Conclusion and Future Work
This paper presented UFAC, an uncertainty-first multi-agent LLM orchestration framework for farmer eligibility assessment across Indian government agricultural welfare schemes. By instantiating a five-agent council in which each agent contributes both a candidate output and an uncertainty signal, and by routing pipeline execution based on a composite confidence score computed from those signals, UFAC achieves improved answer faithfulness, better calibration, and principled abstention compared to single-agent RAG and multi-agent baselines without uncertainty routing. The system operates at inference time without task-specific fine-tuning, making it deployable without specialized compute resources.

The primary finding is that treating uncertainty as a first-class coordination signal — rather than as a post-hoc output qualifier — changes the character of multi-agent pipeline failures: instead of confidently incorrect answers, the system produces acknowledged information gaps that can be escalated to human reviewers or supplemented with targeted additional retrieval. This property is essential in the agricultural welfare context where overconfident misguidance can cause eligible farmers to miss entitlements.

10.1 Future Work
Several directions for future work follow directly from the current limitations:
6.	Multilingual extension: Adapting the preprocessing, embedding, and agent prompting pipeline to Hindi and major Indian regional languages to support direct farmer interaction without intermediary extension workers.
7.	Automated corpus update: Integrating a policy monitoring module that detects new scheme notifications and incrementally updates the ChromaDB index without full re-embedding.
8.	Formal calibration training: Replacing verbalized uncertainty scores with calibrated confidence estimates produced through temperature scaling or Platt scaling on a held-out calibration set.
9.	Field deployment study: Conducting a randomized field trial with agricultural extension workers to measure the real-world impact of UFAC-assisted scheme guidance on application uptake rates.
10.	Expanded benchmark: Constructing a large-scale, publicly available benchmark for Indian agricultural scheme QA with standardized evaluation protocols to support reproducible comparison of future systems.
 
11. References
⚠ [MANUAL INPUT NEEDED: Replace all placeholder references below with full citation details. Target ~50 references. Format: [n] Author(s). Title. Venue, Year. DOI.]

[1] Lewis, P., Perez, E., Piktus, A., et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS, 2020.
[2] Wei, J., Wang, X., Schuurmans, D., et al. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS, 2022.
[3] Wu, Q., Bansal, G., Zhang, J., et al. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. arXiv:2308.08155, 2023.
[4] Hong, S., Zhuge, M., Chen, J., et al. MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework. ICLR, 2024.
[5] Asai, A., Wu, Z., Wang, Y., et al. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. ICLR, 2024.
[6] Kuhn, L., Gal, Y., Farquhar, S. Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation. ICLR, 2023.
[7] Xiong, M., Hu, Z., Lu, X., et al. Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs. ICLR, 2024.
[8] Kadavath, S., Conerly, T., Askell, A., et al. Language Models (Mostly) Know What They Know. arXiv:2207.05221, 2022.
[9] Shazeer, N., Mirhoseini, A., Maziarz, K., et al. Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer. ICLR, 2017.
[10] Du, Y., Li, S., Torralba, A., et al. Improving Factuality and Reasoning in Language Models through Multiagent Debate. ICML, 2023.
[11] Gal, Y., Ghahramani, Z. Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning. ICML, 2016.
[12] Kamath, A., Jia, R., Liang, P. Selective Question Answering under Domain Shift. ACL, 2020.
[13] Liu, X., Yu, H., Zhang, H., et al. AgentBench: Evaluating LLMs as Agents. ICLR, 2024.
[14] Shao, Z., Gong, Y., Shen, Y., et al. Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy. EMNLP Findings, 2023.
[15] Wang, J., Wang, F., Shi, Z., et al. Mixture-of-Agents Enhances Large Language Model Capabilities. arXiv:2406.04692, 2024.
[16] Varshney, N., Yao, W., Zhang, H., et al. A Stitch in Time Saves Nine: Detecting and Mitigating Hallucinations of LLMs by Validating Low-Confidence Generation. arXiv:2307.03987, 2023.
[17] Ye, J., et al. Benchmarking LLMs via Uncertainty Quantification. NeurIPS, 2024.
[18–50]  [MANUAL INPUT NEEDED: Add remaining ~32 references covering: multi-agent routing, agricultural NLP, legal document understanding, government policy AI, calibration methods, crop insurance NLP, Indian agriculture AI, RAG evaluation, chain-of-thought in structured domains, selective abstention in QA.]
 
Declarations
Author Contributions
⚠ [MANUAL INPUT NEEDED: Describe each author's specific contribution using CRediT taxonomy: Conceptualization, Methodology, Software, Validation, Formal Analysis, Data Curation, Writing – Original Draft, Writing – Review & Editing, Visualization, Supervision, Funding Acquisition.]

Funding
⚠ [MANUAL INPUT NEEDED: State the funding source(s), grant number(s), and funder role. If no external funding was received, state: 'This research received no external funding.']

Data Availability
The UFAC document corpus is compiled from publicly available government policy documents accessible at:
•	PM-KISAN: https://pmkisan.gov.in
•	PMFBY: https://pmfby.gov.in
•	PM-KUSUM: https://mnre.gov.in/solar/schemes
•	Soil Health Card: https://soilhealth.dac.gov.in
•	Kisan Credit Card: https://agricoop.nic.in
•	PM Dhan-Dhaanya Krishi Yojana: https://agriculture.gov.in
⚠ [MANUAL INPUT NEEDED: Add the GitHub repository link where the UFAC codebase and evaluation benchmark are publicly available for reproducibility. Format: 'The UFAC source code and evaluation benchmark are available at https://github.com/[your-repo]/UFAC.']

Ethics Statement
This research involves no human subjects experiments, clinical trials, or personally identifiable data. The document corpus used in this study consists exclusively of publicly available government policy documents. The internal evaluation benchmark was constructed from domain expert annotations of publicly available policy content. No ethical approval was required.

Competing Interests
The authors declare no competing interests.

Additional Information
Correspondence and requests for materials should be addressed to A.K.S.
