from langchain_community.vectorstores import Chroma
from backend.core.config import CHROMA_DIR, embedding_model


def get_chroma_retriever(role: str):
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model
    ).as_retriever(
        search_kwargs={
            "k": 8,
            "filter": {f"role_{role}": True}
        }
    )


# File: backend/api/chatbot.py
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from backend.core.config import OPENROUTER_API_KEY
from backend.core.vectorstore import get_chroma_retriever

prompt = PromptTemplate.from_template(
    "You are a helpful assistant. Use the following documents to answer the question.\n\n{context}\n\nQuestion: {question}"
)

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    model="mistralai/mistral-7b-instruct",
    temperature=0
)


def get_qa_chain(role):
    retriever = get_chroma_retriever(role)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )


def get_answer(query, role):
    chain = get_qa_chain(role)
    result = chain({"query": query})
    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result.get("source_documents", [])]
    }
