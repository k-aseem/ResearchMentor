# NotebookLLM Comparison Experiment

This directory contains everything you need to compare NotebookLLM with your Research Mentor system.

## Quick Start

**Step 1**: Generate Research Mentor baseline data
```bash
python run_tests.py --category known --save-results notebooklm_comparison/rm_baseline_results.json
```

**Step 2**: Populate the CSV with RM data
```bash
python notebooklm_comparison/populate_rm_data.py
```

**Step 3**: Test NotebookLLM manually
- Open `EXPERIMENT_INSTRUCTIONS.md` for detailed step-by-step guide
- Use `known_test_questions.txt` for the 30 questions
- Record results in `comparison_tracking.csv`

**Step 4**: Generate comparison report
```bash
python notebooklm_comparison/analyze_comparison.py
```

**Step 5**: Review results
- Open `COMPARISON_REPORT.md` to see findings

---

## Files in This Directory

### Input Files (you'll create these)
- `known_test_questions.txt` - The 30 questions to ask both systems
- `comparison_tracking.csv` - Tracking spreadsheet (fill in NotebookLLM columns manually)

### Scripts (automated)
- `populate_rm_data.py` - Extracts RM data from JSON and populates CSV
- `analyze_comparison.py` - Analyzes CSV and generates report

### Documentation
- `EXPERIMENT_INSTRUCTIONS.md` - Detailed step-by-step instructions
- `README.md` - This file

### Output Files (generated)
- `rm_baseline_results.json` - Raw RM test results
- `COMPARISON_REPORT.md` - Final analysis report

---

## Time Required

- **Research Mentor testing**: ~10 minutes (automated)
- **NotebookLLM testing**: ~45-60 minutes (manual)
- **Analysis**: ~5 minutes (automated)

**Total**: ~1 hour

---

## What You'll Learn

1. **Speed**: Which system responds faster?
2. **Quality**: Which gives better answers?
3. **Citations**: How often does NotebookLLM cite papers?
4. **Mode Detection**: How well does RM detect Known questions?

---

## Next Steps After This Experiment

Once you complete the NotebookLLM comparison, you can tackle the other two professor assignments:

1. ✅ **NotebookLLM Comparison** (this experiment)
2. ⬜ **Better RAG Approaches** - Explore alternatives to current RAG
3. ⬜ **Instruction Tuning** - Research instruction tuning for research-specific use

Good luck! 🚀
