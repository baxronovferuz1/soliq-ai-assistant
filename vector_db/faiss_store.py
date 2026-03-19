import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).parent.parent))

from embeddings.embad import Embeddings
from langchain_community.vectorstores import FAISS


class FaissStore:
    INDEX_PATH = str(Path(__file__).parent.parent / "vector_db" / "faiss_index")

    def __init__(self):
        self.embeddings = Embeddings().get_embeddings()

        if not os.path.exists(self.INDEX_PATH):
            raise FileNotFoundError(
                f"❌ Vector DB topilmadi!\n"
                f"Path: {self.INDEX_PATH}\n"
                f"Avval ingestion.py ni ishga tushiring."
            )

        self.vectorstore = FAISS.load_local(
            self.INDEX_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

    
    def as_retriever(self, search_type="similarity", search_kwargs=None):
        if search_kwargs is None:
            search_kwargs = {"k": 12}          # default 12 ta chunk
        
        return self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )