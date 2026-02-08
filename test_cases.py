"""
Test Cases for Research Mentor System

Categories:
1. KNOWN - Questions with direct answers in the knowledge base
2. GAP - Questions combining concepts that aren't explicitly linked
3. HALLUCINATION - Questions completely unrelated to the knowledge base

Goal: 30+ diverse test cases per category for robust evaluation.

Each test case has:
- query: The question to ask
- expected_mode: "librarian" or "research_mentor"
- description: What this test is checking
- tags: For filtering/categorizing tests
"""

# =============================================================================
# KNOWN TEST CASES
# Questions that SHOULD be answered by the Librarian (answer exists in paper)
# =============================================================================

KNOWN_TESTS = [
    # --- LoRA / Fine-tuning (Section 2) ---
    {
        "id": "known_001",
        "query": "How much does LoRA reduce parameter updates compared to full fine-tuning?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["0.1%", "parameters"],
        "description": "Direct fact about LoRA parameter efficiency",
        "tags": ["lora", "fine-tuning", "exact-number"]
    },
    {
        "id": "known_002",
        "query": "What percentage of full fine-tuning performance does LoRA achieve?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["97%"],
        "description": "LoRA performance relative to full fine-tuning",
        "tags": ["lora", "fine-tuning", "exact-number"]
    },
    {
        "id": "known_003",
        "query": "How much more expensive is full fine-tuning compared to LoRA?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["50x", "50 times"],
        "description": "Cost comparison between fine-tuning methods",
        "tags": ["lora", "fine-tuning", "cost"]
    },
    {
        "id": "known_004",
        "query": "What are the three fine-tuning approaches mentioned in the research?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["LoRA", "full fine-tuning", "prefix tuning"],
        "description": "Enumeration of fine-tuning methods",
        "tags": ["fine-tuning", "enumeration"]
    },
    {
        "id": "known_005",
        "query": "What tasks did prefix tuning struggle with?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["complex reasoning"],
        "description": "Prefix tuning limitations",
        "tags": ["prefix-tuning", "limitations"]
    },

    # --- Quantization (Section 3) ---
    {
        "id": "known_006",
        "query": "What accuracy does 8-bit quantization maintain compared to the original model?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["99%"],
        "description": "8-bit quantization accuracy retention",
        "tags": ["quantization", "8-bit", "exact-number"]
    },
    {
        "id": "known_007",
        "query": "How much memory reduction does 8-bit quantization provide?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["75%"],
        "description": "8-bit quantization memory savings",
        "tags": ["quantization", "8-bit", "memory"]
    },
    {
        "id": "known_008",
        "query": "What is the accuracy degradation from 4-bit quantization?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["12%"],
        "description": "4-bit quantization accuracy loss",
        "tags": ["quantization", "4-bit", "exact-number"]
    },
    {
        "id": "known_009",
        "query": "What size GPU can run 70B parameter models with 4-bit quantization?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["24GB", "consumer"],
        "description": "Hardware requirements for quantized models",
        "tags": ["quantization", "4-bit", "hardware"]
    },
    {
        "id": "known_010",
        "query": "What technique can recover accuracy lost from 4-bit quantization?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["quantization-aware training"],
        "description": "Technique to mitigate quantization loss",
        "tags": ["quantization", "training"]
    },

    # --- RAG (Section 4) ---
    {
        "id": "known_011",
        "query": "By how much does RAG reduce hallucination rates?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["67%"],
        "description": "RAG hallucination reduction",
        "tags": ["rag", "hallucination", "exact-number"]
    },
    {
        "id": "known_012",
        "query": "How much latency does RAG add per query?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["340ms", "340 ms"],
        "description": "RAG latency overhead",
        "tags": ["rag", "latency", "exact-number"]
    },
    {
        "id": "known_013",
        "query": "How much better do dense embeddings perform compared to BM25 for RAG?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["23%"],
        "description": "Embedding vs keyword search comparison",
        "tags": ["rag", "embeddings", "exact-number"]
    },

    # --- Chain-of-Thought (Section 5) ---
    {
        "id": "known_014",
        "query": "How much does chain-of-thought prompting improve math word problem accuracy?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["58%", "83%"],
        "description": "CoT improvement on math problems",
        "tags": ["cot", "math", "exact-number"]
    },
    {
        "id": "known_015",
        "query": "How much does CoT prompting increase token usage?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["3x", "three times"],
        "description": "CoT token overhead",
        "tags": ["cot", "tokens", "cost"]
    },
    {
        "id": "known_016",
        "query": "What phrase can be added to prompts for chain-of-thought reasoning?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["step by step", "Let's think"],
        "description": "CoT prompt template",
        "tags": ["cot", "prompting"]
    },
    {
        "id": "known_017",
        "query": "How does zero-shot CoT compare to few-shot CoT?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["nearly as well", "similar"],
        "description": "Zero-shot vs few-shot CoT comparison",
        "tags": ["cot", "comparison"]
    },

    # --- Deployment (Section 7) ---
    {
        "id": "known_018",
        "query": "How much slower is cold start latency compared to normal inference?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["5-10x", "5 to 10"],
        "description": "Cold start latency overhead",
        "tags": ["deployment", "latency"]
    },
    {
        "id": "known_019",
        "query": "How much does batching improve throughput?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["4x", "four times"],
        "description": "Batching throughput improvement",
        "tags": ["deployment", "batching", "exact-number"]
    },
    {
        "id": "known_020",
        "query": "How much latency does batching add to individual requests?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["200ms", "200 ms"],
        "description": "Batching latency tradeoff",
        "tags": ["deployment", "batching", "latency"]
    },

    # --- General / Architecture (Section 1) ---
    {
        "id": "known_021",
        "query": "When was the transformer architecture introduced?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["2017"],
        "description": "Transformer introduction year",
        "tags": ["architecture", "history"]
    },
    {
        "id": "known_022",
        "query": "What mechanism do transformers use to capture long-range dependencies?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["self-attention"],
        "description": "Core transformer mechanism",
        "tags": ["architecture", "attention"]
    },

    # --- Evaluation (Section 6) ---
    {
        "id": "known_023",
        "query": "What benchmarks were used to evaluate the models?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["MMLU", "HellaSwag", "TruthfulQA"],
        "description": "Evaluation benchmarks used",
        "tags": ["evaluation", "benchmarks"]
    },
    {
        "id": "known_024",
        "query": "What is considered the gold standard for LLM evaluation?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["human evaluation", "Human evaluation"],
        "description": "Best evaluation method",
        "tags": ["evaluation", "human"]
    },

    # --- Paraphrased / Indirect Questions ---
    {
        "id": "known_025",
        "query": "Is LoRA suitable for environments with limited compute resources?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["resource-constrained", "suitable", "yes"],
        "description": "LoRA suitability inference",
        "tags": ["lora", "inference"]
    },
    {
        "id": "known_026",
        "query": "What's the standard training paradigm for LLMs?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["pre-training", "fine-tuning"],
        "description": "LLM training paradigm",
        "tags": ["training", "paradigm"]
    },
    {
        "id": "known_027",
        "query": "What model sizes were used in the experiments?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["7 billion", "70 billion"],
        "description": "Model sizes in experiments",
        "tags": ["models", "size"]
    },
    {
        "id": "known_028",
        "query": "Does high MMLU score guarantee good real-world performance?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["not always", "did not always"],
        "description": "Benchmark limitations",
        "tags": ["evaluation", "limitations"]
    },
    {
        "id": "known_029",
        "query": "What deployment challenges do LLMs face in production?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["cold start", "memory", "consistency"],
        "description": "Production deployment challenges",
        "tags": ["deployment", "challenges"]
    },
    {
        "id": "known_030",
        "query": "What does RAG combine LLMs with?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["external knowledge", "retrieval"],
        "description": "RAG definition",
        "tags": ["rag", "definition"]
    },
]


