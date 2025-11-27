import os
import argparse
from vector_db import create_db_from_html, get_retriever, CHROMA_PATH
from llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = """
Ты — полезный ассистент, который отвечает только на основе предоставленного контекста.
Если в контексте нет ответа — скажи, что не знаешь.

Контекст:
{context}

Вопрос: {question}

Ответь максимально точно и по-русски.
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true", help="Пересоздать базу")
    args = parser.parse_args()

    # Пересоздаём БД при необходимости
    if args.build or not os.path.exists(CHROMA_PATH):
        print("Создаём/пересоздаём векторную базу...")
        create_db_from_html("datasets")
    else:
        print("Используем существующую базу.")

    # Инициализируем компоненты
    retriever = get_retriever(k=10)
    llm = get_llm(model="llama3.1:8b")  # или другая модель
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    print("\nГотово! Задавай вопросы (или напиши 'exit')\n")

    while True:
        query = input("\nТы: ").strip()
        if query.lower() in {"exit", "quit", "выход"}:
            print("Пока!")
            break

        print("Ищем в базе...")
        docs = retriever.invoke(query)
        print(f"\n[DEBUG] Найдено {len(docs)} релевантных фрагментов. Источники:")
        for i, doc in enumerate(docs[:3]):  # показываем первые 3
            source = doc.metadata["source"].split("/")[-1]
            print(f"  {i+1}. {source}")
        print("-" * 50)

        if not docs:
            print("Бот: Ничего не нашёл в базе.")
            continue
        context = "\n\n---\n\n".join([doc.page_content for doc in docs])

        print("Думаю...", end="", flush=True)
        chain = prompt | llm

        for chunk in chain.stream({"context": context, "question": query}):
            print(chunk.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    main()