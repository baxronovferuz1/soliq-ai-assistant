import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

class LLMClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.llm = ChatGroq(
                model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),   
                temperature=float(os.getenv("TEMPERATURE", "0.1")),
                max_tokens=int(os.getenv("MAX_TOKENS", "4096")),           
                api_key=os.getenv("GROQ_API_KEY"),
            )
        return cls._instance

    def get_llm(self):
        return self.llm