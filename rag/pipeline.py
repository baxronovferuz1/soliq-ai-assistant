import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from llm.llm_client import LLMClient
from vector_db.faiss_store import FaissStore


def format_docs(docs):
    """Documentlarni bitta matnga aylantiradi"""
    return "\n\n".join(doc.page_content for doc in docs)


class RAGPipeline:
    def __init__(self):
        self.llm = LLMClient().get_llm()
        
        
        self.retriever = FaissStore().as_retriever(
            search_type="similarity",   
            search_kwargs={"k": 12}     
        )

        prompt_template = """Siz O'zbekiston Respublikasi soliq qonunlari bo'yicha mutaxassis yordamchi botsiz.

Quyidagi kontekstdan **har qanday** ma'lumotni ishlatib, aniq, to'liq va professional javob bering.
Agar kontekstda biror ma'lumot bo'lsa, uni albatta ishlating. "Ma'lumot yo'q" deb hech qachon yozmang.

Kontekst:
{context}

Savol: {question}

Javob (faqat o'zbek tilida, aniq va batafsil):"""

        self.prompt = PromptTemplate.from_template(prompt_template)

        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def query(self, question: str) -> str:
        return self.chain.invoke(question)