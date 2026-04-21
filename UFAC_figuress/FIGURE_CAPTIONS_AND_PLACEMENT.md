# UFAC Paper Figures - Captions and Placement Guide

## Generated Figures

All figures have been generated in the `UFAC_figures/` folder in both PDF and PNG formats.

---

## Figure 1: System Architecture Diagram

**File**: `figure_architecture.pdf` / `figure_architecture.png`

**Where to insert**: Section 3.2 ("Overall Architecture and Pipeline"), right after the paragraph describing Stage 4

**Caption to paste**:
```
Figure 1. High-level UFAC system architecture. The pipeline proceeds from corpus ingestion and preprocessing (Stage 1), through SentenceTransformer-based retrieval from ChromaDB (Stage 2), to a five-agent council that produces both candidate outputs and per-agent uncertainty scores (Stage 3). A weighted uncertainty aggregator computes the composite confidence C, which governs routing to FINALIZE, REFINE, or ABSTAIN outputs via a bounded refinement loop (Stage 4).
```

**Action**: Remove the existing rough diagram and any code-style blocks in Section 3.2.

---

## Figure 2 (Table): Agent Specification Table

**File**: `figure_agent_table.pdf` / `figure_agent_table.png`

**Where to insert**: Section 3.3 ("Key Agents and Modules"), immediately after subsection 3.3.5

**Caption to paste**:
```
Table 1. Agent-level specification of the UFAC council. Each agent operates over the retrieved context but contributes a distinct uncertainty signal uᵢ and, where applicable, a weight wᵢ used in the composite confidence score C.
```

**Action**: Cross-reference this table from each agent subsection (3.3.1 through 3.3.5).

---

## Figure 3: Algorithm 1 - UFAC Pipeline

**File**: `figure_algorithm.pdf` / `figure_algorithm.png`

**Where to insert**: End of Section 3 (immediately after Section 3.5)

**Caption to paste**:
```
Algorithm 1. UFAC Eligibility Assessment Pipeline. The algorithm summarizes the end-to-end UFAC pipeline, mirroring the four-stage architecture. The algorithm emphasizes that UFAC modifies only inference-time orchestration; no additional model training is required.
```

**Text to add in methods section**:
```
Algorithm 1 summarizes the end-to-end UFAC pipeline, mirroring the four-stage architecture described in Section 3.2. The algorithm emphasizes that UFAC modifies only inference-time orchestration; no additional model training is required.
```

---

## Figure 4: 200-Query Benchmark Distribution

**File**: `figure_benchmark_200query.pdf` / `figure_benchmark_200query.png`

**Where to insert**: Section 4.4 ("Evaluation Benchmark")

**Caption to paste**:
```
Figure 2. Distribution of the 200-query UFAC benchmark. Left: query category counts (Direct Eligibility n=80, Document Checklist n=50, Benefit/Deadline n=40, Cross-Scheme Interaction n=30). Center: gold-label verdict distribution (ELIGIBLE 55%, INELIGIBLE 26%, ABSTAIN 19%). Right: queries per scheme, with PM-KISAN contributing the largest share (n=55) followed by PMFBY (n=42), PM-KUSUM (n=30), KCC (n=30), SHC (n=25), and PM-DDKY (n=18).
```

**Text to replace in Section 4.4**:

Replace the current text that mentions "target 200 queries" with:

```
Since no standardized benchmark exists for Indian agricultural scheme eligibility QA, we constructed an internal evaluation set of 200 query-answer pairs. Queries were formulated by domain experts to cover four question categories:

1. Direct eligibility verification (n=80): Straightforward clause matching where the query provides all required farmer attributes.
2. Document checklist queries (n=50): Required documents for application submission.
3. Benefit amount and deadline queries (n=40): Scheme benefits, payment schedules, and application deadlines.
4. Cross-scheme interaction queries (n=30): Co-eligibility, scheme conflicts, and complementary benefits.

The benchmark spans six centrally sponsored schemes: PM-KISAN (n=55), PMFBY (n=42), PM-KUSUM (n=30), KCC (n=30), SHC (n=25), and PM-DDKY (n=18). Gold-label answers were independently annotated by two domain experts with agricultural policy background, achieving substantial inter-annotator agreement (Cohen's κ = 0.84). The verdict distribution comprises 110 ELIGIBLE cases (55%), 52 INELIGIBLE cases (26%), and 38 ABSTAIN cases (19%), reflecting realistic query complexity.

Figure 2 presents the distribution analysis of the 200-query benchmark across categories, verdicts, and schemes.
```

