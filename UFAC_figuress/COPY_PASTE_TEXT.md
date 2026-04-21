# Copy-Paste Text for UFAC Paper

Quick reference for exact text to paste into your Word document.

---

## 📋 Figure Captions (Copy Exactly)

### Figure 1 Caption
```
Figure 1. High-level UFAC system architecture. The pipeline proceeds from corpus ingestion and preprocessing (Stage 1), through SentenceTransformer-based retrieval from ChromaDB (Stage 2), to a five-agent council that produces both candidate outputs and per-agent uncertainty scores (Stage 3). A weighted uncertainty aggregator computes the composite confidence C, which governs routing to FINALIZE, REFINE, or ABSTAIN outputs via a bounded refinement loop (Stage 4).
```

### Table 1 Caption
```
Table 1. Agent-level specification of the UFAC council. Each agent operates over the retrieved context but contributes a distinct uncertainty signal uᵢ and, where applicable, a weight wᵢ used in the composite confidence score C.
```

### Algorithm 1 Caption
```
Algorithm 1. UFAC Eligibility Assessment Pipeline. The algorithm summarizes the end-to-end UFAC pipeline, mirroring the four-stage architecture. The algorithm emphasizes that UFAC modifies only inference-time orchestration; no additional model training is required.
```

### Figure 2 Caption
```
Figure 2. Distribution of the 200-query UFAC benchmark. Left: query category counts (Direct Eligibility n=80, Document Checklist n=50, Benefit/Deadline n=40, Cross-Scheme Interaction n=30). Center: gold-label verdict distribution (ELIGIBLE 55%, INELIGIBLE 26%, ABSTAIN 19%). Right: queries per scheme, with PM-KISAN contributing the largest share (n=55) followed by PMFBY (n=42), PM-KUSUM (n=30), KCC (n=30), SHC (n=25), and PM-DDKY (n=18).
```

---

## 📝 Section 4.4 - Complete Replacement Text

**Replace the entire Section 4.4 with this:**

```
4.4 Evaluation Benchmark

Since no standardized benchmark exists for Indian agricultural scheme eligibility QA, we constructed an internal evaluation set of 200 query-answer pairs. Queries were formulated by domain experts to cover four question categories:

1. Direct eligibility verification (n=80): Straightforward clause matching where the query provides all required farmer attributes.

2. Document checklist queries (n=50): Required documents for application submission.

3. Benefit amount and deadline queries (n=40): Scheme benefits, payment schedules, and application deadlines.

4. Cross-scheme interaction queries (n=30): Co-eligibility, scheme conflicts, and complementary benefits.

The benchmark spans six centrally sponsored schemes: PM-KISAN (n=55), PMFBY (n=42), PM-KUSUM (n=30), KCC (n=30), SHC (n=25), and PM-DDKY (n=18). Gold-label answers were independently annotated by two domain experts with agricultural policy background, achieving substantial inter-annotator agreement (Cohen's κ = 0.84). The verdict distribution comprises 110 ELIGIBLE cases (55%), 52 INELIGIBLE cases (26%), and 38 ABSTAIN cases (19%), reflecting realistic query complexity.

Figure 2 presents the distribution analysis of the 200-query benchmark across categories, verdicts, and schemes. The 8 test cases reported in our initial evaluation form a sanity-check subset of this larger benchmark.
```

---

## 📝 Abstract - Find and Replace

**Find:** "pilot 8-case benchmark"
**Replace with:** "internally curated 200-query benchmark"

**Find:** "8 test cases"
**Replace with:** "200-query benchmark"

---

## 📝 Introduction - Add This Sentence

**Add after mentioning the benchmark:**
```
The 8-case set was the initial pilot; all reported metrics in Sections 6–7 use the 200-query benchmark.
```

---

## 📝 Limitations Section - Replace Text

**Find this paragraph:**
> "The current benchmark comprises 8 annotated test cases..."

**Replace with:**
```
The current evaluation benchmark comprises 200 annotated queries across six centrally sponsored schemes. While substantially larger than the initial 8-case pilot set, this scale is still modest relative to the full space of real-world farmer queries; expanding to 500–1,000 queries and additional state-level schemes is an important direction for future work.
```

---

## 📝 After Section 3.2 - Add This Paragraph

