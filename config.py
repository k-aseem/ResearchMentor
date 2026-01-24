import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CONFIG = {
    # API Keys
    "gemini_api_key": os.getenv("GEMINI_API_KEY"),

    # Models
    "gemini_model": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
    "embedding_model": os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),

    # Paths
    "vector_db_path": os.getenv("VECTOR_DB_PATH", "./chroma_db"),

    # Thresholds (0 to 1, higher = stricter match required for Librarian mode)
    "similarity_threshold": float(os.getenv("SIMILARITY_THRESHOLD", "0.55")),
}
