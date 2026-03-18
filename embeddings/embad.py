import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from langchain_huggingface import HuggingFaceEmbeddings

class Embeddings:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def get_embeddings(self):
        return self.embeddings