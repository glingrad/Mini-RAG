Локальный чат-бот с Retrieval-Augmented Generation (RAG).

### Особенности
- Поиск по смыслу, а не по точным словам. (Vector database)
- 100 % офлайн 
- Показывает источника каждого ответа  
- Streaming-ответы в реальном времени  ф
- Работает с любой моделью через Ollama (Llama 3.1, Llama 3.2, Phi-3, Gemma2 и др.)

### Требования
- Python 3.9+
- Ollama (запущен на localhost:11434)

# 1. Скачиваем репозиторий

# 2. Устанавливаем зависимости
pip install -r requirements.txt

# 3. Скачиваем модели (один раз)
ollama pull nomic-embed-text:latest
ollama pull llama3.2:3b        # или llama3.1:8b, phi3:3.8b и т.д.

# 4. Первый запуск — создаём векторную базу
python main.py --build

# 5. Готово! Задаём вопросы
python main.py

