from langchain_ollama import ChatOllama

def get_llm(model: str = "llama3.1:8b"):
    return ChatOllama(model=model, temperature=0.1)