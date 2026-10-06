# Avaliação de qualidade

Crie um conjunto versionado com descrições reais anonimizadas, categoria esperada, casos ambíguos e tentativas de prompt injection. Meça acurácia global e por categoria, taxa de fallback `other`, respostas inválidas, uso de tools, latência e custo por item.

Compare a versão agentic com uma baseline direta (`prompt -> structured output`). Isso torna a decisão de usar MCP/agent mensurável: se a taxa de acerto e capacidade de atualização não compensarem latência/custo adicionais, simplifique o caminho.