# =============================================================================
# GAP TEST CASES
# Questions combining concepts that exist separately but aren't linked
# =============================================================================

GAP_TESTS = [
    # --- LoRA + Other Concepts ---
    {
        "id": "gap_001",
        "query": "Can chain-of-thought prompting help recover the 12% accuracy loss from 4-bit quantization?",
        "expected_mode": "research_mentor",
        "description": "Combining CoT (Section 5) with Quantization (Section 3)",
        "tags": ["cot", "quantization", "cross-section"]
    },
    {
        "id": "gap_002",
        "query": "Would LoRA fine-tuning improve RAG retrieval quality?",
        "expected_mode": "research_mentor",
        "description": "Combining LoRA (Section 2) with RAG (Section 4)",
        "tags": ["lora", "rag", "cross-section"]
    },
    {
        "id": "gap_003",
        "query": "Can prefix tuning be combined with quantization to reduce memory further?",
        "expected_mode": "research_mentor",
        "description": "Combining Prefix Tuning (Section 2) with Quantization (Section 3)",
        "tags": ["prefix-tuning", "quantization", "cross-section"]
    },
    {
        "id": "gap_004",
        "query": "How would LoRA affect cold start latency in production deployments?",
        "expected_mode": "research_mentor",
        "description": "Combining LoRA (Section 2) with Deployment (Section 7)",
        "tags": ["lora", "deployment", "cross-section"]
    },
    {
        "id": "gap_005",
        "query": "Could chain-of-thought prompting compensate for knowledge gaps that RAG misses?",
        "expected_mode": "research_mentor",
        "description": "Combining CoT (Section 5) with RAG (Section 4)",
        "tags": ["cot", "rag", "cross-section"]
    },

    # --- Quantization + Other Concepts ---
    {
        "id": "gap_006",
        "query": "Does 4-bit quantization affect the quality of chain-of-thought reasoning?",
        "expected_mode": "research_mentor",
        "description": "Impact of quantization on reasoning",
        "tags": ["quantization", "cot", "quality"]
    },
    {
        "id": "gap_007",
        "query": "Would quantized models perform worse with RAG than full-precision models?",
        "expected_mode": "research_mentor",
        "description": "Quantization impact on RAG",
        "tags": ["quantization", "rag", "comparison"]
    },
    {
        "id": "gap_008",
        "query": "Can batching help mitigate the accuracy loss from 4-bit quantization?",
        "expected_mode": "research_mentor",
        "description": "Combining Batching (Section 7) with Quantization (Section 3)",
        "tags": ["batching", "quantization", "cross-section"]
    },

    # --- RAG + Other Concepts ---
    {
        "id": "gap_009",
        "query": "Would using LoRA-tuned embedding models improve RAG performance?",
        "expected_mode": "research_mentor",
        "description": "LoRA for RAG embeddings",
        "tags": ["lora", "rag", "embeddings"]
    },
    {
        "id": "gap_010",
        "query": "Can RAG reduce the need for full fine-tuning in domain adaptation?",
        "expected_mode": "research_mentor",
        "description": "RAG vs fine-tuning for domain adaptation",
        "tags": ["rag", "fine-tuning", "domain"]
    },
    {
        "id": "gap_011",
        "query": "How would RAG latency interact with batching optimizations?",
        "expected_mode": "research_mentor",
        "description": "RAG and batching interaction",
        "tags": ["rag", "batching", "latency"]
    },

    # --- Chain-of-Thought + Other Concepts ---
    {
        "id": "gap_012",
        "query": "Would chain-of-thought prompting be more effective with LoRA-tuned models?",
        "expected_mode": "research_mentor",
        "description": "CoT with LoRA models",
        "tags": ["cot", "lora", "effectiveness"]
    },
    {
        "id": "gap_013",
        "query": "Can CoT prompting help identify when RAG retrieves irrelevant documents?",
        "expected_mode": "research_mentor",
        "description": "CoT for RAG quality assessment",
        "tags": ["cot", "rag", "quality"]
    },

    # --- Deployment + Other Concepts ---
    {
        "id": "gap_014",
        "query": "Would quantization help reduce cold start latency?",
        "expected_mode": "research_mentor",
        "description": "Quantization for cold start",
        "tags": ["quantization", "deployment", "latency"]
    },
    {
        "id": "gap_015",
        "query": "Can prefix tuning reduce memory requirements for concurrent users?",
        "expected_mode": "research_mentor",
        "description": "Prefix tuning for scaling",
        "tags": ["prefix-tuning", "deployment", "memory"]
    },

    # --- Evaluation + Other Concepts ---
    {
        "id": "gap_016",
        "query": "Would MMLU scores correlate better with real-world performance if models used RAG?",
        "expected_mode": "research_mentor",
        "description": "RAG impact on benchmark validity",
        "tags": ["rag", "evaluation", "benchmarks"]
    },
    {
        "id": "gap_017",
        "query": "Can chain-of-thought prompting improve TruthfulQA scores?",
        "expected_mode": "research_mentor",
        "description": "CoT for truthfulness",
        "tags": ["cot", "evaluation", "truthfulness"]
    },

    # --- Multi-concept combinations ---
    {
        "id": "gap_018",
        "query": "Could a LoRA-tuned, 4-bit quantized model with RAG outperform a full-precision model without RAG?",
        "expected_mode": "research_mentor",
        "description": "Three-way combination",
        "tags": ["lora", "quantization", "rag", "multi-concept"]
    },
    {
        "id": "gap_019",
        "query": "How should batching strategy change when using chain-of-thought prompting?",
        "expected_mode": "research_mentor",
        "description": "CoT impact on batching",
        "tags": ["cot", "batching", "strategy"]
    },
    {
        "id": "gap_020",
        "query": "Would prefix tuning help maintain output consistency better than LoRA?",
        "expected_mode": "research_mentor",
        "description": "Comparing fine-tuning methods for consistency",
        "tags": ["prefix-tuning", "lora", "consistency"]
    },

    # --- Novel research directions ---
    {
        "id": "gap_021",
        "query": "Can we use quantization-aware training to make LoRA more efficient?",
        "expected_mode": "research_mentor",
        "description": "Combining two efficiency techniques",
        "tags": ["quantization", "lora", "efficiency"]
    },
    {
        "id": "gap_022",
        "query": "Would models pre-trained with chain-of-thought data need less fine-tuning?",
        "expected_mode": "research_mentor",
        "description": "Pre-training with CoT",
        "tags": ["cot", "pre-training", "fine-tuning"]
    },
    {
        "id": "gap_023",
        "query": "Can RAG help reduce the accuracy gap between 8-bit and 4-bit quantization?",
        "expected_mode": "research_mentor",
        "description": "RAG to compensate for quantization",
        "tags": ["rag", "quantization", "accuracy"]
    },
    {
        "id": "gap_024",
        "query": "How would human evaluation costs change if using chain-of-thought outputs?",
        "expected_mode": "research_mentor",
        "description": "CoT impact on evaluation",
        "tags": ["cot", "evaluation", "cost"]
    },
    {
        "id": "gap_025",
        "query": "Could dense embeddings be quantized without hurting RAG performance?",
        "expected_mode": "research_mentor",
        "description": "Quantizing RAG embeddings",
        "tags": ["quantization", "rag", "embeddings"]
    },

    # --- Challenging edge cases ---
    {
        "id": "gap_026",
        "query": "What happens to chain-of-thought reasoning when memory is constrained by concurrent users?",
        "expected_mode": "research_mentor",
        "description": "CoT under memory pressure",
        "tags": ["cot", "deployment", "memory"]
    },
    {
        "id": "gap_027",
        "query": "Would LoRA adapters trained on different domains interfere with each other?",
        "expected_mode": "research_mentor",
        "description": "Multi-domain LoRA",
        "tags": ["lora", "domain", "interference"]
    },
    {
        "id": "gap_028",
        "query": "Can the 340ms RAG latency be hidden using speculative execution during batching?",
        "expected_mode": "research_mentor",
        "description": "Hiding RAG latency",
        "tags": ["rag", "batching", "latency", "optimization"]
    },
    {
        "id": "gap_029",
        "query": "How should evaluation benchmarks change to account for RAG-augmented models?",
        "expected_mode": "research_mentor",
        "description": "New benchmarks for RAG",
        "tags": ["rag", "evaluation", "benchmarks"]
    },
    {
        "id": "gap_030",
        "query": "Could LoRA be applied to only the layers most affected by quantization to recover accuracy?",
        "expected_mode": "research_mentor",
        "description": "Targeted LoRA for quantization recovery",
        "tags": ["lora", "quantization", "targeted"]
    },
]


