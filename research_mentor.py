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
GAP_THRESHOLD = CONFIG["gap_threshold"] 

class ResearchMentorSystem:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=CONFIG["gemini_api_key"])
        self.vector_db = None
        self.llm_librarian = GoogleGenerativeAI(model=CONFIG["gemini_model"], google_api_key=CONFIG["gemini_api_key"], temperature=0)
        self.llm_dreamer = GoogleGenerativeAI(model=CONFIG["gemini_model"], google_api_key=CONFIG["gemini_api_key"], temperature=1.2)
        self.llm_critic = GoogleGenerativeAI(model=CONFIG["gemini_model"], google_api_key=CONFIG["gemini_api_key"], temperature=0)

    def ingest_documents(self, pdf_paths: List[str]):
        """
        Loads PDFs, splits them, and creates the Vector DB.
        """
        print(f"📚 Ingesting {len(pdf_paths)} documents...")
        docs = []
        for path in pdf_paths:
            if os.path.exists(path):
                loader = PyPDFLoader(path)
                docs.extend(loader.load())
            else:
                print(f"⚠️ Warning: File not found: {path}")

        # Split text for better retrieval
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # Create/Update Vector DB
        self.vector_db = Chroma.from_documents(
            documents=splits, 
            embedding=self.embeddings,
            persist_directory=VECTOR_DB_PATH
        )
        print(f"✅ Knowledge Base Ready with {len(splits)} chunks.")

    def create_dummy_paper(self):
        """
        Creates a fake research paper for testing purposes if you don't have PDFs.
        """
        content = """
        Title: Analysis of Distributed Consensus in High-Latency Networks
        Abstract: We explore the Paxos algorithm applied to interplanetary networks.
        
        Section 1: Introduction
        Standard consensus algorithms fail when latency exceeds 10 minutes.
        We observe that Paxos requires synchronous rounds which are impossible on Mars.
        
        Section 2: The Time-Warp Limitation
        Our experiments show that packet loss correlates linearly with solar flares.
        However, we established that Raft is strictly worse than Paxos in this domain.
        There is no known method to bridge the 20-minute light delay gap for real-time consistency.
        """
        filename = "dummy_paper.pdf"
        # We can just simulate loading this text directly to avoid PDF dependency for this demo
        # But to keep the pipeline pure, let's just make a text file and load it as a Document
        return [Document(page_content=content, metadata={"source": "dummy_paper"})]

    def ingest_dummy_data(self):    
        """Helper to load dummy data without needing real PDFs"""
        print("📚 Loading dummy research data...")
        docs = self.create_dummy_paper()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)
        self.vector_db = Chroma.from_documents(splits, self.embeddings)
        print("✅ Dummy Knowledge Base Ready.")

    def retrieve_context(self, query: str) -> Tuple[str, float]:
        """
        The Librarian: Retrieves context and checks the distance score.
        Returns: (context_text, best_distance_score)
        """
        if not self.vector_db:
            return "No database loaded.", 1.0

        # similarity_search_with_score returns L2 distance (Lower is better)
        # 0.0 = Exact Match, > 1.0 = Very poor match
        results = self.vector_db.similarity_search_with_score(query, k=3)
        
        if not results:
            return "", 1.0

        best_doc, best_score = results[0]
        context_text = "\n\n".join([doc.page_content for doc, score in results])
        
        return context_text, best_score

    def run_librarian_mode(self, query, context):
        """Standard RAG response"""
        prompt = f"""
        You are an expert Research Librarian. Answer the user's query strictly based on the context below.
        If the answer is not in the context, admit it.
        
        Context: {context}
        
        User Query: {query}
        """
        return self.llm_librarian.invoke(prompt)

    def run_dreamer_mode(self, query, context):
        """
        The Dreamer: Generates novel hypotheses.
        """
        prompt = f"""
        You are a visionary Principal Investigator (PI) in Computer Science.
        The user asked: "{query}"
        
        Our current literature (context below) does NOT contain a direct answer.
        Context: {context}
        
        Your Task:
        1. Acknowledge the gap in the literature.
        2. Propose 2 NOVEL hypotheses or theoretical frameworks that might answer the question.
        3. You may "hallucinate" new connections, but they must be grounded in scientific principles.
        4. Do NOT cite fake papers.
        """
        print("   ... 🧠 Dreaming up hypotheses (Temp=1.2)...")
        return self.llm_dreamer.invoke(prompt)

    def run_critic_mode(self, hypotheses):
        """
        The Critic: Checks for feasibility.
        """
        prompt = f"""
        You are "Reviewer #2" for a top-tier academic journal.
        Evaluate the following hypotheses for scientific validity and feasibility.
        
        Hypotheses:
        {hypotheses}
        
        Your Task:
        1. Identify any logical fallacies or physical impossibilities.
        2. Assign a "Feasibility Score" (0-10) to each.
        3. Provide a harsh but constructive critique.
        """
        print("   ... 🧐 Critiquing logic (Temp=0)...")
        return self.llm_critic.invoke(prompt)

    def process_query(self, query: str):
        print(f"\n\n🔍 Analyzing Query: '{query}'")
        
        # 1. RETRIEVE
        context, score = self.retrieve_context(query)
        print(f"   ... Top Match Score: {score:.4f} (Threshold: {GAP_THRESHOLD})")

        # 2. GAP DETECTION
        if score < GAP_THRESHOLD:
            # High Similarity (Low Distance) -> Answer Factually
            print("   ✅ Knowledge Found. Running LIBRARIAN MODE.")
            response = self.run_librarian_mode(query, context)
            print(f"\n--- 📖 LIBRARIAN RESPONSE ---\n{response}")
            
        else:
            # Low Similarity (High Distance) -> Gap Detected
            print("   ⚠️  Knowledge Gap Detected. Switching to RESEARCH MENTOR MODE.")
            
            # 3. DREAM
            hypotheses = self.run_dreamer_mode(query, context)
            
            # 4. CRITIQUE
            critique = self.run_critic_mode(hypotheses)
            
            print(f"\n--- 🧪 PROPOSED HYPOTHESES ---\n{hypotheses}")
            print(f"\n--- 📝 REVIEWER CRITIQUE ---\n{critique}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    mentor = ResearchMentorSystem()
    
    # SETUP: Load Dummy Data
    mentor.ingest_dummy_data()
    
    # TEST CASE 1: The "Known" Query
    mentor.process_query("How does packet loss correlate with solar flares?")
    
    # TEST CASE 2: The "Gap" Query
    mentor.process_query("Could we use Quantum Entanglement to fix the latency issue in Paxos?")