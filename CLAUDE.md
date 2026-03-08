# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research Mentor is an AI-powered multi-agent system that helps researchers generate novel, testable hypotheses when existing literature doesn't directly answer their questions. The core concept is "Productive Hallucination" — a pipeline that deliberately induces creative LLM generation in detected knowledge gaps while constraining it with critical review.

## Commands

```bash
# Run the main program (interactive demo with 3 sample queries)
python research_mentor.py

# Run all tests (90 total: 30 known, 30 gap, 30 hallucination)
python run_tests.py

# Run tests by category
python run_tests.py --category known
python run_tests.py --category gap
python run_tests.py --category hallucination

# Run a single test
python run_tests.py --test-id known_001

# Limit tests per category
python run_tests.py --limit 5

# Save detailed results to JSON
python run_tests.py --save-results results.json
```

## Setup

Requires Python 3.12 with a `.venv` virtual environment. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`. Uses Google Gemini 2.0 Flash as the LLM and local HuggingFace `all-MiniLM-L6-v2` embeddings (no API calls for embeddings).

## Architecture

### Multi-Agent Pipeline

Five specialized agents in `research_mentor.py`, each with deliberate temperature settings:

- **Librarian** (temp=0): RAG-based answering with self-reported confidence (HIGH/MEDIUM/LOW)
- **Gap Detector** (no LLM): Two-stage routing logic based on similarity + confidence
- **Dreamer** (temp=1.2): Generates 3 novel, testable hypotheses grounded in literature
- **Critic** (temp=0): Reviews hypotheses for logical consistency, domain constraints, and testability (scored 0-10)
- **Judge** (temp=0): Compares Research Mentor output vs. Baseline LLM response
- **Baseline LLM** (temp=0.7): Standard response for comparison benchmarking

### Two-Stage Gap Detection (Core Routing Logic)

1. **Stage 1 — Similarity Check**: Query embedded and compared against ChromaDB. If `similarity < 0.55` → Research Mentor Mode (topic not in knowledge base)
2. **Stage 2 — Confidence Check**: If similarity ≥ 0.55, Librarian attempts an answer. HIGH/MEDIUM confidence → return Librarian answer. LOW confidence → Research Mentor Mode (gap detected despite related content)

### Research Mentor Pipeline (when gap detected)

Query → Dreamer (3 hypotheses at temp=1.2) → Critic (feasibility review at temp=0) → formatted output with hypotheses + critical review

### Key Classes and Methods

All core logic lives in the `ResearchMentorSystem` class in `research_mentor.py`:
- `ingest_documents(pdf_paths)` / `ingest_dummy_data()` — Load documents into ChromaDB
- `retrieve_context(query)` — Semantic search returning top 3 results + similarity score
- `process_query(query)` — Full pipeline with human-readable output
- `process_query_for_eval(query)` — Returns structured dict (used by test runner)
- `_parse_confidence(response)` — Extracts HIGH/MEDIUM/LOW from Librarian output
- `_parse_judge_response(response)` — Parses judge scores and winner

### File Layout

- `research_mentor.py` — All agent logic, RAG pipeline, and the `ResearchMentorSystem` class
- `config.py` — Loads config from `.env` into a `CONFIG` dict
- `test_cases.py` — 90 test cases across 3 categories (known/gap/hallucination)
- `run_tests.py` — Test runner with CLI args, mode detection accuracy, and judge scoring
- `RESULTS_REPORT.md` — Evaluation analysis and findings

### Tech Stack

- **LLM**: Google Gemini via `langchain-google-genai`
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (local, via `sentence-transformers`)
- **Vector DB**: ChromaDB (persistent, stored at `./chroma_db`)
- **Orchestration**: LangChain (prompts, document loading, text splitting)
