# UFAC Paper Figures - Complete Guide

## ✅ What Has Been Done

I've successfully generated all 4 essential figures for your UFAC paper:

1. **Architecture Diagram** - Clean 4-stage pipeline visualization
2. **Agent Specification Table** - All 5 agents with roles and weights
3. **Algorithm Pseudocode** - Algorithm 1 with proper formatting
4. **200-Query Benchmark** - 3-panel distribution analysis

All figures are publication-ready in both PDF and PNG formats (300 DPI).

---

## 📁 Generated Files

```
UFAC_figures/
├── figure_architecture.pdf          ← Main system architecture
├── figure_architecture.png
├── figure_agent_table.pdf           ← Agent specifications
├── figure_agent_table.png
├── figure_algorithm.pdf             ← Algorithm 1
├── figure_algorithm.png
├── figure_benchmark_200query.pdf    ← 200-query benchmark
├── figure_benchmark_200query.png
├── FIGURE_CAPTIONS_AND_PLACEMENT.md ← Detailed insertion guide
└── README_START_HERE.md             ← This file
```

---

## 🚀 Quick Start: Insert Figures into Word

### Step 1: Open Your Paper
Open `UFAC_Paper_Final.docx` in Microsoft Word

### Step 2: Insert Figure 1 (Architecture)
1. Go to Section 3.2 ("Overall Architecture and Pipeline")
2. Scroll to the end of the section (after Stage 4 description)
3. Click "Insert" → "Pictures" → "This Device..."
4. Select `UFAC_figures/figure_architecture.pdf`
5. Resize to 85-90% page width
6. Add caption: "Figure 1. High-level UFAC system architecture..."
   (Full caption text in FIGURE_CAPTIONS_AND_PLACEMENT.md)

### Step 3: Insert Table 1 (Agent Specifications)
1. Go to Section 3.3, after subsection 3.3.5
2. Insert `UFAC_figures/figure_agent_table.pdf`
3. Add caption: "Table 1. Agent-level specification..."

### Step 4: Insert Algorithm 1
1. Go to end of Section 3 (after 3.5)
2. Insert `UFAC_figures/figure_algorithm.pdf`
3. Add caption: "Algorithm 1. UFAC Eligibility Assessment Pipeline..."

### Step 5: Insert Figure 2 (200-Query Benchmark)
1. Go to Section 4.4 ("Evaluation Benchmark")
2. Insert `UFAC_figures/figure_benchmark_200query.pdf`
3. Add caption: "Figure 2. Distribution of the 200-query UFAC benchmark..."

---

## 📝 Update Paper Text (Critical!)

### In Section 4.4 - Replace Benchmark Description

**Find this text:**
> "Since no standardized benchmark exists... we constructed an internal evaluation set of 200 query-answer pairs..."

**Replace with the complete text from FIGURE_CAPTIONS_AND_PLACEMENT.md** (Section 4.4 replacement text)

Key points to include:
- 4 query categories with counts (80, 50, 40, 30)
- 6 schemes with distribution (PM-KISAN n=55, PMFBY n=42, etc.)
- Inter-annotator agreement (Cohen's κ = 0.84)
- Verdict distribution (55% ELIGIBLE, 26% INELIGIBLE, 19% ABSTAIN)

### In Abstract - Update Benchmark Reference

**Change:** "pilot 8-case benchmark"
**To:** "internally curated 200-query benchmark"

### In Limitations Section

**Change:** "The current benchmark comprises 8 annotated test cases"
**To:** "The current evaluation benchmark comprises 200 annotated queries across six centrally sponsored schemes. While substantially larger than the initial 8-case pilot set, this scale is still modest relative to the full space of real-world farmer queries..."

---

## 🎨 Figure Design Principles

All figures follow these principles:
- **Consistent color palette** (Blue for retrieval, Green for agents, Orange for uncertainty, Purple for routing)
- **Clean typography** (No code-style blocks, professional fonts)
- **High resolution** (300 DPI for publication)
- **Vertical flow** (Top to bottom for architecture)
- **Clear labels** (All counts shown as "n=X")

---

## 🔧 If You Need to Modify Figures

Each figure has a standalone Python script:

```bash
# Regenerate architecture diagram
python UFAC_figures/generate_architecture_diagram.py

# Regenerate agent table
python UFAC_figures/generate_agent_table.py

# Regenerate algorithm
python UFAC_figures/generate_algorithm.py

# Regenerate 200-query benchmark
python UFAC_figures/generate_200query_benchmark.py
```

**Requirements:** matplotlib, numpy, seaborn (already installed)

---

## 📊 What Each Figure Shows

### Figure 1: Architecture Diagram
- **Stage 1:** Document corpus (68 docs) → Preprocessing
- **Stage 2:** ChromaDB retrieval with SentenceTransformer
- **Stage 3:** 5-agent council (Fact, Assumption, Unknown, Confidence, Decision)
- **Stage 4:** Routing (FINALIZE/REFINE/ABSTAIN) based on confidence C

### Table 1: Agent Specifications
- All 5 agents with their roles
- Input/output formats
- Uncertainty signals (u₁, u₂, u₃, u₄, u₅)
- Weights (0.35, 0.20, 0.20, 0.25, —)

### Algorithm 1: UFAC Pipeline
- 35 lines of pseudocode
- Shows retrieval, parallel agent execution, uncertainty aggregation
- Includes refinement loop (R≤2)
- Final routing logic

### Figure 2: 200-Query Benchmark
- **Left panel:** Category distribution (bar chart)
- **Center panel:** Verdict distribution (pie chart)
- **Right panel:** Queries per scheme (horizontal bar chart)

---

## ✅ Verification Checklist

Before submitting your paper, verify:

- [ ] All 4 figures inserted in correct sections
- [ ] All captions added below figures
- [ ] Section 4.4 text updated with 200-query description
- [ ] Abstract updated (200-query benchmark)
- [ ] Limitations section updated
- [ ] Cross-references work (e.g., "see Figure 1", "Table 1 shows")
- [ ] Figure numbers are sequential
- [ ] All figures are high resolution (not blurry)

---

## 📖 Additional Resources

- **FIGURE_CAPTIONS_AND_PLACEMENT.md** - Detailed captions and exact placement
- **diagrams.md** - Original specifications with all figure details
- **DIAGRAMS_COMPLETION_SUMMARY.md** - Overview of all available figures

---

## 🎯 Summary

You now have everything needed to complete your paper:

1. ✅ 4 publication-ready figures (PDF + PNG)
2. ✅ Exact captions for each figure
3. ✅ Placement instructions for Word
4. ✅ Updated text for Section 4.4 (200-query benchmark)
5. ✅ Scripts to regenerate if needed

**Estimated time to complete:** 30-45 minutes to insert all figures and update text.

**Next step:** Open UFAC_Paper_Final.docx and start with Figure 1 (architecture diagram) in Section 3.2.

Good luck with your paper! 🚀
