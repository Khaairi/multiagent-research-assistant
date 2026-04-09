import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")

DB_PATH: str = os.getenv("DB_PATH", "research_results.db")

GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX_ID: str | None = os.getenv("GOOGLE_CX_ID")