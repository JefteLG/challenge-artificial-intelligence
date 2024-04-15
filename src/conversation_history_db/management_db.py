import os
from datetime import datetime, timezone
from pymongo import MongoClient


class ConversationHistory:
    def __init__(self):
        self.client = MongoClient(host=os.environ.get('MONGODB_URI'))
        self.db = self.client[os.environ.get('MONGODB_NAME_DB')]
        self.collection = self.db[os.environ.get('MONGODB_NAME_COLLECTION')]

    def buscar_conversa_por_id(self, user_id, gaps_knowledge):
        # Pega só as duas últimas perguntas e respostas de uma conversa existente
        conversa = self.collection.find_one({'user_id': user_id})
        if conversa:
            if gaps_knowledge:
                text_context = '\n\n'.join(
                    f'- Pergunta {numer+1}: {question["pergunta"]}' for numer, question in enumerate(conversa["perguntas_respostas"])
                )
            else:
                text_context = '\n\n'.join(
                    f'- Pergunta: {item["pergunta"]} Resposta GPT: {item["resposta_gpt"]["rsp"]}' for item in conversa["perguntas_respostas"][-2:]
                )
            return text_context
        else:
            return {}

    def adicionar_pergunta_resposta(self, user_id, pergunta, resposta_gpt):
        timestamp = datetime.now(timezone.utc).isoformat()
        nova_pergunta_resposta = {
            "pergunta": pergunta,
            "resposta_gpt": resposta_gpt,
            "timestamp": timestamp
        }
        conversa = self.collection.find_one({'user_id': user_id})
        if conversa:
            self.collection.update_one(
                {'user_id': user_id},
                {'$push': {'perguntas_respostas': nova_pergunta_resposta}}
            )
        else:
            self.collection.insert_one({
                'user_id': user_id,
                'perguntas_respostas': [nova_pergunta_resposta]
            })





# manager = ConversationHistory()
                
# manager.buscar_conversa_por_id("a7e78a2c-6de7-4ba1-be06-d9a039d78919", True)

# # Adicionando perguntas e respostas a uma conversa existente
# manager.adicionar_pergunta_resposta("123", "O que é um parágrafo em HTML?", "Um parágrafo HTML é uma unidade de texto...")
# manager.adicionar_pergunta_resposta(456, "Qual é a importância do CSS?", "O CSS é importante para o design web porque...")
# manager.adicionar_pergunta_resposta(456, "Como usar loops em Python?", "Em Python, você pode usar loops for e while para...")
# # Criando uma nova conversa com um novo ID de usuário
# manager.adicionar_pergunta_resposta(789, "O que é uma função em programação?", "Uma função em programação é um bloco de código...")
