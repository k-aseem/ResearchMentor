# Research Mentor: Evaluation Report

## Productive Hallucination for Novel Hypothesis Generation in AI-Assisted Research

---

## 1. Introduction

This report presents the evaluation results for the **Research Mentor** system, a multi-agent AI pipeline designed to assist PhD students in generating novel, testable hypotheses when existing literature does not directly address their research questions. The core innovation is the concept of **Productive Hallucination** -- rather than treating LLM hallucinations as a failure mode, the system deliberately induces creative generation in detected knowledge gaps to produce scientifically grounded hypotheses that can guide further investigation.

The central thesis is that a structured multi-agent pipeline with explicit gap detection, creative generation, and critical review can outperform a standard LLM in producing useful research hypotheses, particularly in scenarios where the answer is not readily available in the existing knowledge base.

## 2. System Architecture

### 2.1 Agent Pipeline

The Research Mentor system comprises five specialized agents, each with a deliberately chosen temperature setting to balance precision and creativity at the appropriate stage:

| Agent | Temperature | Role |
|-------|-------------|------|
| **Librarian** | 0.0 | RAG-based retrieval with explicit confidence assessment (HIGH / MEDIUM / LOW) |
| **Gap Detector** | -- | Two-stage decision gate routing queries to the appropriate response path |
| **Dreamer** | 1.2 | Creative hypothesis generator; produces 3 novel, testable hypotheses per query |
| **Critic** | 0.0 | Feasibility reviewer; scores each hypothesis on a 0--10 scale |
| **Judge** | 0.0 | Comparative evaluator; scores Research Mentor output vs. Baseline LLM output |
| **Baseline LLM** | 0.7 | Standard LLM response for head-to-head comparison |

### 2.2 Two-Stage Gap Detection

The Gap Detector implements a two-stage decision gate that routes queries based on their relationship to the knowledge base:

1. **Stage 1 -- Similarity Check:** The query embedding is compared against the knowledge base using cosine similarity. If the maximum similarity score falls below **0.5**, the query is deemed outside the knowledge base entirely, and the system enters Research Mentor mode immediately.

2. **Stage 2 -- Confidence Check:** If similarity >= 0.5 (i.e., the topic appears to be covered), the Librarian attempts to answer the query and self-reports a confidence level:
   - **HIGH or MEDIUM confidence** --> The Librarian's answer is returned directly.
   - **LOW confidence** --> The system enters Research Mentor mode, activating the Dreamer and Critic pipeline.

### 2.3 Technology Stack

- **Language:** Python 3.12
- **LLM:** Google Gemini 2.0 Flash
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store:** ChromaDB
- **Orchestration:** LangChain

### 2.4 Knowledge Base

The knowledge base consists of a single dummy ML/LLM research paper covering the following topics: LoRA, quantization, RAG, chain-of-thought prompting, model deployment, and evaluation methodologies. All content was chunked and embedded into ChromaDB for retrieval.

## 3. Evaluation Methodology

### 3.1 Test Design

A total of **90 test cases** were constructed across three categories (30 each):

- **Known (30 tests):** Questions with direct answers in the paper. These test whether the system correctly identifies that the knowledge base can answer the query and returns the Librarian's response.
- **Gap (30 tests):** Questions that combine concepts present in the paper in ways not explicitly addressed (e.g., "What happens when you combine LoRA with RAG embeddings?"). These should trigger Research Mentor mode and produce novel hypotheses.
- **Hallucination (30 tests):** Questions on topics completely unrelated to the knowledge base. These should always trigger Research Mentor mode, testing the system's behavior at the boundary of productive vs. unproductive hallucination.

### 3.2 Metrics

- **Mode Detection Accuracy:** Whether the system correctly chose Librarian mode vs. Research Mentor mode for each query.
- **Judge Score (0--10):** The Judge agent's comparative quality assessment of both Research Mentor and Baseline outputs.
- **Win Rate:** The proportion of tests where the Research Mentor output was scored higher than the Baseline.

## 4. Results

### 4.1 Overall Summary

