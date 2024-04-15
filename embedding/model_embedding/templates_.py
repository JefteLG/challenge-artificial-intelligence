class DataExtractionTemplate:
    SYSTEM_PROMPT_TEMPLATE = """
Extraia as informações importantes para responder às dúvidas sobre o assunto abordado no texto fornecido e crie um texto utilizando a mesma pessoa na escrita. Evite o uso de tópicos e concentre-se em elaborar um texto coeso e informativo com base nas informações apresentadas.

Saída: por favor, retorne um texto estruturado em parágrafos.
"""

    HUMAN_PROMPT_TEMPLATE = """
Extraia as informações relevantes para responder às dúvidas sobre o assunto mencionado no texto abaixo e elabore um texto utilizando a mesma pessoa na escrita. Evite o uso de tópicos e concentre-se em criar um texto coeso e informativo:

Texto:
{context}

---

Saída: por favor, retorne um texto estruturado em parágrafos.
"""

class DataExtractionJsonTemplate:
    SYSTEM_PROMPT_TEMPLATE = """
Organize os textos numerando as questões, perguntas e respostas, inserindo uma quebra de linha para cada pergunta diferente. Apenas organize o texto e remova as tags HTML, se não forem necessárias.

Exemplo de saída:
'Questão 1: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n
Questão 2: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n
Questão 3: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n
Questão 4: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n
Questão 5: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n'

Saída: Por favor, retorne um texto organizando as questões, perguntas e respostas numeradas.
"""

    HUMAN_PROMPT_TEMPLATE = """
Organize os textos numerando as questões, perguntas e respostas, inserindo uma quebra de linha para cada pergunta diferente. Apenas organize o texto e remova as tags HTML, se não forem necessárias.

Questões:
{context}

---

Exemplo de saída:
'Questão 1: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n
Questão 2: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n
Questão 3: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n
Questão 4: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n
Questão 5: Pergunta. Resposta: Resposta. Explicação: feedback.\n\n'

Saída: Por favor, retorne um texto organizando as questões, perguntas e respostas numeradas.
"""
