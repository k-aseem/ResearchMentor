# NotebookLLM vs Research Mentor Comparison Experiment

**Goal**: Compare NotebookLLM and Research Mentor on the same 10 papers and 30 Known test questions to evaluate speed and quality.

---

## Part 1: Extract Research Mentor Baseline Data

First, we need to extract timing and scoring data from our existing Research Mentor results.

### Step 1: Run Research Mentor tests and capture timing

```bash
cd /Users/aseemkhandelwal/VSCode-Projects/research-mentor
python run_tests.py --category known --save-results notebooklm_comparison/rm_baseline_results.json
```

This will generate a JSON file with all the timing data we need.

### Step 2: Extract timing data to CSV

I'll create a script to parse the JSON and populate the RM columns in `comparison_tracking.csv`.

---

## Part 2: Test NotebookLLM

### Prerequisites

1. Go to https://notebooklm.google.com/
2. Sign in with your Google account
3. Create a new notebook

### Step 1: Upload Papers to NotebookLLM

Upload all 10 PDFs from your `papers/` directory:

- [ ] 2106.09685.pdf (LoRA)
- [ ] 2305.14314.pdf (QLoRA)
- [ ] 2208.07339.pdf (LLM.int8())
- [ ] 2210.17323.pdf (GPTQ)
- [ ] 2005.11401.pdf (RAG)
- [ ] 2201.11903.pdf (Chain-of-Thought)
- [ ] 2101.00190.pdf (Prefix-Tuning)
- [ ] 1706.03762.pdf (Attention Is All You Need)
- [ ] 2307.03109.pdf (LLM Evaluation Survey)
- [ ] 2312.03863.pdf (Efficient LLMs Survey)

**Note**: Wait for all papers to finish processing before proceeding.

### Step 2: Ask Questions and Track Results

Open `known_test_questions.txt` and `comparison_tracking.csv` side by side.

For each question (1-30):

1. **Start timer** (use your phone or https://www.online-stopwatch.com/)
2. **Copy question** from `known_test_questions.txt`
3. **Paste into NotebookLLM** and press Enter
4. **Stop timer** when NotebookLLM finishes generating the response
5. **Record in CSV**:
   - `NotebookLM_Response_Time_Seconds`: Time in seconds (e.g., 3.5)
   - `NotebookLM_Cites_Papers`: "Yes" if it cites specific papers, "No" otherwise
   - `NotebookLM_Answer_Summary`: Brief 1-2 sentence summary of the answer
6. **Rate quality** (1-10 scale):
   - 10 = Perfect, specific answer with exact numbers/facts
   - 7-9 = Good answer, mostly accurate
   - 4-6 = Vague or partially correct
   - 1-3 = Wrong or hallucinated
7. **Add notes** if needed (e.g., "Hallucinated a number", "Cited wrong paper", "Very detailed")

### Timing Tips

- Use a stopwatch or timer app on your phone
- Start timer IMMEDIATELY when you press Enter
- Stop timer when the FULL response is visible (not when it starts typing)
- If NotebookLLM takes more than 30 seconds, note this in the Notes column

### Quality Assessment Guidelines

**10/10**: Exact answer with specific numbers/facts from the papers
- Example: "LoRA reduces trainable parameters by 10,000x for GPT-3 175B"

**8-9/10**: Correct answer, specific but missing minor details
- Example: "LoRA reduces parameters significantly, on the order of 10,000x"

**6-7/10**: Correct general idea but vague or imprecise
- Example: "LoRA greatly reduces the number of parameters needed for fine-tuning"

**4-5/10**: Partially correct or missing key information
- Example: "LoRA is a parameter-efficient fine-tuning method" (doesn't answer "how much")

**1-3/10**: Incorrect, hallucinated, or doesn't answer the question
- Example: "LoRA reduces parameters by 50%" (wrong number)

---

## Part 3: Fill in Research Mentor Data

Once you have NotebookLLM results, run this script to populate RM columns:

```bash
python notebooklm_comparison/populate_rm_data.py
```

This will read `rm_baseline_results.json` and fill in:
- `RM_Response_Time_Seconds`
- `RM_Mode` (librarian or research_mentor)
- `RM_Judge_Score`
- `RM_Answer_Quality_1_10` (using Judge scores)

---

## Part 4: Analyze Results

Once `comparison_tracking.csv` is complete, run the analysis script:

```bash
python notebooklm_comparison/analyze_comparison.py
```

This will generate:
- **Average response times** (NotebookLLM vs RM)
- **Quality comparison** (average scores)
- **Winner breakdown** (which system won on each question)
- **Citation analysis** (how often NotebookLLM cites papers)
- **Mode analysis** (RM Librarian mode success rate)

Output will be saved to `notebooklm_comparison/COMPARISON_REPORT.md`.

---

## Expected Time Investment

- **Part 1** (RM baseline): ~10 minutes
- **Part 2** (NotebookLLM testing): ~45-60 minutes (30 questions × 1-2 min each)
- **Part 3** (Fill RM data): ~2 minutes
- **Part 4** (Analysis): ~2 minutes

**Total**: ~1 hour

---

## What We're Measuring

### Speed
- Average response time per question
- Variance in response times
- Which system is faster overall

### Quality
- Answer accuracy and specificity
- Citation behavior (does it reference papers?)
- Hallucination rate

### Mode Detection (RM only)
- How often RM correctly uses Librarian mode for Known questions
- Relationship between mode detection and answer quality

---

## Common Issues and Solutions

### NotebookLLM Issues

**Problem**: NotebookLLM says "I don't have information on this"
- **Solution**: Check that all 10 papers uploaded successfully
- **Record**: Note this in the Notes column, score quality as 1-2

**Problem**: NotebookLLM gives a very long response
- **Solution**: Still record the full time, note "verbose" in Notes column
- **Quality**: Judge based on whether it actually answers the question

**Problem**: NotebookLLM cites papers but gets the fact wrong
- **Solution**: Lower quality score (6-7 range), note "cited but inaccurate"

### Timing Issues

**Problem**: Hard to time precisely
- **Solution**: Round to nearest 0.5 seconds (e.g., 3.5s, 4.0s, 4.5s)
- **Alternative**: Use screen recording software to time later

**Problem**: NotebookLLM freezes or crashes
- **Solution**: Note in CSV, retry the question, record the retry time

---

## Next Steps After Completion

Once you have the full comparison data:

1. Review `COMPARISON_REPORT.md` for key findings
2. Prepare a presentation slide deck comparing the two systems
3. Discuss with your professor:
   - Which system is faster?
   - Which gives better quality answers?
   - What are the trade-offs?
   - Which would you recommend for research use cases?

---

## Questions?

If you run into issues during the experiment, document them in the Notes column and we can troubleshoot later.

Good luck! 🚀
