# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent))
# import os

# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from embeddings.embad import Embeddings
# from langchain_community.vectorstores import FAISS

# def ingest_documents():
#     os.makedirs("vector_db", exist_ok=True)
    
#     print("📄 PDF lar yuklanmoqda...")
#     loader = PyPDFDirectoryLoader("data")
#     documents = loader.load()
    
#     print(f"📚 {len(documents)} ta hujjat topildi. Split qilinmoqda...")
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#         length_function=len,
#     )
#     splits = text_splitter.split_documents(documents)
    
#     print("🔢 Embedding yaratilmoqda...")
#     embeddings = Embeddings().get_embeddings()
    
#     vectorstore = FAISS.from_documents(splits, embeddings)
#     vectorstore.save_local("vector_db/faiss_index")
    
#     print(f"✅ Ingestion tugadi! {len(splits)} ta chunk saqlandi.")

# if __name__ == "__main__":
#     ingest_documents()


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import os

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings.embad import Embeddings
from langchain_community.vectorstores import FAISS

def ingest_documents():
    os.makedirs("vector_db", exist_ok=True)
    
    print("📄 PDF lar yuklanmoqda...")
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()
    
    print(f"📚 {len(documents)} ta hujjat topildi. Split qilinmoqda...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,      
        chunk_overlap=300,    
        length_function=len,
    )
    splits = text_splitter.split_documents(documents)
    
    print("🔢 Embedding yaratilmoqda...")
    embeddings = Embeddings().get_embeddings()
    
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local("vector_db/faiss_index")
    
    print(f"✅ Ingestion tugadi! {len(splits)} ta chunk saqlandi.")

if __name__ == "__main__":
    ingest_documents()