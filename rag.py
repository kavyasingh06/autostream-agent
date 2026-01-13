import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 

def load_rag():
   
    if not os.path.exists("data/knowledge.md"):
        
        os.makedirs("data", exist_ok=True)
        with open("data/knowledge.md", "w") as f:
            f.write("# Pricing\nBasic Plan: $29/mo (720p)\nPro Plan: $79/mo (4K, AI Captions)")

    loader = TextLoader("data/knowledge.md")
    docs = loader.load()

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    return db