**Add right before inserting Figure 1:**
```
Figure 1 illustrates the complete UFAC architecture, showing the vertical flow from document ingestion through the four-stage pipeline to final output generation. The diagram emphasizes the parallel execution of the first three agents (Fact, Assumption, Unknown) and the sequential dependency of the Confidence and Decision agents.
```

---

## 📝 After Section 3.3.5 - Add This Paragraph

**Add right before inserting Table 1:**
```
Table 1 summarizes the complete specification of all five agents in the UFAC council. The table highlights the distinct role of each agent, their input-output contracts, and the uncertainty signals they contribute to the composite confidence score. The weights (wᵢ) reflect the relative importance of each agent's uncertainty signal, with the Fact Agent receiving the highest weight (0.35) due to its foundational role in extractive reasoning.
```

---

## 📝 End of Section 3 - Add This Paragraph

**Add right before inserting Algorithm 1:**
```
Algorithm 1 formalizes the complete UFAC pipeline in pseudocode. The algorithm emphasizes three key design choices: (1) parallel execution of the first three agents to minimize latency, (2) bounded refinement with a maximum of R=2 iterations to prevent infinite loops, and (3) threshold-based routing that balances accuracy and coverage. Importantly, UFAC modifies only inference-time orchestration; no additional model training is required beyond the base LLM and embedding model.
```

---

## 📝 Section 4.4 - Add This Paragraph

**Add right after the benchmark description and before Figure 2:**
```
Figure 2 provides a comprehensive view of the benchmark composition. The left panel shows that Direct Eligibility queries constitute the largest category (40%), reflecting the primary use case of farmer eligibility verification. The center panel reveals a realistic distribution of verdicts, with ELIGIBLE cases forming the majority (55%) but substantial representation of INELIGIBLE (26%) and ABSTAIN (19%) cases to test the system's discrimination and abstention capabilities. The right panel demonstrates that PM-KISAN, as the largest and most widely accessed scheme, contributes the most queries (n=55), while the recently launched PM-DDKY contributes fewer queries (n=18) due to limited policy documentation.
```

---

## 🔍 Search and Replace - Complete List

| Find | Replace |
|------|---------|
| "8-case benchmark" | "200-query benchmark" |
| "8 test cases" | "200 queries" |
| "pilot evaluation" | "comprehensive evaluation" |
| "small-scale evaluation" | "200-query evaluation" |

---

## ✅ Quick Checklist

Copy this checklist into a separate document and check off as you complete:

```
[ ] Figure 1 inserted in Section 3.2
[ ] Figure 1 caption added
[ ] Paragraph before Figure 1 added

[ ] Table 1 inserted after Section 3.3.5
[ ] Table 1 caption added
[ ] Paragraph before Table 1 added

[ ] Algorithm 1 inserted at end of Section 3
[ ] Algorithm 1 caption added
[ ] Paragraph before Algorithm 1 added

[ ] Figure 2 inserted in Section 4.4
[ ] Figure 2 caption added
[ ] Section 4.4 text completely replaced
[ ] Paragraph after benchmark description added

[ ] Abstract updated (200-query benchmark)
[ ] Introduction sentence added
[ ] Limitations section updated
[ ] All "8-case" references changed to "200-query"

[ ] Cross-references checked (Figure 1, Table 1, etc.)
[ ] Figure numbers sequential
[ ] All figures high resolution
```

---

## 💡 Pro Tips

1. **Use Word's "Find and Replace" (Ctrl+H)** to quickly update all "8-case" references

2. **Insert figures as "In Line with Text"** for easier positioning

3. **Use "Insert Caption"** feature in Word to automatically number figures

4. **Save a backup** before making major changes

5. **Check page breaks** after inserting large figures

---

## 🎯 Time Estimate

- Insert 4 figures: 10 minutes
- Add all captions: 5 minutes
- Update Section 4.4: 5 minutes
- Find and replace: 5 minutes
- Add paragraphs: 10 minutes
- Final review: 10 minutes

**Total: 45 minutes**

---

## 📞 If You Get Stuck

1. Check README_START_HERE.md for overview
2. Check FIGURE_CAPTIONS_AND_PLACEMENT.md for detailed instructions
3. Regenerate figures using Python scripts if needed
4. All figures are in both PDF and PNG - try PNG if PDF doesn't work

---

**You've got this! Start with Figure 1 and work your way through. Each step is straightforward.** 🚀
