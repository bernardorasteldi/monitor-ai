# Visão Arquitetônica Final: Projeto IA Monitor de Disciplina com Medidas de Mitigação

---

## 1. Medidas de Mitigação Implementadas

Com base na análise inicial de riscos, as seguintes medidas foram incorporadas para aprimorar a segurança e a resiliência do sistema:

### 1.1 Isolamento de Rede para Agentes (Containerização)

* **Mitigação de Risco:** Exposição de Endpoints, Confidencialidade, Integridade (ataques internos).
* **Implementação:** O **Agente 1 (Indexador)** é executado em um container Docker, e sua configuração de rede é estritamente definida para permitir comunicação apenas com o host local (via `localhost`). Isso limita a superfície de ataque ao impedir que o agente seja acessível de outras máquinas na rede, a menos que explicitamente configurado.
* **Justificativa:** Ao confinar o Agente 1 a um ambiente de rede isolado, minimizamos o risco de acesso não autorizado externo. A comunicação entre os agentes, que ocorre via `localhost`, permanece segura dentro do ambiente de execução isolado.

### 1.2 Validação de Entrada de Dados

* **Mitigação de Risco:** Integridade dos Dados, Desempenho.
* **Implementação:**
    * No Agente 1, foi implementada a validação do tipo de arquivo enviado para o endpoint `/upload/`, aceitando exclusivamente arquivos PDF. Isso é feito utilizando as funcionalidades do **FastAPI** para validação de tipo de mídia.
    * No Agente 2, a validação de entrada para as perguntas garante que apenas dados de texto sejam processados, evitando entradas malformadas que poderiam comprometer o modelo de IA ou a lógica de busca.
* **Justificativa:** A validação rigorosa de entrada garante que o sistema processe apenas dados esperados e válidos, prevenindo potenciais ataques de injeção e melhorando a estabilidade geral do sistema. Isso também contribui para um desempenho mais previsível, uma vez que o sistema não desperdiça recursos tentando processar dados inválidos.

### 1.3 Utilização de Bibliotecas Consolidadas e Open Source

* **Mitigação de Risco:** Vulnerabilidades de Software, Desempenho, Disponibilidade.
* **Implementação:** O projeto utiliza amplamente bibliotecas de código aberto e bem estabelecidas na comunidade de IA e desenvolvimento web, como **FastAPI, PyMuPDF, SentenceTransformers, FAISS, Transformers** e **PyTorch**.
* **Justificativa:** A adoção de bibliotecas populares e com histórico comprovado de manutenção e segurança reduz significativamente o risco de vulnerabilidades desconhecidas. A vasta comunidade de desenvolvedores por trás dessas bibliotecas garante que patches de segurança e melhorias de desempenho sejam lançados regularmente, contribuindo para a robustez e a segurança contínua do sistema.

### 1.4 Separação de Responsabilidades e Dependências

* **Mitigação de Risco:** Disponibilidade, Segurança (princípio do menor privilégio).
* **Implementação:** Cada agente é um microserviço com responsabilidades bem definidas e dependências controladas. O Agente 2 tem sua única dependência externa sendo o Agente 1, acessado via HTTP.
* **Justificativa:** A arquitetura de microserviços intrinsecamente melhora a resiliência. Uma falha em um agente não necessariamente derruba o sistema inteiro, pois as responsabilidades são segregadas. Além disso, a separação clara de responsabilidades contribui para o princípio do menor privilégio, onde cada componente tem acesso apenas aos recursos de que necessita, reduzindo a superfície de ataque.

---

## 2. Aprimoramentos Futuros (Considerações para um Ambiente de Produção)

Embora as medidas acima melhorem significativamente a segurança para o contexto do projeto, em um ambiente de produção com exposição pública, seriam consideradas as seguintes melhorias:

* **Autenticação e Autorização:** Implementação de tokens de autenticação (e.g., JWT) para todas as chamadas de API, garantindo que apenas clientes e agentes autorizados possam interagir com o sistema.
* **Monitoramento e Logs:** Ferramentas de monitoramento para detectar atividades incomuns, erros e gargalos de desempenho, além de um sistema de logging centralizado para rastreamento de eventos.
* **Gerenciamento de Segredos:** Armazenamento seguro de credenciais e chaves API (se houver) utilizando ferramentas como HashiCorp Vault ou AWS Secrets Manager.
* **Hardening de Containers:** Otimização adicional da imagem Docker do Agente 1 para reduzir a superfície de ataque, removendo ferramentas desnecessárias e rodando com um usuário não-root.
* **Redundância e Balanceamento de Carga:** Para alta disponibilidade e escalabilidade, a implementação de múltiplos instâncias de cada agente atrás de um balanceador de carga.

---

## 3. Conclusão

A arquitetura final do "IA Monitor de Disciplina" demonstra uma evolução consciente das preocupações de segurança desde a concepção inicial. As medidas implementadas, como isolamento de rede, validação de entrada e o uso de bibliotecas robustas, contribuem para um sistema mais seguro e confiável, atendendo aos requisitos de sistemas distribuídos e de segurança propostos pelo trabalho. O design modular facilita ainda futuras expansões e a incorporação de práticas de segurança mais avançadas, caso o sistema seja escalado para um ambiente de produção.