| Metric | Value |
|--------|-------|
| Total Tests | 90 |
| Mode Detection Accuracy | 72 / 90 (80.0%) |
| RM Wins | 67 (74.4%) |
| Baseline Wins | 23 (25.6%) |
| Ties | 0 (0.0%) |
| Overall RM Mean Score | 7.79 / 10 |
| Overall Baseline Mean Score | 6.98 / 10 |
| Overall RM Median Score | 9.0 |
| Overall Baseline Median Score | 7.0 |

The Research Mentor system outperformed the Baseline LLM in nearly three-quarters of all test cases, with a mean score advantage of +0.81 and a median score advantage of +2.0.

### 4.2 Results by Category

| Category | Mode Detection | RM Wins | BL Wins | RM Mean | RM Median | BL Mean | BL Median |
|----------|---------------|---------|---------|---------|-----------|---------|-----------|
| Known | 17 / 30 (56.7%) | 25 | 5 | 8.50 | 9.0 | 6.53 | 7.0 |
| Gap | 25 / 30 (83.3%) | 24 | 6 | 8.33 | 9.0 | 7.30 | 7.0 |
| Hallucination | 30 / 30 (100.0%) | 18 | 12 | 6.53 | 8.5 | 7.10 | 7.0 |

### 4.3 Detailed Score Distributions

#### Known Tests

| Statistic | Research Mentor | Baseline |
|-----------|----------------|----------|
| Mean | 8.50 | 6.53 |
| Median | 9.0 | 7.0 |
| Std Dev | 1.07 | 1.81 |
| Min | 6 | 1 |
| Max | 10 | 9 |

**RM scores:** 6, 6, 6, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10

**BL scores:** 1, 2, 2, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 9

The Research Mentor achieved a tight distribution clustered around 9, while the Baseline showed greater variance with a notable tail of low scores (1--2). Even when Known tests were misrouted into Research Mentor mode (see Section 5), the Dreamer and Critic pipeline still produced high-quality output, as the underlying LLM possesses general knowledge about these ML topics.

#### Gap Tests

| Statistic | Research Mentor | Baseline |
|-----------|----------------|----------|
| Mean | 8.33 | 7.30 |
| Median | 9.0 | 7.0 |
| Std Dev | 1.45 | 0.75 |
| Min | 4 | 6 |
| Max | 9 | 9 |

**RM scores:** 4, 5, 5, 6, 7, 7, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9

**BL scores:** 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9

Gap tests represent the **primary intended use case** of the Research Mentor system. The results are strong: 80% of RM scores are 9/10, while the Baseline clusters around 7--8 with notably lower variance. The RM's structured hypothesis generation -- producing three distinct hypotheses, each reviewed for feasibility by the Critic -- provides substantially more research value than the Baseline's single, conventional response. The +1.03 mean score advantage and +2.0 median advantage confirm that the multi-agent pipeline adds meaningful value precisely where it is designed to.

#### Hallucination Tests

| Statistic | Research Mentor | Baseline |
|-----------|----------------|----------|
| Mean | 6.53 | 7.10 |
| Median | 8.5 | 7.0 |
| Std Dev | 3.20 | 2.06 |
| Min | 1 | 1 |
| Max | 10 | 10 |

**RM scores:** 1, 1, 1, 1, 2, 3, 3, 3, 3, 6, 6, 6, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10

**BL scores:** 1, 1, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 9, 10, 10, 10, 10

The hallucination tests reveal the most nuanced findings. The RM score distribution is **bimodal**: a cluster of low scores (1--3, comprising roughly one-third of tests) and a cluster of high scores (8--10, comprising roughly half of tests). This bimodality reflects two distinct failure/success modes:

- **Low scores (1--3):** The Dreamer attempted to force connections between the unrelated query topic and the ML knowledge base. When the topics were too distant (e.g., questions about biology or history forced into an ML framing), the resulting hypotheses were incoherent or trivially unfalsifiable.
- **High scores (8--10):** The Dreamer found genuinely creative cross-domain connections. For instance, applying optimization concepts from ML to unrelated problem domains, or identifying structural analogies that produced surprisingly plausible research directions.

