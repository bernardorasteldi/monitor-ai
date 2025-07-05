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


## 🧪 Etapas do Teste

### 🟣 1. Enviar um PDF para o Agente 1

#### 📌 Usando curl (no terminal):

```bash
curl -X POST "http://localhost:8001/upload/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/para/arquivo.pdf"
```

> Substitua `/caminho/para/arquivo.pdf` pelo caminho real do seu arquivo (ex: `/home/bernardorasteldi/Downloads/rede.pdf`)

#### ✅ Resposta esperada:

```json
{
  "message": "Arquivo processado",
  "chunks": 12
}
```

---

### 🟡 2. Fazer uma pergunta para o Agente 2

#### 📌 Usando o navegador:

Acesse:

```
http://localhost:8002/perguntar/?pergunta=O%20que%20é%20uma%20rede%20de%20computadores
```

#### 📌 Ou usando curl:

```bash
curl "http://localhost:8002/perguntar/?pergunta=O que é uma rede de computadores?"
```

#### ✅ Resposta esperada (exemplo):

```json
{
  "resposta": "Pergunta: O que é uma rede de computadores? Resposta: Uma rede de computadores é um conjunto..."
}
```

---

### 🧪 Se quiser testar passo a passo pelo Postman

1. Crie uma requisição `POST` para:

```
http://localhost:8001/upload/
```

2. Na aba **Body > form-data**, adicione o campo:

- **Key:** `file` (tipo **File**)  
- **Value:** selecione um PDF com conteúdo relevante

3. Faça uma requisição `GET` para:

```
http://localhost:8002/perguntar/?pergunta=sua-pergunta
```
### Validação do Problema

1. Relevância do Problema

No ambiente acadêmico, alunos frequentemente se deparam com dúvidas pontuais sobre conteúdos de disciplinas, especialmente ao estudar de forma autônoma fora do horário das aulas, caso muito comum em cursos a distância, onde o acesso a tutores, monitores ou mesmo ao professor é mais restrito. Essas dúvidas incluem:

- Conceitos técnicos vistos em aula;

- Interpretação de trechos de slides, textos ou PDFs;

- Aplicações práticas de fórmulas, algoritmos ou teorias.

Apesar de haver materiais disponíveis, os alunos muitas vezes não sabem onde encontrar a resposta rapidamente ou têm dificuldades em interpretar textos técnicos isoladamente.

Nesses casos os alunos acabam dependento da disponibilidade do professor ou monitor para tirar dúvidas — o que nem sempre ocorre de forma imediata.

Essa lacuna entre disponibilidade da informação e acesso contextualizado e ágil ao conhecimento compromete o aprendizado, aumenta a frustração e dificulta a aprendizagem contínua, especialmente em disciplinas de alta complexidade.

2. O que o projeto resolve

O IA Monitor de Disciplina propõe uma solução baseada em agentes de inteligência artificial para automatizar o esclarecimento de dúvidas dos alunos, utilizando os próprios materiais da disciplina como base de conhecimento.

3. Como funciona:

O Agente 1 (Indexador) permite ao professor ou ao aluno fazer upload de PDFs da disciplina (como apostilas, slides ou artigos). O sistema extrai e organiza o conteúdo, criando uma base vetorial semântica.

O Agente 2 (Respondedor) interpreta a pergunta feita pelo aluno, consulta a base de conhecimento do Agente 1 e gera uma resposta relevante e contextualizada utilizando modelos de linguagem (Transformers).

4. Impactos esperados

Acesso imediato e inteligente a respostas, mesmo fora do horário de aula.

Redução da sobrecarga de professores e monitores em atendimentos repetitivos.

Aprendizado contínuo e autônomo por parte dos alunos.

Flexibilidade para uso em diferentes disciplinas e cursos, adaptando os materiais de entrada conforme necessário.

Foco no contéudo disinibilizado pelo professor, evitando busca em materiais não indicados ou foro do escopo da disciplina.