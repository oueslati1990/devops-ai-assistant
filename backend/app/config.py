import os

from dotenv import load_dotenv

load_dotenv()

LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "http://localhost:11434")
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2")
