# 🤖 FinBot – RAG-Based Chatbot with Role-Based Access (Codebasics Challenge #1)

**FinBot** is a secure, role-aware AI assistant built for internal company use. It uses **Retrieval-Augmented Generation (RAG)** to help employees answer department-specific queries based on their role — while ensuring **no unauthorized access** to sensitive data.

Built for [Codebasics AI Challenge #1](https://codebasics.io/challenges/rag-chatbot-rbac-submission), FinBot blends **FastAPI, LangChain, ChromaDB, and OpenRouter** into a smooth, intelligent chatbot experience.

---

## 🚀 Features

- 🔐 **JWT-based login & authentication**
- 👥 **Role-Based Access Control (RBAC)** for document-level filtering
- 📄 **RAG pipeline** using LangChain + ChromaDB
- 🤖 **Mistral-7B** LLM via OpenRouter
- 🧠 Document chunking, metadata tagging & filtering
- 🌐 **Streamlit UI** as the primary interface


---

## ⚙️ Tech Stack

| Component     | Tool/Service                              |
|---------------|-------------------------------------------|
| LLM           | OpenRouter (mistralai/mistral-7b-instruct)|
| Backend       | FastAPI                                   |
| Frontend      | Streamlit                                 |
| Vector Store  | ChromaDB                                  |
| Embeddings    | Sentence Transformers (MiniLM)            |
| RAG Pipeline  | LangChain                                 |
| Auth System   | JWT (`python-jose`)                       |

---

## 👥 Role Definitions & Access

| Role        | Access To Documents              |
|-------------|----------------------------------|
| **Finance**     | Finance + General             |
| **HR**          | HR + General                  |
| **Marketing**   | Marketing + General           |
| **Engineering** | Engineering + General         |
| **C-Level**     | All departments               |
| **Employee**    | General only                  |

🔒 Access is enforced at **document chunk level** using metadata like `role_Finance=True`.

---

## 🧱 Architecture Overview

[Streamlit UI] --> /login --> [FastAPI Backend] --> [JWT Token Issued]
                                     ↓
                                /chat POST
                                     ↓
                            Role-Based Filter
                                     ↓
                            [ChromaDB + LangChain]
                                     ↓
                          [OpenRouter LLM → Answer]
                                     ↓
                          [Response + Source shown]


Documents are:

-Chunked using RecursiveCharacterTextSplitter

-Embedded using MiniLM

-Tagged with metadata (department, roles, access flags)

-Retrieved using LangChain retriever with role-based filtering



🛠️ Setup Instructions:
recommended python version:
----Python 3.11.0----------

🐍 1. Create  Virtual Environment
 
📦 Step 1: Open a terminal inside your project directory and run:
    python -m venv venv

⚙️ Step 2: Activate the Virtual Environment
    .\venv\Scripts\Activate.ps1


🧪 2. Install Dependencies

  pip install -r requirements.txt


🔐 3. Configure .env
---.env file in the root directory of the project:
---Paste your OpenRouter API key into it like this:

OPENROUTER_API_KEY=paste your your_openrouter_key


  
📂 4. Ingest Documents into Chroma
 # ✅ This will generate the chroma_db folder from your markdown and CSV files

   python -m backend.ingest


▶️ How to Run the Project

🟢 1. Start Backend (FastAPI)
   
    uvicorn backend.api.main:app --reload


🖥️ 2. Start Frontend (Streamlit)
    
    streamlit run frontend/app.py

    - Visit: http://localhost:8501




💬 Usage Example


Username: alice||bob||john||eve||dan||-- (any one!!)
password: password123

------------------
Ask Question according to the role:
-What is the company’s vision and mission?--(emploee)
-Where is FinSolve headquartered?--(engineering)
-What was the total revenue in Q4 2024?--(finace)
-What was the customer acquisition target for Q4 2024?--(marketing)
-any question from the company for-- (c-Level)





✅ FinBot will:

-Verify JWT

-Filter chunks by role

-Use Mistral-7B to answer using roles accesed  docs only



📁 Folder Structure:

    finbot/
    ├── .env
    ├── README.MD
    ├── requirements.txt
    ├── backend/
    │   ├── ingest.py
    │   ├── users.db
    │   ├── api/
    │   │   ├── auth.py
    │   │   ├── chatbot.py
    │   │   ├── main.py
    │   │   ├── models.py
    │   ├── core/
    │   │   ├── config.py
    │   │   ├── vectorstore.py
    │   ├── db/
    │   │   ├── user_db.py
    ├── data/
    │   ├── engineering/
    │   ├── finance/
    │   ├── general/
    │   ├── hr/
    │   └── marketing/
    └── frontend/
        └── app.py




## 👨‍💻 Author

**Santhosh Kumar**  
📍 Chennai, India  
🎓 Recently completed 3rd year of B.Sc. Computer Science  
🚀 Aspiring **Generative AI / LLM Engineer**  
🧠 Passionate about building intelligent tools powered by modern AI techniques like RAG, AI Agents ,etc... 
💡 FinBot was developed as part of [Codebasics Challenge #1](https://codebasics.io/challenges), combining real-world architecture with secure, role-aware document retrieval using LLMs.  
🔍 Eager to explore opportunities in Generative AI, LangChain development, and full-stack AI systems
