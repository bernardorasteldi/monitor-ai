# IA Monitor de Disciplina

Este projeto é um sistema distribuído composto por múltiplos agentes de Inteligência Artificial. O objetivo é permitir que alunos enviem materiais de uma disciplina e recebam respostas automáticas para dúvidas relacionadas.

## 💡 Visão Geral

- **Agente 1 (Indexador):** recebe PDFs, extrai texto, gera vetores e fornece contexto para perguntas.
- **Agente 2 (Respondedor):** recebe a pergunta do usuário, busca contexto e gera a resposta com um modelo de linguagem.

## 🧱 Tecnologias Utilizadas

- FastAPI
- Transformers (HuggingFace)
- FAISS
- SentenceTransformers
- PyMuPDF
- Docker (para o Agente 1)

## 🚀 Como Rodar

### Agente 1 (Indexador - via Docker)

```bash
cd agente1-indexador
docker build -t agente1-indexador .
docker run -d -p 8001:8001 agente1-indexador

cd agente2-respondedor
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app:app --reload --port 8002
```

## 🚀 Endpoints

Upload do PDF

POST /upload/ (localhost:8001)

Buscar Contexto

GET /buscar-contexto/?pergunta=... (localhost:8001)

Perguntar

GET /perguntar/?pergunta=... (localhost:8002)
