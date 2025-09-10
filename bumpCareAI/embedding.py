import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_faiss_from_txt(file_path, db_path="txt_faiss_index"):
    # Load the .txt file as documents
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    if not documents:
        raise ValueError("No content found in the TXT file!")

    print(f" Loaded {len(documents)} document(s) from {file_path}")

    # Create embeddings (use CPU if GPU fails)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}   # force CPU (fix CUDA errors)
    )

    # Create FAISS index
    vectorstore = FAISS.from_documents(documents, embeddings)

    #Save FAISS locally
    vectorstore.save_local(db_path)
    print(f" FAISS index saved at: {db_path}")

    return vectorstore


if __name__ == "__main__":
    # Change this to your ICD/SNOMED .txt file path
    file_path = "Your path here"
    
    db_path = "Your path here"

    # Build FAISS
    build_faiss_from_txt(file_path, db_path)
