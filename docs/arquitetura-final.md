# Arquitetura Final com Medidas de Segurança

## Mudanças após análise

- Isolamento de rede entre os agentes
- Utilização de token de autenticação simples (a implementar)
- Validação de arquivos enviados (PDF)

## Medidas implementadas

- Agente 1 rodando em container com rede limitada
- Agente 2 separado, com dependência apenas via HTTP
- Uso de bibliotecas consolidadas e open source
