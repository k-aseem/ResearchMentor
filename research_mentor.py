import os
import re
from typing import Tuple, List

# Load configuration
from config import CONFIG

# LangChain Imports
from langchain_google_genai import GoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- CONFIGURATION ---
VECTOR_DB_PATH = CONFIG["vector_db_path"]
SIMILARITY_THRESHOLD = CONFIG["similarity_threshold"]


class ResearchMentorSystem:
    def __init__(self):
        # Local embeddings (no API calls, no rate limits)
        self.embeddings = HuggingFaceEmbeddings(model_name=CONFIG["embedding_model"])
        self.vector_db = None

        # LLM instances with different temperatures
        self.llm_librarian = GoogleGenerativeAI(
            model=CONFIG["gemini_model"],
            google_api_key=CONFIG["gemini_api_key"],
            temperature=0
        )
        self.llm_dreamer = GoogleGenerativeAI(
            model=CONFIG["gemini_model"],
            google_api_key=CONFIG["gemini_api_key"],
            temperature=1.2  # High randomness for creative hypothesis generation
        )
        self.llm_critic = GoogleGenerativeAI(
            model=CONFIG["gemini_model"],
            google_api_key=CONFIG["gemini_api_key"],
            temperature=0
        )
        # Baseline LLM for comparison (standard ChatGPT-like behavior)
        self.llm_baseline = GoogleGenerativeAI(
            model=CONFIG["gemini_model"],
            google_api_key=CONFIG["gemini_api_key"],
            temperature=0.7
        )
        # Judge LLM for comparing outputs (temperature=0 for consistent evaluation)
        self.llm_judge = GoogleGenerativeAI(
            model=CONFIG["gemini_model"],
            google_api_key=CONFIG["gemini_api_key"],
            temperature=0
        )

    def ingest_documents(self, pdf_paths: List[str]):
        """Loads PDFs, splits them, and creates the Vector DB."""
        print(f"Ingesting {len(pdf_paths)} documents...")
        docs = []
        for path in pdf_paths:
            if os.path.exists(path):
                loader = PyPDFLoader(path)
                docs.extend(loader.load())
            else:
                print(f"Warning: File not found: {path}")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        self.vector_db = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=VECTOR_DB_PATH
        )
        print(f"Knowledge Base Ready with {len(splits)} chunks.")

    def create_dummy_paper(self):
        """
        Creates a fake research paper about LLMs and Machine Learning for testing.
        Contains multiple distinct concepts that can be tested independently or combined.
        """
        content = """
        Title: Advances in Large Language Model Training and Deployment
        Authors: Research Team, AI Laboratory

        Abstract:
        This paper presents our findings on training and deploying large language models (LLMs).
        We examine the effectiveness of various fine-tuning strategies, the impact of model
        quantization on inference speed, and the role of retrieval-augmented generation (RAG)
        in reducing hallucinations. Our experiments were conducted on models ranging from
        7 billion to 70 billion parameters.

        Section 1: Introduction to Large Language Models
        Large language models are neural networks trained on vast amounts of text data.
        The transformer architecture, introduced in 2017, forms the backbone of modern LLMs.
        These models use self-attention mechanisms to capture long-range dependencies in text.
        Pre-training on large corpora followed by task-specific fine-tuning has become the
        standard paradigm for achieving state-of-the-art results on NLP benchmarks.

        Section 2: Fine-Tuning Strategies
        We investigated three fine-tuning approaches: full fine-tuning, LoRA (Low-Rank Adaptation),
        and prefix tuning. Our experiments show that LoRA achieves 97% of full fine-tuning
        performance while only updating 0.1% of the model parameters. This makes LoRA particularly
        suitable for resource-constrained environments. Full fine-tuning remains superior for
        tasks requiring significant domain adaptation, but the computational cost is 50x higher
        than LoRA. Prefix tuning showed promising results for few-shot learning scenarios but
        struggled with complex reasoning tasks.

        Section 3: Model Quantization and Inference
        Quantization reduces model precision from 32-bit floating point to lower bit representations.
        Our tests demonstrate that 8-bit quantization maintains 99% of original model accuracy
        while reducing memory footprint by 75%. However, 4-bit quantization shows a 12% accuracy
        degradation on complex reasoning tasks, though it enables running 70B parameter models
        on consumer GPUs with 24GB VRAM. We found that quantization-aware training can recover
        most of the lost accuracy in 4-bit models.

        Section 4: Retrieval-Augmented Generation (RAG)
        RAG combines LLMs with external knowledge retrieval to ground responses in factual data.
        Our experiments show that RAG reduces hallucination rates by 67% compared to base models.
        The quality of the retrieval system directly impacts RAG performance - using dense
        embeddings with cosine similarity outperformed BM25 keyword search by 23% on factual
        accuracy benchmarks. However, RAG increases latency by 340ms per query on average due
        to the retrieval step.

        Section 5: Prompt Engineering and Chain-of-Thought
        Chain-of-thought (CoT) prompting significantly improves reasoning capabilities.
        Our experiments show that adding "Let's think step by step" to prompts increases
        accuracy on math word problems from 58% to 83%. However, CoT prompting increases
        token usage by 3x on average, which impacts cost in production deployments.
        Zero-shot CoT performs nearly as well as few-shot CoT for most reasoning tasks.

        Section 6: Evaluation Metrics and Benchmarks
        We evaluated models on MMLU, HellaSwag, TruthfulQA, and custom domain-specific benchmarks.
        Interestingly, we found that models with higher MMLU scores did not always perform
        better on real-world tasks, suggesting the need for more practical evaluation frameworks.
        Human evaluation remains the gold standard but is expensive and time-consuming.

        Section 7: Deployment Challenges
        Production deployment of LLMs faces several challenges: cold start latency (first
        inference takes 5-10x longer), memory management for concurrent users, and output
        consistency across identical prompts. We found that batching requests improves
        throughput by 4x but increases individual request latency by 200ms.

        Conclusion:
        Our research demonstrates that careful selection of fine-tuning strategies, quantization
        levels, and retrieval augmentation can significantly impact LLM performance and
        deployment costs. LoRA provides an excellent balance of performance and efficiency
        for most use cases. RAG is essential for applications requiring factual accuracy.
        Future work should explore combining these techniques optimally.
        """
        return [Document(page_content=content, metadata={"source": "llm_research_paper"})]

    def ingest_dummy_data(self):
        """Helper to load dummy data without needing real PDFs"""
        print("Loading dummy research data...")
        docs = self.create_dummy_paper()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)
        self.vector_db = Chroma.from_documents(splits, self.embeddings)
        print(f"Dummy Knowledge Base Ready. ({len(splits)} chunks)")

    def retrieve_context(self, query: str) -> Tuple[str, float]:
        """
        The Librarian: Retrieves context and calculates similarity score.
        Returns: (context_text, similarity_score)
        """
        if not self.vector_db:
            return "No database loaded.", 0.0

        results = self.vector_db.similarity_search_with_score(query, k=3)

        if not results:
            return "", 0.0

        best_doc, best_distance = results[0]
        context_text = "\n\n".join([doc.page_content for doc, score in results])

        # Convert L2 distance to similarity score (0 to 1, higher = better)
        similarity = 1 / (1 + best_distance)

        return context_text, similarity

    def get_baseline_response(self, query: str) -> str:
        """
        Get a standard LLM response without any special prompting or RAG.
        This serves as a baseline to compare against our specialized agents.
        """
        prompt = f"Answer this question: {query}"
        return self.llm_baseline.invoke(prompt)

    def run_librarian_mode(self, query: str, context: str) -> Tuple[str, str]:
        """
        The Librarian: RAG-based response with confidence assessment.
        Returns: (answer, confidence) where confidence is HIGH, MEDIUM, or LOW
        """
        prompt = f"""You are an expert Research Librarian helping a PhD student. Your job is to answer questions based ONLY on the provided context, but in a thorough and research-useful way.

CONTEXT:
{context}

QUESTION: {query}

INSTRUCTIONS:
1. Answer the question using ONLY information from the context above.
2. Provide a detailed, well-structured answer that would be useful for a researcher:
   - State the key finding or fact clearly
   - Include specific numbers, percentages, or metrics from the context
   - Explain the significance or implications of the finding
   - Mention any related tradeoffs, limitations, or caveats from the context
   - Reference which part of the literature the information comes from
3. After your answer, assess your confidence level:
   - HIGH: The context directly and explicitly answers the question
   - MEDIUM: The context partially answers the question or requires some inference
   - LOW: The context does NOT contain information to answer this question

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
ANSWER: [Your detailed answer here - aim for 3-5 sentences that would be useful in a research context]

CONFIDENCE: [HIGH/MEDIUM/LOW]
REASON: [Brief explanation of why you assigned this confidence level]"""

        response = self.llm_librarian.invoke(prompt)

        # Parse confidence from response
        confidence = self._parse_confidence(response)

        return response, confidence

    def _parse_confidence(self, response: str) -> str:
        """Extract confidence level from Librarian response."""
        response_upper = response.upper()

        # Look for explicit confidence markers
        if "CONFIDENCE: HIGH" in response_upper or "CONFIDENCE:HIGH" in response_upper:
            return "HIGH"
        elif "CONFIDENCE: MEDIUM" in response_upper or "CONFIDENCE:MEDIUM" in response_upper:
            return "MEDIUM"
        elif "CONFIDENCE: LOW" in response_upper or "CONFIDENCE:LOW" in response_upper:
            return "LOW"

        # Fallback: look for indicators of uncertainty in the text
        uncertainty_phrases = [
            "not in the context",
            "no information",
            "does not contain",
            "doesn't contain",
            "cannot find",
            "not mentioned",
            "not addressed",
            "no direct answer",
            "not explicitly",
            "unable to find"
        ]

        response_lower = response.lower()
        for phrase in uncertainty_phrases:
            if phrase in response_lower:
                return "LOW"

        # Default to MEDIUM if we can't determine
        return "MEDIUM"

    def run_dreamer_mode(self, query: str, context: str) -> str:
        """
        The Dreamer: Generates novel hypotheses through "Productive Hallucination".
        Uses high temperature (1.2) to encourage creative but grounded speculation.
        """
        prompt = f"""You are a visionary Principal Investigator (PI) mentoring a PhD student.
Your role is to help bridge gaps in the literature by proposing novel, testable hypotheses.

THE RESEARCH QUESTION: "{query}"

AVAILABLE LITERATURE (Your "Known Universe"):
{context}

YOUR TASK - PRODUCTIVE HALLUCINATION:
The literature above does NOT directly answer the research question. Your job is to:

1. ACKNOWLEDGE THE GAP: Briefly state what the literature covers and what's missing.

2. PROPOSE 3 NOVEL HYPOTHESES that could bridge this gap:
   - Each hypothesis should be grounded in concepts from the literature above
   - You MAY speculate and make creative connections
   - You MAY NOT cite fake papers or fabricate experimental results
   - Each hypothesis should be specific enough to be testable

3. For each hypothesis, explain:
   - The core idea
   - How it connects to the existing literature
   - What experiment or analysis could test it

FORMAT:
## Gap Analysis
[Your analysis of what's missing]

## Hypothesis 1: [Title]
[Description and grounding]

## Hypothesis 2: [Title]
[Description and grounding]

## Hypothesis 3: [Title]
[Description and grounding]"""
        print("   Dreaming up hypotheses (Temp=1.2)...")
        return self.llm_dreamer.invoke(prompt)

    def run_critic_mode(self, hypotheses: str, context: str) -> str:
        """
        The Critic: Verifies feasibility of proposed hypotheses.
        Uses temperature=0 for strict logical analysis.
        Does NOT check if hypothesis is TRUE (it's novel), but if it is VALID.
        """
        prompt = f"""You are "Reviewer #2" - a rigorous but fair scientific reviewer.
Your job is NOT to check if these hypotheses are true (they are novel ideas), but whether they are VALID.

PROPOSED HYPOTHESES:
{hypotheses}

DOMAIN KNOWLEDGE (from the literature):
{context}

YOUR REVIEW CRITERIA:

1. LOGICAL CONSISTENCY (Does the hypothesis contradict itself?)
   - Are the claims internally consistent?
   - Does the reasoning follow logically?

2. DOMAIN CONSTRAINTS (Does it violate known facts from the literature?)
   - Does it contradict established findings in the context?
   - Does it make physically/mathematically impossible claims?

3. TESTABILITY (Could this be experimentally verified?)
   - Is the hypothesis specific enough to test?
   - Are the proposed experiments realistic?

FOR EACH HYPOTHESIS, PROVIDE:

## Hypothesis [N] Review
- **Feasibility Score: X/10**
- **Logical Consistency:** [Pass/Fail with explanation]
- **Domain Constraints:** [Pass/Fail with explanation]
- **Testability:** [High/Medium/Low with explanation]
- **Key Strengths:** [What's promising about this idea]
- **Key Weaknesses:** [What are the concerns]
- **Verdict:** [Promising / Needs Work / Not Recommended]

## Overall Recommendation
[Which hypothesis is most promising and why]"""
        print("   Critiquing hypotheses (Temp=0)...")
        return self.llm_critic.invoke(prompt)

    def process_query(self, query: str, include_baseline: bool = True):
        """
        Process a query through the Research Mentor system.

        Two-stage gap detection:
        1. Similarity threshold for initial filtering (is query even related?)
        2. Librarian confidence for semantic gap detection (does context answer the question?)
        """
        print(f"\n{'='*70}")
        print(f"QUERY: '{query}'")
        print('='*70)

        # Get baseline response for comparison (if enabled)
        baseline_response = None
        if include_baseline:
            print("\n[BASELINE] Getting standard LLM response...")
            baseline_response = self.get_baseline_response(query)

        # 1. RETRIEVE
        context, similarity = self.retrieve_context(query)
        print(f"\n[RESEARCH MENTOR] Similarity Score: {similarity:.4f} (Threshold: {SIMILARITY_THRESHOLD})")

        # 2. TWO-STAGE GAP DETECTION
        if similarity < SIMILARITY_THRESHOLD:
            # Stage 1: Low similarity = clearly unrelated topic
            print("[RESEARCH MENTOR] Stage 1: Low similarity - Topic not in knowledge base")
            print("[RESEARCH MENTOR] Mode: RESEARCH MENTOR (Gap Detected)")
            self._run_research_mentor_pipeline(query, context)
        else:
            # Stage 2: High similarity, but does the context actually answer the question?
            print("[RESEARCH MENTOR] Stage 1: Similarity OK - Checking if context answers the question...")
            librarian_response, confidence = self.run_librarian_mode(query, context)
            print(f"[RESEARCH MENTOR] Stage 2: Librarian Confidence: {confidence}")

            if confidence == "HIGH":
                # Context directly answers the question
                print("[RESEARCH MENTOR] Mode: LIBRARIAN (Direct Answer Found)")
                print("\n" + "-"*70)
                print("LIBRARIAN RESPONSE:")
                print("-"*70)
                print(librarian_response)

            elif confidence == "MEDIUM":
                # Context partially answers - show Librarian response but note uncertainty
                print("[RESEARCH MENTOR] Mode: LIBRARIAN (Partial Answer - Medium Confidence)")
                print("\n" + "-"*70)
                print("LIBRARIAN RESPONSE (Medium Confidence):")
                print("-"*70)
                print(librarian_response)

            else:  # LOW confidence
                # Context is related but doesn't answer the question = GAP
                print("[RESEARCH MENTOR] Mode: RESEARCH MENTOR (Gap Detected - Context doesn't answer question)")
                print("\n" + "-"*70)
                print("LIBRARIAN ASSESSMENT:")
                print("-"*70)
                print(librarian_response)
                print("\n[RESEARCH MENTOR] Librarian found no direct answer. Switching to hypothesis generation...")
                self._run_research_mentor_pipeline(query, context)

        # Show baseline comparison
        if include_baseline and baseline_response:
            print("\n" + "-"*70)
            print("BASELINE COMPARISON (Standard LLM, no RAG/special prompting):")
            print("-"*70)
            print(baseline_response)

    def _run_research_mentor_pipeline(self, query: str, context: str) -> Tuple[str, str]:
        """
        Run the Dreamer -> Critic pipeline for gap/hallucination cases.
        This is the core "Research Mentor Protocol" for productive hallucination.
        Returns: (hypotheses, critique) for use in evaluation
        """
        # Phase 2a: THE DREAMER - Generate novel hypotheses
        hypotheses = self.run_dreamer_mode(query, context)

        # Phase 2b: THE CRITIC - Verify feasibility
        critique = self.run_critic_mode(hypotheses, context)

        # Phase 3: FINAL OUTPUT - Structured presentation
        print("\n" + "="*70)
        print("RESEARCH MENTOR OUTPUT")
        print("="*70)

        print("\n" + "-"*70)
        print("PROPOSED HYPOTHESES (The Dreamer - Temp=1.2)")
        print("-"*70)
        print(hypotheses)

        print("\n" + "-"*70)
        print("FEASIBILITY REVIEW (The Critic - Temp=0)")
        print("-"*70)
        print(critique)

        return hypotheses, critique

    def run_judge(self, query: str, baseline_response: str, rm_response: str, mode: str) -> dict:
        """
        The Judge: Compares Baseline LLM output vs Research Mentor output.
        Determines which response is more helpful for a PhD student/researcher.

        Returns a dict with:
        - winner: "baseline" | "research_mentor" | "tie"
        - score_baseline: 1-10
        - score_rm: 1-10
        - reasoning: explanation
        """
        prompt = f"""You are an impartial judge evaluating two AI responses for a PhD student doing research.

You MUST respond in EXACTLY this format with these four lines. Do not add any text before or after:

SCORE_A: [integer from 1 to 10]
SCORE_B: [integer from 1 to 10]
WINNER: [exactly A, B, or TIE]
REASONING: [2-3 sentences explaining your decision]

RESEARCH QUESTION: "{query}"

RESPONSE A (Baseline LLM - Standard ChatGPT-like response):
{baseline_response[:3000]}

RESPONSE B (Research Mentor System - {mode}):
{rm_response[:3000]}

EVALUATION CRITERIA:
1. Usefulness for Research - Does it help advance the student's research?
2. Accuracy - Is the information factually correct (or appropriately speculative)?
3. Actionability - Does it provide concrete next steps or testable ideas?
4. Grounding - Is it grounded in relevant literature/context?
5. Novelty (for gap questions) - Does it propose interesting new directions?

CONTEXT FOR JUDGING:
- For KNOWN questions: Better response should be concise, accurate, and cite the source
- For GAP questions: Better response should propose novel, testable hypotheses
- For HALLUCINATION questions: Better response should acknowledge limitations or find creative connections

Remember: You MUST start your response with "SCORE_A:" and follow the exact four-line format above."""

        response = self.llm_judge.invoke(prompt)

        # Parse the judge's response
        result = self._parse_judge_response(response)
        return result

    def _parse_judge_response(self, response: str) -> dict:
        """Parse the Judge's response into structured output."""
        result = {
            "winner": "tie",
            "score_baseline": 5,
            "score_rm": 5,
            "reasoning": response,
            "raw_response": response
        }

        response_upper = response.upper()

        # Parse scores - try multiple patterns
        score_a_match = re.search(r'SCORE_A\s*[:=]\s*(\d+)', response_upper)
        score_b_match = re.search(r'SCORE_B\s*[:=]\s*(\d+)', response_upper)

        if score_a_match:
            result["score_baseline"] = min(int(score_a_match.group(1)), 10)
        if score_b_match:
            result["score_rm"] = min(int(score_b_match.group(1)), 10)

        # Parse winner - try explicit marker first
        winner_match = re.search(r'WINNER\s*[:=]\s*(A|B|TIE)', response_upper)
        if winner_match:
            w = winner_match.group(1)
            if w == "A":
                result["winner"] = "baseline"
            elif w == "B":
                result["winner"] = "research_mentor"
            else:
                result["winner"] = "tie"
        elif score_a_match and score_b_match:
            # Fallback: infer winner from scores if markers not found
            sa = result["score_baseline"]
            sb = result["score_rm"]
            if sa > sb:
                result["winner"] = "baseline"
            elif sb > sa:
                result["winner"] = "research_mentor"
            else:
                result["winner"] = "tie"
        else:
            # Last resort: infer from reasoning text
            response_lower = response.lower()
            b_better_phrases = ["response b is better", "response b is much better",
                                "b is more useful", "b is better", "b wins",
                                "response b provides better", "b is more helpful"]
            a_better_phrases = ["response a is better", "response a is much better",
                                "a is more useful", "a is better", "a wins",
                                "response a provides better", "a is more helpful"]
            for phrase in b_better_phrases:
                if phrase in response_lower:
                    result["winner"] = "research_mentor"
                    break
            else:
                for phrase in a_better_phrases:
                    if phrase in response_lower:
                        result["winner"] = "baseline"
                        break

        # Extract reasoning
        reasoning_match = re.search(r'REASONING:\s*(.+)', response, re.IGNORECASE | re.DOTALL)
        if reasoning_match:
            result["reasoning"] = reasoning_match.group(1).strip()[:500]

        return result

    def process_query_for_eval(self, query: str) -> dict:
        """
        Process a query and return structured results for evaluation.
        Used by the test runner.

        Returns a dict with all relevant data for analysis.
        """
        results = {
            "query": query,
            "similarity": 0.0,
            "mode": None,
            "confidence": None,
            "baseline_response": None,
            "rm_response": None,
            "hypotheses": None,
            "critique": None,
            "judge_result": None
        }

        # Get baseline response
        results["baseline_response"] = self.get_baseline_response(query)

        # Retrieve context
        context, similarity = self.retrieve_context(query)
        results["similarity"] = similarity

        # Two-stage gap detection
        if similarity < SIMILARITY_THRESHOLD:
            results["mode"] = "research_mentor"
            results["confidence"] = "N/A (low similarity)"
            hypotheses = self.run_dreamer_mode(query, context)
            critique = self.run_critic_mode(hypotheses, context)
            results["hypotheses"] = hypotheses
            results["critique"] = critique
            results["rm_response"] = f"HYPOTHESES:\n{hypotheses}\n\nCRITIQUE:\n{critique}"
        else:
            librarian_response, confidence = self.run_librarian_mode(query, context)
            results["confidence"] = confidence

            if confidence in ["HIGH", "MEDIUM"]:
                results["mode"] = "librarian"
                results["rm_response"] = librarian_response
            else:  # LOW confidence
                results["mode"] = "research_mentor"
                hypotheses = self.run_dreamer_mode(query, context)
                critique = self.run_critic_mode(hypotheses, context)
                results["hypotheses"] = hypotheses
                results["critique"] = critique
                results["rm_response"] = f"LIBRARIAN ASSESSMENT:\n{librarian_response}\n\nHYPOTHESES:\n{hypotheses}\n\nCRITIQUE:\n{critique}"

        # Run Judge comparison
        results["judge_result"] = self.run_judge(
            query,
            results["baseline_response"],
            results["rm_response"],
            results["mode"]
        )

        return results


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    mentor = ResearchMentorSystem()

    # SETUP: Load Dummy Data
    mentor.ingest_dummy_data()

    # TEST CASE 1: The "Known" Test
    # Question about something explicitly stated in the paper
    # Expected: Librarian with HIGH confidence
    print("\n\n" + "="*70)
    print("TEST CASE 1: KNOWN TEST")
    print("="*70)
    mentor.process_query(
        "How much does LoRA reduce parameter updates compared to full fine-tuning?"
    )

    # TEST CASE 2: The "Gap" Test
    # Question combining two concepts from the paper that aren't explicitly linked
    # The paper discusses Chain-of-Thought (Section 5) and Quantization (Section 3) separately
    # but never mentions using CoT to recover accuracy lost from quantization
    # Expected: Librarian with LOW confidence -> Research Mentor Mode
    print("\n\n" + "="*70)
    print("TEST CASE 2: GAP TEST")
    print("="*70)
    mentor.process_query(
        "Can chain-of-thought prompting help recover the 12% accuracy loss from 4-bit quantization?"
    )

    # TEST CASE 3: The "Hallucination" Test
    # Question about something completely absent from the knowledge base
    # Expected: Low similarity -> Research Mentor Mode directly
    print("\n\n" + "="*70)
    print("TEST CASE 3: HALLUCINATION TEST")
    print("="*70)
    mentor.process_query(
        "What is the best way to grow tomatoes in a greenhouse?"
    )
