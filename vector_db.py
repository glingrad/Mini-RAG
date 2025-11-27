# vector_db.py
import os
import shutil
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from bs4 import BeautifulSoup
from typing import List

CHROMA_PATH = "chroma_db_store"
EMBEDDING_MODEL = "nomic-embed-text:latest"


def get_embedding_function():
    return OllamaEmbeddings(model=EMBEDDING_MODEL)


def load_html_documents(dataset_path: str) -> List[Document]:
    docs = []
    path = Path(dataset_path)

    if not path.exists():
        raise FileNotFoundError(f"Папка не найдена: {dataset_path}")

    for html_file in path.rglob("*.html"):
        text = None
        for encoding in ["utf-8", "cp1251", "latin-1"]:
            try:
                with open(html_file, "r", encoding=encoding) as f:
                    soup = BeautifulSoup(f, "html.parser")
                    text = soup.get_text(separator="\n")
                break
            except UnicodeDecodeError:
                continue

        if not text or not text.strip():
            continue

        clean_lines = [
            line.strip() 
            for line in text.splitlines() 
                if line.strip()
        ]
        clean_text = "\n".join(clean_lines)

        docs.append(Document(
            page_content=clean_text,
            metadata={"source": str(html_file)}
        ))

    return docs


def create_db_from_html(dataset_path: str = "datasets"):
    documents = load_html_documents(dataset_path)
    
    if not documents:
        print("Нет загруженных документов! Проверьте папку datasets/")
        return

    print(f"Загружено документов: {len(documents)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    chunks = splitter.split_documents(documents)
    print(f"Создано чанков: {len(chunks)}")

    if os.makedirs(CHROMA_PATH, exist_ok=True):
        shutil.rmtree(CHROMA_PATH, ignore_errors=True)

    print("Создаём векторную базу (это может занять время)...")
    Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding_function(),
        persist_directory=CHROMA_PATH
    )
    print(f"База сохранена в {CHROMA_PATH}")


def get_retriever(k: int = 10):
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )
    return db.as_retriever(search_kwargs={"k": k})