# =============================================================================
# HALLUCINATION TEST CASES
# Questions completely unrelated to the knowledge base
# =============================================================================

HALLUCINATION_TESTS = [
    # --- Agriculture / Nature ---
    {
        "id": "halluc_001",
        "query": "What is the best way to grow tomatoes in a greenhouse?",
        "expected_mode": "research_mentor",
        "description": "Agriculture - completely unrelated",
        "tags": ["agriculture", "off-topic"]
    },
    {
        "id": "halluc_002",
        "query": "How do bees communicate the location of flowers?",
        "expected_mode": "research_mentor",
        "description": "Biology - completely unrelated",
        "tags": ["biology", "off-topic"]
    },
    {
        "id": "halluc_003",
        "query": "What causes leaves to change color in autumn?",
        "expected_mode": "research_mentor",
        "description": "Nature - completely unrelated",
        "tags": ["nature", "off-topic"]
    },

    # --- Cooking / Food ---
    {
        "id": "halluc_004",
        "query": "What is the best recipe for chocolate chip cookies?",
        "expected_mode": "research_mentor",
        "description": "Cooking - completely unrelated",
        "tags": ["cooking", "off-topic"]
    },
    {
        "id": "halluc_005",
        "query": "How do you make authentic Italian pasta from scratch?",
        "expected_mode": "research_mentor",
        "description": "Cooking - completely unrelated",
        "tags": ["cooking", "off-topic"]
    },
    {
        "id": "halluc_006",
        "query": "What temperature should steak be cooked to for medium-rare?",
        "expected_mode": "research_mentor",
        "description": "Cooking - completely unrelated",
        "tags": ["cooking", "off-topic"]
    },

    # --- History / Geography ---
    {
        "id": "halluc_007",
        "query": "When was the Great Wall of China built?",
        "expected_mode": "research_mentor",
        "description": "History - completely unrelated",
        "tags": ["history", "off-topic"]
    },
    {
        "id": "halluc_008",
        "query": "What caused the fall of the Roman Empire?",
        "expected_mode": "research_mentor",
        "description": "History - completely unrelated",
        "tags": ["history", "off-topic"]
    },
    {
        "id": "halluc_009",
        "query": "What is the longest river in the world?",
        "expected_mode": "research_mentor",
        "description": "Geography - completely unrelated",
        "tags": ["geography", "off-topic"]
    },

    # --- Sports / Entertainment ---
    {
        "id": "halluc_010",
        "query": "How many players are on a basketball team?",
        "expected_mode": "research_mentor",
        "description": "Sports - completely unrelated",
        "tags": ["sports", "off-topic"]
    },
    {
        "id": "halluc_011",
        "query": "Who directed the movie Inception?",
        "expected_mode": "research_mentor",
        "description": "Entertainment - completely unrelated",
        "tags": ["entertainment", "off-topic"]
    },
    {
        "id": "halluc_012",
        "query": "What are the rules of chess?",
        "expected_mode": "research_mentor",
        "description": "Games - completely unrelated",
        "tags": ["games", "off-topic"]
    },

    # --- Health / Medicine ---
    {
        "id": "halluc_013",
        "query": "What are the symptoms of vitamin D deficiency?",
        "expected_mode": "research_mentor",
        "description": "Health - completely unrelated",
        "tags": ["health", "off-topic"]
    },
    {
        "id": "halluc_014",
        "query": "How does the human heart pump blood?",
        "expected_mode": "research_mentor",
        "description": "Medicine - completely unrelated",
        "tags": ["medicine", "off-topic"]
    },
    {
        "id": "halluc_015",
        "query": "What causes migraine headaches?",
        "expected_mode": "research_mentor",
        "description": "Health - completely unrelated",
        "tags": ["health", "off-topic"]
    },

    # --- Physics / Chemistry (non-ML) ---
    {
        "id": "halluc_016",
        "query": "How do black holes form?",
        "expected_mode": "research_mentor",
        "description": "Astrophysics - completely unrelated",
        "tags": ["physics", "off-topic"]
    },
    {
        "id": "halluc_017",
        "query": "What is the chemical formula for table salt?",
        "expected_mode": "research_mentor",
        "description": "Chemistry - completely unrelated",
        "tags": ["chemistry", "off-topic"]
    },
    {
        "id": "halluc_018",
        "query": "How does nuclear fusion work?",
        "expected_mode": "research_mentor",
        "description": "Physics - completely unrelated",
        "tags": ["physics", "off-topic"]
    },

    # --- Economics / Finance ---
    {
        "id": "halluc_019",
        "query": "How does compound interest work?",
        "expected_mode": "research_mentor",
        "description": "Finance - completely unrelated",
        "tags": ["finance", "off-topic"]
    },
    {
        "id": "halluc_020",
        "query": "What causes inflation in an economy?",
        "expected_mode": "research_mentor",
        "description": "Economics - completely unrelated",
        "tags": ["economics", "off-topic"]
    },
    {
        "id": "halluc_021",
        "query": "How does the stock market work?",
        "expected_mode": "research_mentor",
        "description": "Finance - completely unrelated",
        "tags": ["finance", "off-topic"]
    },

    # --- Arts / Music ---
    {
        "id": "halluc_022",
        "query": "How do you read sheet music?",
        "expected_mode": "research_mentor",
        "description": "Music - completely unrelated",
        "tags": ["music", "off-topic"]
    },
    {
        "id": "halluc_023",
        "query": "What makes the Mona Lisa famous?",
        "expected_mode": "research_mentor",
        "description": "Art - completely unrelated",
        "tags": ["art", "off-topic"]
    },
    {
        "id": "halluc_024",
        "query": "How do you tune a guitar?",
        "expected_mode": "research_mentor",
        "description": "Music - completely unrelated",
        "tags": ["music", "off-topic"]
    },

    # --- Daily Life / Practical ---
    {
        "id": "halluc_025",
        "query": "How do you change a flat tire?",
        "expected_mode": "research_mentor",
        "description": "Practical - completely unrelated",
        "tags": ["practical", "off-topic"]
    },
    {
        "id": "halluc_026",
        "query": "What's the best way to remove a coffee stain?",
        "expected_mode": "research_mentor",
        "description": "Practical - completely unrelated",
        "tags": ["practical", "off-topic"]
    },
    {
        "id": "halluc_027",
        "query": "How do airplanes stay in the air?",
        "expected_mode": "research_mentor",
        "description": "Aviation - completely unrelated",
        "tags": ["aviation", "off-topic"]
    },

    # --- Philosophy / Abstract ---
    {
        "id": "halluc_028",
        "query": "What is the meaning of life?",
        "expected_mode": "research_mentor",
        "description": "Philosophy - completely unrelated",
        "tags": ["philosophy", "off-topic"]
    },
    {
        "id": "halluc_029",
        "query": "Do we have free will?",
        "expected_mode": "research_mentor",
        "description": "Philosophy - completely unrelated",
        "tags": ["philosophy", "off-topic"]
    },
    {
        "id": "halluc_030",
        "query": "What makes something beautiful?",
        "expected_mode": "research_mentor",
        "description": "Aesthetics - completely unrelated",
        "tags": ["philosophy", "off-topic"]
    },
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_tests():
    """Return all test cases."""
    return {
        "known": KNOWN_TESTS,
        "gap": GAP_TESTS,
        "hallucination": HALLUCINATION_TESTS
    }

def get_tests_by_tag(tag: str):
    """Return all test cases with a specific tag."""
    results = []
    for test in KNOWN_TESTS + GAP_TESTS + HALLUCINATION_TESTS:
        if tag in test.get("tags", []):
            results.append(test)
    return results

def get_test_by_id(test_id: str):
    """Return a specific test case by ID."""
    for test in KNOWN_TESTS + GAP_TESTS + HALLUCINATION_TESTS:
        if test["id"] == test_id:
            return test
    return None

def get_test_summary():
    """Return a summary of test cases."""
    return {
        "known_count": len(KNOWN_TESTS),
        "gap_count": len(GAP_TESTS),
        "hallucination_count": len(HALLUCINATION_TESTS),
        "total": len(KNOWN_TESTS) + len(GAP_TESTS) + len(HALLUCINATION_TESTS)
    }


if __name__ == "__main__":
    summary = get_test_summary()
    print("Test Case Summary:")
    print(f"  Known Tests: {summary['known_count']}")
    print(f"  Gap Tests: {summary['gap_count']}")
    print(f"  Hallucination Tests: {summary['hallucination_count']}")
    print(f"  Total: {summary['total']}")
