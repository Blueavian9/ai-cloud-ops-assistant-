from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document

class QASystem:
    def __init__(self, openai_api_key: str, vector_store):
        """Initialize the QA system with OpenAI and vector store."""
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0
        )
        self.vector_store = vector_store
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.vector_store.as_retriever(
                search_kwargs={"k": 4}
            )
        )

    def answer_question(self, question: str) -> Dict:
        """Answer a question using the QA chain."""
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "sources": self._get_sources(result)
            }
        except Exception as e:
            return {
                "answer": f"Error: {str(e)}",
                "sources": []
            }

    def _get_sources(self, result: Dict) -> List[Dict]:
        """Extract source documents from the QA result."""
        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                sources.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
        return sources 