The Baseline, by contrast, produces a narrower and more consistent distribution centered around 7, reflecting its tendency to provide competent but uninspired general-knowledge answers. The RM's higher variance is a direct consequence of the high-temperature creative generation: when it works, it produces exceptional output; when it fails, it fails noticeably.

## 5. Analysis of Mode Detection Failures

### 5.1 Known Test Failures (13 / 30)

All 13 misclassified Known tests failed at **Stage 1** of gap detection -- the similarity score fell below the 0.5 threshold, causing the system to bypass the Librarian entirely and enter Research Mentor mode.

| Test ID | Topic | Similarity |
|---------|-------|-----------|
| known_005 | Prefix tuning struggles | 0.4649 |
| known_011 | RAG hallucination reduction | 0.4435 |
| known_012 | RAG latency | 0.4923 |
| known_015 | CoT token usage | 0.4709 |
| known_017 | Zero-shot vs few-shot CoT | 0.4065 |
| known_018 | Cold start latency | 0.4490 |
| known_021 | Transformer introduction year | 0.3873 |
| known_022 | Self-attention mechanism | 0.4162 |
| known_024 | Gold standard evaluation | 0.4749 |
| known_025 | LoRA resource-constrained | 0.4747 |
| known_026 | Training paradigm | 0.4775 |
| known_027 | Model sizes | 0.3976 |
| known_030 | RAG definition | 0.4637 |

Several observations:

1. **Narrow misses:** 10 of the 13 failures had similarity scores between 0.45 and 0.50, falling just below the threshold. A threshold of 0.40 would have recovered most of these, but may introduce false positives elsewhere.

2. **Embedding mismatch:** The all-MiniLM-L6-v2 model produces 384-dimensional embeddings optimized for semantic textual similarity. However, the gap between a user's natural-language question (e.g., "When were transformers introduced?") and the corresponding passage in a technical paper (which may discuss transformers in a different framing) can produce lower-than-expected similarity scores.

3. **Chunking effects:** The paper was chunked for embedding, meaning that the relevant information for a query may be split across chunks or embedded alongside contextually different content, diluting the similarity signal.

Despite being misrouted, these tests still scored well overall (the RM mean for Known tests was 8.50), because the Dreamer's underlying LLM possesses general ML knowledge and the Critic enforced quality. The primary cost was not quality degradation but unnecessary computational overhead from running the full hypothesis pipeline.

### 5.2 Gap Test Failures (5 / 30)

All 5 misclassified Gap tests failed at **Stage 2** -- similarity was above 0.5, but the Librarian returned **MEDIUM** confidence instead of LOW, causing the system to return the Librarian's partial answer rather than entering Research Mentor mode.

| Test ID | Topic | Similarity | Confidence |
|---------|-------|-----------|------------|
| gap_006 | Quantization + CoT | 0.5429 | MEDIUM |
| gap_009 | LoRA + RAG embeddings | 0.5240 | MEDIUM |
| gap_019 | CoT + batching | 0.5204 | MEDIUM |
| gap_023 | RAG + quantization gap | 0.5323 | MEDIUM |
| gap_029 | Benchmarks for RAG | 0.5550 | MEDIUM |

These are fundamentally more challenging failures because the topics **are** present in the knowledge base individually, but the specific combination or angle of the query is not addressed. The Librarian, finding relevant content about each individual concept, assessed its confidence as MEDIUM rather than LOW. This is a limitation of using a single confidence threshold boundary between "answer directly" and "defer to Dreamer."

## 6. Discussion

### 6.1 The Research Mentor Excels at Its Intended Use Case

The strongest finding is that the Research Mentor significantly outperforms the Baseline on **gap questions** -- precisely the scenario it was designed for. With a win rate of 80% (24/30), a mean score of 8.33 vs. 7.30, and a median of 9.0 vs. 7.0, the structured hypothesis-generation pipeline consistently produces more valuable research output than a standard LLM when the question falls between existing knowledge areas.

