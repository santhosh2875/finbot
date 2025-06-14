# File: backend/api/chatbot.py
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from backend.core.config import OPENROUTER_API_KEY
from backend.core.vectorstore import get_chroma_retriever

# Prompt used for answering questions
prompt = PromptTemplate.from_template(
   "You are FinBot, an internal assistant at FinSolve Technologies.\n"
    "Answer the following question using ONLY the information provided in the context below.\n"
    "If the context does not contain the answer, reply with: \"Sorry, I couldn't find that in the documents or you dont have acesses to it.\"\n\n"
    "Context:\n{context}\n\nQuestion: {question}")

# LLM configured to use OpenRouter's Mistral 7B
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    model="mistralai/mistral-7b-instruct",
    temperature=0
)

# Build the RAG chain for a given role
def get_qa_chain(role):
    retriever = get_chroma_retriever(role)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

# Called by the /chat endpoint to handle user queries
def get_answer(query, role):
    retriever = get_chroma_retriever(role)
    docs = retriever.get_relevant_documents(query)

    print(f"🔍 Retrieved {len(docs)} Chunks:")
    for i, doc in enumerate(docs):
        print(f"→ [{i+1}] {doc.metadata.get('filename', 'unknown')}")
        print(doc.page_content[:200])
        print("-" * 50)

    if not docs:
        return {
            "answer": (
                "📄 I'm sorry, but I couldn't find relevant content in the documents to answer your query. "
                "Please try rephrasing your question or check with the admin if the data is available."
            ),
            "sources": []
        }

    chain = get_qa_chain(role)
    result = chain.invoke({"query": query})

    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result.get("source_documents", [])]
    }
