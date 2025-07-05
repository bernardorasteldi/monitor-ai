---
---

## 📁 `docs/arquitetura-inicial.md`

```markdown
# Arquitetura Inicial

## Componentes

- **Agente 1 (Indexador):** Recebe PDF → Extrai texto → Divide em partes → Gera vetores → Indexa em FAISS
- **Agente 2 (Respondedor):** Recebe pergunta → Consulta Agente 1 → Usa modelo GPT2 para gerar resposta

## Comunicação

- REST entre os agentes usando FastAPI
- Comunicação local via HTTP

## Riscos

- Falha no container do Agente 1
- Perguntas mal interpretadas por modelos pequenos
- Possível lentidão em máquinas com pouco recurso
```
