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
    # --- LoRA (Hu et al., 2021) ---
    {
        "id": "known_001",
        "query": "How much does LoRA reduce the number of trainable parameters compared to full fine-tuning?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["10,000", "10000"],
        "description": "LoRA reduces trainable parameters by 10,000x vs GPT-3 175B",
        "tags": ["lora", "fine-tuning", "exact-number"]
    },
    {
        "id": "known_002",
        "query": "How much does LoRA reduce GPU memory requirements?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["3", "VRAM"],
        "description": "LoRA reduces GPU memory by up to 2/3 (3x reduction)",
        "tags": ["lora", "fine-tuning", "memory"]
    },
    {
        "id": "known_003",
        "query": "Does LoRA introduce additional inference latency compared to full fine-tuning?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["no additional", "no inference latency"],
        "description": "LoRA adds no inference latency by merging weights",
        "tags": ["lora", "inference", "latency"]
    },
    {
        "id": "known_004",
        "query": "What models was LoRA evaluated on?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["RoBERTa", "GPT"],
        "description": "LoRA tested on RoBERTa, DeBERTa, GPT-2, GPT-3",
        "tags": ["lora", "evaluation"]
    },
    {
        "id": "known_005",
        "query": "How much does LoRA reduce the checkpoint size for GPT-3 175B?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["10,000", "350GB", "35MB"],
        "description": "Checkpoint reduced ~10,000x from 350GB to 35MB",
        "tags": ["lora", "storage", "exact-number"]
    },

    # --- QLoRA (Dettmers et al., 2023) ---
    {
        "id": "known_006",
        "query": "What size GPU can QLoRA use to finetune a 65B parameter model?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["48GB", "single"],
        "description": "QLoRA finetunes 65B on a single 48GB GPU",
        "tags": ["qlora", "hardware", "exact-number"]
    },
    {
        "id": "known_007",
        "query": "What percentage of ChatGPT's performance does Guanaco achieve on the Vicuna benchmark?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["99.3%", "99.3"],
        "description": "Guanaco reaches 99.3% of ChatGPT performance",
        "tags": ["qlora", "guanaco", "exact-number"]
    },
    {
        "id": "known_008",
        "query": "What are the three key innovations introduced in QLoRA?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["NormalFloat", "Double Quantization", "Paged Optimizers"],
        "description": "QLoRA introduces NF4, Double Quantization, Paged Optimizers",
        "tags": ["qlora", "innovations", "enumeration"]
    },
    {
        "id": "known_009",
        "query": "How much GPU memory does regular 16-bit finetuning of a LLaMA 65B model require?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["780", "GB"],
        "description": "Regular 16-bit finetuning requires >780 GB",
        "tags": ["qlora", "memory", "exact-number"]
    },

    # --- LLM.int8() (Dettmers et al., 2022) ---
    {
        "id": "known_010",
        "query": "How much does LLM.int8() reduce the memory needed for inference?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["half", "50%"],
        "description": "LLM.int8() cuts inference memory by half",
        "tags": ["quantization", "8-bit", "memory"]
    },
    {
        "id": "known_011",
        "query": "What percentage of values are multiplied in 8-bit in the LLM.int8() method?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["99.9%", "99.9"],
        "description": "99.9% of values use 8-bit multiplication",
        "tags": ["quantization", "8-bit", "exact-number"]
    },
    {
        "id": "known_012",
        "query": "At what model scale do outlier features emerge that break standard quantization?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["6.7B", "6.7 billion"],
        "description": "Outlier features emerge at 6.7B parameter scale",
        "tags": ["quantization", "outliers", "exact-number"]
    },

    # --- GPTQ (Frantar et al., 2022) ---
    {
        "id": "known_013",
        "query": "How long does GPTQ take to quantize a 175 billion parameter model?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["4", "GPU hours", "four"],
        "description": "GPTQ quantizes 175B models in ~4 GPU hours",
        "tags": ["gptq", "quantization", "exact-number"]
    },
    {
        "id": "known_014",
        "query": "How many bits per weight does GPTQ compress models to?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["3", "4", "bits"],
        "description": "GPTQ compresses to 3-4 bits per weight",
        "tags": ["gptq", "quantization", "compression"]
    },
    {
        "id": "known_015",
        "query": "What inference speedup does GPTQ achieve on an NVIDIA A100 GPU?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["3.25", "3.25x"],
        "description": "GPTQ achieves 3.25x speedup on A100",
        "tags": ["gptq", "speedup", "exact-number"]
    },

    # --- RAG (Lewis et al., 2020) ---
    {
        "id": "known_016",
        "query": "What are the two types of memory that RAG combines?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["parametric", "non-parametric"],
        "description": "RAG combines parametric and non-parametric memory",
        "tags": ["rag", "architecture"]
    },
    {
        "id": "known_017",
        "query": "What generator model does RAG use?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["BART", "400M"],
        "description": "RAG uses BART-large (400M parameters) as generator",
        "tags": ["rag", "generator", "architecture"]
    },
    {
        "id": "known_018",
        "query": "What open-domain QA datasets did RAG set state-of-the-art results on?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["Natural Questions", "WebQuestions", "CuratedTrec"],
        "description": "RAG SOTA on NQ, WQ, CuratedTrec",
        "tags": ["rag", "benchmarks"]
    },

    # --- Chain-of-Thought (Wei et al., 2022) ---
    {
        "id": "known_019",
        "query": "What benchmark did PaLM 540B with chain-of-thought prompting achieve state-of-the-art on?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["GSM8K"],
        "description": "PaLM 540B with CoT achieves SOTA on GSM8K",
        "tags": ["cot", "benchmark", "math"]
    },
    {
        "id": "known_020",
        "query": "What is chain-of-thought prompting?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["intermediate", "reasoning", "steps"],
        "description": "CoT = series of intermediate reasoning steps",
        "tags": ["cot", "definition"]
    },
    {
        "id": "known_021",
        "query": "How many chain-of-thought exemplars were used in the PaLM 540B GSM8K experiment?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["eight", "8"],
        "description": "Eight CoT exemplars used for SOTA result",
        "tags": ["cot", "exact-number"]
    },
    {
        "id": "known_022",
        "query": "At what model scale does chain-of-thought prompting become effective?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["100B", "100 billion", "large"],
        "description": "CoT is an emergent ability in ~100B+ parameter models",
        "tags": ["cot", "scale", "emergent"]
    },

    # --- Prefix-Tuning (Li & Liang, 2021) ---
    {
        "id": "known_023",
        "query": "What percentage of the parameters does prefix-tuning learn compared to full fine-tuning?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["0.1%"],
        "description": "Prefix-tuning learns only 0.1% of parameters",
        "tags": ["prefix-tuning", "exact-number"]
    },
    {
        "id": "known_024",
        "query": "How does prefix-tuning compare to fine-tuning in terms of storage?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["1000", "fewer"],
        "description": "Prefix-tuning stores 1000x fewer parameters",
        "tags": ["prefix-tuning", "storage"]
    },
    {
        "id": "known_025",
        "query": "What tasks was prefix-tuning evaluated on?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["table-to-text", "summarization"],
        "description": "Prefix-tuning tested on table-to-text and summarization",
        "tags": ["prefix-tuning", "tasks"]
    },

    # --- Attention Is All You Need (Vaswani et al., 2017) ---
    {
        "id": "known_026",
        "query": "What BLEU score did the Transformer achieve on the WMT 2014 English-to-German translation task?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["28.4"],
        "description": "Transformer achieves 28.4 BLEU on EN-DE",
        "tags": ["transformer", "bleu", "exact-number"]
    },
    {
        "id": "known_027",
        "query": "How many attention heads does the original Transformer model use?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["8", "eight"],
        "description": "Transformer uses h=8 parallel attention heads",
        "tags": ["transformer", "architecture", "exact-number"]
    },
    {
        "id": "known_028",
        "query": "What is the model dimension d_model in the original Transformer?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["512"],
        "description": "Transformer uses d_model=512",
        "tags": ["transformer", "architecture", "exact-number"]
    },

    # --- LLM Evaluation Survey (Chang et al., 2023) ---
    {
        "id": "known_029",
        "query": "What are the three key dimensions of LLM evaluation discussed in the survey by Chang et al.?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["what to evaluate", "where to evaluate", "how to evaluate"],
        "description": "Three dimensions: what, where, how to evaluate",
        "tags": ["evaluation", "survey", "dimensions"]
    },

    # --- Efficient LLMs Survey (Wan et al., 2023) ---
    {
        "id": "known_030",
        "query": "What are the three main categories in the efficient LLMs taxonomy?",
        "expected_mode": "librarian",
        "expected_answer_contains": ["model-centric", "data-centric", "framework"],
        "description": "Taxonomy: model-centric, data-centric, framework-centric",
        "tags": ["efficiency", "survey", "taxonomy"]
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
