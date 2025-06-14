import os
import pandas as pd
from langchain_community.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from backend.core.config import embedding_model, CHROMA_DIR, DATA_DIR

# Define department-wise metadata
METADATA_LOOKUP = {
    "engineering": {
        "access": ["Engineering", "C-Level"],
        "sensitivity": "high",
        "owner": "Engineering Team",
        "purpose": "Reference for audits, onboarding, scaling, and system maintenance",
    },
    "finance": {
        "access": ["Finance", "C-Level"],
        "sensitivity": "high",
        "owner": "Finance Team",
        "purpose": "Financial planning, audits, investor reporting, and strategic decisions",
    },
    "general": {
        "access": ["Employee", "HR", "C-Level", "Finance", "Engineering", "Marketing"],
        "sensitivity": "low",
        "owner": "HR Department",
        "purpose": "Employee onboarding, policy clarification, and general info",
    },
    "hr": {
        "access": ["HR", "C-Level"],
        "sensitivity": "medium",
        "owner": "HR & People Analytics Team",
        "purpose": "Talent forecasting, compliance reporting, and engagement insights",
    },
    "marketing": {
        "access": ["Marketing", "C-Level"],
        "sensitivity": "medium",
        "owner": "Marketing Team",
        "purpose": "Quarterly planning, performance reviews, and strategic decisions",
    }
}

def ingest():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=300,
        separators=["\n\n", "\n", ".", " "]
    )

    all_docs = []

    for dept, metadata in METADATA_LOOKUP.items():
        dept_path = os.path.join(DATA_DIR, dept)
        if not os.path.exists(dept_path):
            print(f"⚠️ Skipping missing directory: {dept_path}")
            continue

        for filename in os.listdir(dept_path):
            path = os.path.join(dept_path, filename)
            if filename.endswith(".md"):
                loader = TextLoader(path, encoding="utf-8")
                docs = loader.load()
            elif filename.endswith(".csv"):
                df = pd.read_csv(path)
                docs = [
                    Document(page_content=row.to_json(), metadata={"source": filename})
                    for _, row in df.iterrows()
                ]
            else:
                continue

            for doc in docs:
                # Standard metadata
                doc.metadata.update({
                    "department": dept,
                    "filename": filename,
                    "sensitivity": metadata["sensitivity"],
                    "owner": metadata["owner"],
                    "purpose": metadata["purpose"],
                })

                # ✅ Role-specific boolean flags
                for role in metadata["access"]:
                    doc.metadata[f"role_{role}"] = True

                all_docs.append(doc)
                print(f"Ingested: {filename} with department: {dept}")

    chunks = splitter.split_documents(all_docs)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR
    )
    print("✅ Ingestion complete")

if __name__ == "__main__":
    ingest()
