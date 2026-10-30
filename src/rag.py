import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.tools import tool

CHROMA_DB_DIR = "./chroma_db"
DATA_DIR = "./data"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def initialize_vector_store():
    """Loads markdown files, chunks them, and builds the Chroma database."""
    
    if os.path.exists(CHROMA_DB_DIR) and len(os.listdir(CHROMA_DB_DIR)) > 0:
        print("Loading existing ChromaDB from disk...")
        return Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)

    print(f"Building new ChromaDB from {DATA_DIR}/ directory...")
    md_files = glob.glob(os.path.join(DATA_DIR, "*.md"))
    
    if not md_files:
        raise FileNotFoundError(f"No .md files found in {DATA_DIR}. Please add your policy documents.")

    documents = []
    for file_path in md_files:
        loader = TextLoader(file_path, encoding="utf-8")
        documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)

    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_DB_DIR
    )
    return vector_store

vector_store = initialize_vector_store()

@tool
def query_company_policy(topic: str) -> str:
    """
    Searches the internal company knowledge base for IT troubleshooting steps, 
    refund policies, and escalation SLAs. Use this tool BEFORE giving the user advice
    or taking action on hardware/software complaints.
    """
    results = vector_store.similarity_search(topic, k=2)
    
    if not results:
        return "No relevant policy or troubleshooting steps found in the knowledge base."
        
    formatted_results = "\n\n".join([doc.page_content for doc in results])
    return f"--- KNOWLEDGE BASE RESULTS ---\n{formatted_results}\n------------------------------"

if __name__ == "__main__":
    print("\nTesting RAG Pipeline...")
    test_result = query_company_policy.invoke({"topic": "What is the policy for VIP hardware damage?"})
    print("\n" + test_result)