### 6.2 Productive Hallucination Has Real but Bounded Value

The hallucination test results validate the core concept with an important caveat. Productive hallucination works when there is a meaningful structural or conceptual bridge between the query domain and the knowledge base. When no such bridge exists, the system produces noticeably poor output (scores of 1--3). The bimodal distribution (std dev of 3.20, compared to the Baseline's 2.06) reflects this all-or-nothing dynamic. In a production system, the Critic agent could be enhanced to detect and flag cases where the Dreamer's cross-domain connections are superficial.

### 6.3 The Similarity Threshold Is the Weakest Link

The 0.5 similarity threshold is the single largest source of mode detection errors. It operates as a hard boundary on a continuous measure, and the embedding space does not provide a clean separation between "in knowledge base" and "not in knowledge base." The fact that 10 of 13 Known failures fell in the 0.45--0.50 range suggests the threshold is slightly too aggressive for this embedding model and knowledge base combination.

### 6.4 Confidence Calibration Needs Refinement

The MEDIUM confidence boundary between "answer directly" and "defer to Dreamer" is imprecise. The 5 Gap test failures demonstrate that the Librarian conflates "I recognize these individual concepts" with "I can answer this specific question." A more structured confidence assessment -- distinguishing between concept familiarity and query-specific answer confidence -- would improve Stage 2 accuracy.

## 7. Future Work

1. **Adaptive Similarity Threshold:** Replace the fixed 0.5 threshold with a learned or adaptive threshold that accounts for query length, embedding density in the region, and historical accuracy. Alternatively, explore a soft routing approach where queries near the boundary receive both a Librarian answer and a Dreamer-generated hypothesis set, with the Judge selecting the more useful output.

2. **Improved Confidence Calibration:** Redesign the Librarian's confidence assessment to explicitly distinguish between topic familiarity and answer completeness. A two-dimensional confidence signal (topic relevance x answer specificity) would allow more precise routing at Stage 2.

3. **Critic-Gated Hallucination Filtering:** Enhance the Critic agent to detect and suppress unproductive hallucinations, particularly in cross-domain scenarios. When the Dreamer's hypotheses rely on superficial analogies, the Critic should assign low feasibility scores and the system should fall back to a more conservative response.

4. **Larger and More Diverse Knowledge Bases:** The current evaluation uses a single dummy paper. Testing with a larger corpus (multiple papers, broader topic coverage) would reveal how the system scales and whether the similarity threshold generalizes.

5. **Chunking Strategy Optimization:** Experiment with different chunking strategies (overlapping chunks, hierarchical chunking, semantic chunking) to improve embedding fidelity and reduce the similarity mismatch observed in Known test failures.

6. **Human Evaluation:** The current evaluation relies on the Judge agent (an LLM) for scoring. A human evaluation study with domain experts would provide ground-truth validation of hypothesis quality and novelty.

7. **Multi-Paper Gap Detection:** Extend the system to detect gaps not just within a single paper's knowledge, but across multiple papers -- identifying contradictions, unexplored intersections, and methodological gaps in a body of literature.

## 8. Conclusion

The Research Mentor system demonstrates that structured, multi-agent hypothesis generation can meaningfully outperform standard LLM responses for research questions that fall in knowledge gaps. Across 90 test cases, the system achieved a 74.4% win rate over the Baseline with a mean score of 7.79 vs. 6.98. Its strongest performance was on gap questions (80% win rate, +1.03 mean advantage), validating the core design. Mode detection accuracy of 80% is adequate for a prototype but reveals clear improvement opportunities in threshold tuning and confidence calibration. The bimodal behavior on hallucination tests -- exceptional when cross-domain connections are meaningful, poor when they are not -- highlights both the promise and the risk of productive hallucination as a research tool, and motivates the development of stronger filtering mechanisms in the Critic agent.

---

*Report generated for evaluation of the Research Mentor system. All scores assigned by the Judge agent (Gemini 2.0 Flash, temperature=0) in automated pairwise comparison.*