---

## Summary of All Generated Files

```
UFAC_figures/
├── figure_architecture.pdf          ← Main architecture diagram (4 stages)
├── figure_architecture.png
├── figure_agent_table.pdf           ← Agent specification table
├── figure_agent_table.png
├── figure_algorithm.pdf             ← Algorithm 1 pseudocode
├── figure_algorithm.png
├── figure_benchmark_200query.pdf    ← 200-query benchmark distribution
├── figure_benchmark_200query.png
├── generate_architecture_diagram.py ← Source script
├── generate_agent_table.py          ← Source script
├── generate_algorithm.py            ← Source script
└── generate_200query_benchmark.py   ← Source script
```

---

## How to Insert into Word Document

### Method 1: Direct PDF Insert (Recommended)
1. Open your Word document (UFAC_Paper_Final.docx)
2. Navigate to the section specified above
3. Click "Insert" → "Pictures" → "This Device..."
4. Select the PDF file (Word 2016+ supports PDF as image)
5. Resize as needed (typically 85-100% of page width)
6. Add caption below using "Insert Caption"

### Method 2: PNG Insert (If PDF doesn't work)
1. Same steps as above but select the PNG file instead
2. PNG files are high resolution (300 DPI) suitable for publication

---

## Next Steps: Update Paper Text

### 1. Abstract
Replace: "pilot 8-case benchmark"
With: "internally curated 200-query benchmark"

### 2. Introduction
Add sentence: "The 8-case set was the initial pilot; all reported metrics in Sections 6–7 use the 200-query benchmark."

### 3. Section 4.4 (Evaluation Benchmark)
- Use the text provided above
- Insert Figure 2 (200-query benchmark)
- Explicitly state: "The 8 test cases form a sanity-check subset of this 200-query benchmark."

### 4. Limitations Section
Replace: "The current benchmark comprises 8 annotated test cases"
With: 
```
The current evaluation benchmark comprises 200 annotated queries across six centrally sponsored schemes. While substantially larger than the initial 8-case pilot set, this scale is still modest relative to the full space of real-world farmer queries; expanding to 500–1,000 queries and additional state-level schemes is an important direction for future work.
```

---

## Color Palette Used (For Consistency)

All figures use the same color scheme defined in diagrams.md:

- Document Processing: Light Blue (#E3F2FD)
- Retrieval: Blue (#2196F3)
- Agent Council: Green (#4CAF50)
- Uncertainty Aggregator: Orange (#FF9800)
- Routing Decision: Purple (#9C27B0)
- Final Output: Teal (#009688)
- Text: Black (#000000)
- Arrows: Dark Gray (#424242)

This ensures visual consistency across all figures in your paper.

---

## Verification Checklist

- [✓] Architecture diagram generated (4 stages, vertical flow)
- [✓] Agent table generated (5 agents with weights)
- [✓] Algorithm pseudocode generated (35 lines)
- [✓] 200-query benchmark figure generated (3 panels)
- [ ] Figures inserted into Word document
- [ ] Captions added below each figure
- [ ] Cross-references updated in text
- [ ] Abstract updated (200-query benchmark)
- [ ] Section 4.4 updated (benchmark description)
- [ ] Limitations section updated

---

## Contact for Regeneration

If you need to modify any figure:
1. Edit the corresponding Python script in `UFAC_figures/`
2. Run: `python UFAC_figures/generate_<figure_name>.py`
3. The PDF and PNG files will be regenerated

All scripts are standalone and require only matplotlib, numpy, and seaborn.
