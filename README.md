# Локальный чат-бот с Retrieval-Augmented Generation (RAG)  
# Local Retrieval-Augmented Generation (RAG) Chatbot

Локальный чат-бот с поиском по смыслу по вашим документам. Работает полностью офлайн.

A fully offline chatbot with semantic search over your documents.

## Особенности / Features

| Русский | English |
|---------|---------|
| Поиск по смыслу, а не по точным словам (векторная база) | Semantic search instead of exact keyword matching (vector database) |
| 100 % офлайн | 100 % offline |
| Показывает источники каждого ответа | Shows sources for every answer |
| Streaming-ответы в реальном времени | Real-time streaming responses |
| Работает с любой моделью через Ollama (Llama 3.1, Llama 3.2, Phi-3, Gemma 2 и др.) | Works with any model via Ollama (Llama 3.1, Llama 3.2, Phi-3, Gemma 2, etc.) |

## Требования / Requirements

- Python 3.9+
- Ollama (running on `localhost:11434`)

## Установка и запуск / Installation & Usage

### 1. Скачиваем репозиторий / Clone the repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
