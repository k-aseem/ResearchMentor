import os
import sys
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
            temperature=1.0
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

    def run_librarian_mode(self, query: str, context: str) -> str:
        """Standard RAG response"""
        prompt = f"""You are an expert Research Librarian. Answer the user's query strictly based on the context below.
If the answer is not in the context, admit it.

Context: {context}

User Query: {query}"""
        return self.llm_librarian.invoke(prompt)

    def run_dreamer_mode(self, query: str, context: str) -> str:
        """The Dreamer: Generates novel hypotheses."""
        prompt = f"""You are a visionary Principal Investigator (PI) in Machine Learning and AI.
The user asked: "{query}"

Our current literature (context below) does NOT contain a direct answer.
Context: {context}

Your Task:
1. Acknowledge the gap in the literature.
2. Propose 2 NOVEL hypotheses or theoretical frameworks that might answer the question.
3. Ground your hypotheses in scientific principles from the context where possible.
4. Do NOT cite fake papers."""
        print("   Dreaming up hypotheses (Temp=1.0)...")
        return self.llm_dreamer.invoke(prompt)

    def run_critic_mode(self, hypotheses: str) -> str:
        """The Critic: Checks for feasibility."""
        prompt = f"""You are "Reviewer #2" for a top-tier ML conference (NeurIPS/ICML).
Evaluate the following hypotheses for scientific validity and feasibility.

Hypotheses:
{hypotheses}

Your Task:
1. Identify any logical fallacies, unsupported claims, or technical impossibilities.
2. Assign a "Feasibility Score" (0-10) to each hypothesis.
3. Provide a harsh but constructive critique.
4. If the hypotheses are completely off-topic or nonsensical, give a score of 0."""
        print("   Critiquing hypotheses (Temp=0)...")
        return self.llm_critic.invoke(prompt)

    def process_query(self, query: str, include_baseline: bool = True):
        """
        Process a query through the Research Mentor system.
        Optionally includes baseline comparison for evaluation.
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

        # 2. GAP DETECTION
        if similarity >= SIMILARITY_THRESHOLD:
            print("[RESEARCH MENTOR] Mode: LIBRARIAN (Knowledge Found)")
            response = self.run_librarian_mode(query, context)

            print("\n" + "-"*70)
            print("LIBRARIAN RESPONSE:")
            print("-"*70)
            print(response)

        else:
            print("[RESEARCH MENTOR] Mode: RESEARCH MENTOR (Gap Detected)")

            # 3. DREAM
            hypotheses = self.run_dreamer_mode(query, context)

            # 4. CRITIQUE
            critique = self.run_critic_mode(hypotheses)

            print("\n" + "-"*70)
            print("PROPOSED HYPOTHESES (Dreamer):")
            print("-"*70)
            print(hypotheses)

            print("\n" + "-"*70)
            print("REVIEWER CRITIQUE (Critic):")
            print("-"*70)
            print(critique)

        # Show baseline comparison
        if include_baseline and baseline_response:
            print("\n" + "-"*70)
            print("BASELINE COMPARISON (Standard LLM, no RAG/special prompting):")
            print("-"*70)
            print(baseline_response)


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    mentor = ResearchMentorSystem()

    # SETUP: Load Dummy Data
    mentor.ingest_dummy_data()

    # TEST CASE 1: The "Known" Test
    # Question about something explicitly stated in the paper
    # Expected: Librarian Mode with factual answer from the knowledge base
    print("\n\n" + "="*70)
    print("TEST CASE 1: KNOWN TEST")
    print("="*70)
    mentor.process_query(
        "How much does LoRA reduce parameter updates compared to full fine-tuning?"
    )

    # TEST CASE 2: The "Gap" Test
    # Question combining two concepts from the paper that aren't explicitly linked
    # The paper discusses LoRA and RAG separately, but not together
    # Expected: Research Mentor Mode with hypotheses about combining them
    print("\n\n" + "="*70)
    print("TEST CASE 2: GAP TEST")
    print("="*70)
    mentor.process_query(
        "Could LoRA fine-tuning be combined with RAG to reduce both hallucinations and training cost?"
    )

    # TEST CASE 3: The "Hallucination" Test
    # Question about something completely absent from the knowledge base
    # Expected: Research Mentor Mode, Critic should give very low feasibility scores
    print("\n\n" + "="*70)
    print("TEST CASE 3: HALLUCINATION TEST")
    print("="*70)
    mentor.process_query(
        "What is the best way to grow tomatoes in a greenhouse?"
    )
