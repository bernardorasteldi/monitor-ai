# Visão Arquitetônica Inicial: Projeto IA Monitor de Disciplina

---

## 1. Componentes Principais

O sistema é concebido como uma arquitetura de microserviços, composta por dois agentes de Inteligência Artificial que operam de forma independente, comunicando-se via APIs REST.

### 1.1 Agente 1: Indexador de Conteúdo (Dockerizado)

* **Função Principal:** Processar arquivos PDF de material de disciplina para torná-los pesquisáveis e compreensíveis pelos modelos de IA.
* **Fluxo de Operação:**
    1.  Recebe um arquivo PDF via sua API REST (endpoint `/upload/`).
    2.  Utiliza **PyMuPDF** para extrair o texto completo do PDF.
    3.  Divide o texto extraído em partes menores, ou "chunks".
    4.  Gera **vetores semânticos (embeddings)** para cada chunk utilizando o modelo **all-MiniLM-L6-v2** da biblioteca **SentenceTransformers**.
    5.  Indexa esses vetores em uma base de dados **FAISS** para permitir buscas eficientes de contexto.
* **Tecnologias Utilizadas:** FastAPI (API), PyMuPDF, SentenceTransformers, FAISS, Docker (containerização).
* **Modelo de IA:** `all-MiniLM-L6-v2` (SentenceTransformers).

### 1.2 Agente 2: Respondedor de Perguntas (Execução Local)

* **Função Principal:** Receber perguntas dos usuários e gerar respostas inteligentes baseadas no contexto obtido do Agente 1.
* **Fluxo de Operação:**
    1.  Recebe uma pergunta do usuário via sua API REST (endpoint `/perguntar/`).
    2.  Envia a pergunta para o Agente 1 (via endpoint `/buscar-contexto/`) para obter os chunks de texto mais relevantes (contexto).
    3.  Alimenta o **modelo de linguagem natural (distilgpt2)** da biblioteca **Transformers** com a pergunta original do usuário e o contexto retornado pelo Agente 1.
    4.  Gera uma resposta textual em linguagem natural.
    5.  Retorna a resposta ao usuário.
* **Tecnologias Utilizadas:** FastAPI (API), Transformers, Requests (para comunicação com Agente 1), PyTorch (backend de execução do modelo).
* **Modelo de IA:** `distilgpt2` (Hugging Face - text-generation).

---

## 2. Comunicação Distribuída (A2A - Agent-to-Agent)

A comunicação entre os agentes é implementada utilizando o paradigma **HTTP REST**, com ambos os agentes expondo suas funcionalidades através de APIs desenvolvidas com **FastAPI**.

* **Padrão:** Agente 2 atua como cliente, fazendo requisições GET ao Agente 1 para consultar contextos relevantes.
* **Infraestrutura:** A comunicação ocorre via `localhost`, uma vez que o sistema está configurado para operar em um ambiente local isolado.

---

## 3. Fluxo de Interação

O sistema opera em um ciclo contínuo de indexação e consulta:

1.  **Upload de Conteúdo:** O usuário envia um arquivo PDF para o Agente 1 (Indexador) através de seu endpoint de upload.
2.  **Indexação:** O Agente 1 processa o PDF, extrai, vetoriza e indexa o conteúdo.
3.  **Consulta:** O usuário envia uma pergunta ao Agente 2 (Respondedor) através de seu endpoint de perguntas.
4.  **Busca de Contexto:** O Agente 2, por sua vez, realiza uma requisição ao Agente 1 para buscar os trechos de texto mais relevantes relacionados à pergunta.
5.  **Geração de Resposta:** Com o contexto em mãos, o Agente 2 utiliza seu modelo de IA para gerar uma resposta.
6.  **Retorno da Resposta:** A resposta é então enviada de volta ao usuário.

---

## 4. Potenciais Pontos de Risco (Pré-Mitigação)

Nesta fase inicial, os seguintes pontos são identificados como potenciais áreas de preocupação sem que ainda tenham sido aplicadas soluções de segurança:

* **Exposição de Endpoints:** Ambos os agentes expõem APIs REST. Embora localmente, uma exposição não intencional em ambiente de produção poderia permitir acesso não autorizado.
* **Integridade dos Dados:** Não há validação robusta de entrada para os arquivos PDF ou para as perguntas, o que poderia levar a comportamento inesperado do sistema ou até mesmo a ataques de injeção de dados (se os modelos de IA fossem suscetíveis).
* **Disponibilidade:** A dependência entre Agente 2 e Agente 1 significa que uma falha no Agente 1 (especialmente por ser containerizado e ter suas próprias dependências de execução) pode impactar a disponibilidade total do sistema.
* **Confidencialidade:** Não há mecanismos de autenticação ou autorização entre os agentes, assumindo uma comunicação "confiável" intrínseca ao ambiente local. Em um cenário distribuído real, isso seria um risco.
* **Privilégios:** O Agente 1, por ser containerizado, pode ter permissões de acesso ao sistema de arquivos hospedeiro que, se não restritas, poderiam ser exploradas.
* **Desempenho/Escalabilidade:** Para um volume muito grande de PDFs ou perguntas, os modelos de IA e a base FAISS poderiam se tornar gargalos, especialmente com recursos limitados.