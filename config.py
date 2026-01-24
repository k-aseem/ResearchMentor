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

    # Thresholds
    "gap_threshold": float(os.getenv("GAP_THRESHOLD", "0.4")),
}
