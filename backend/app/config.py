import os

from dotenv import load_dotenv

load_dotenv()

LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "http://localhost:11434")
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2")
MCP_SERVER_URL: str = os.getenv("MCP_SERVER_URL", "http://localhost:8001/sse")
