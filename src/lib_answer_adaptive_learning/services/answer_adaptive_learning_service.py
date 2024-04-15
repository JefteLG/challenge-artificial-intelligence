try:
    import sys
    import os
    current_dir = os.path.dirname(__file__)
    src_dir = os.path.abspath(os.path.join(current_dir, '../../lib_helpers'))
    sys.path.append(src_dir)
    from lib_helpers.llm.llm import LLM
    from lib_answer_adaptive_learning.answer_adaptive_learning import AnswerAdaptiveLearning
    from lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from lib_answer_adaptive_learning.services.templates_ import AnswerFAQTemplate, ShortAnswerFAQTemplate, GapAdaptiveTemplate, AffirmativeMaisEducaAnswerFAQTemplate, NegativeMaisEducaAnswerFAQTemplate, IntentClassifierAnswerFAQTemplate, HistoryMaisEducaAnswerFAQTemplate, BotInfoAnswerFAQTemplate, keywordAnswerFAQTemplate, GreetAnswerFAQTemplate, OnlyGreetAnswerFAQTemplate, ExampleAnswerFAQTemplate, HistoryContentMaisEducaAnswerFAQTemplate, AffirmativeAnswerFAQTemplate
    from lib_helpers.lib_utils.PineconeDBSearch import PineconeDBSearch
except ModuleNotFoundError:
    from src.lib_helpers.llm.llm import LLM
    from src.lib_answer_adaptive_learning.answer_adaptive_learning import AnswerAdaptiveLearning
    from src.lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from src.lib_answer_adaptive_learning.services.templates_ import AnswerFAQTemplate, ShortAnswerFAQTemplate, GapAdaptiveTemplate, AffirmativeMaisEducaAnswerFAQTemplate, NegativeMaisEducaAnswerFAQTemplate, IntentClassifierAnswerFAQTemplate, HistoryMaisEducaAnswerFAQTemplate, BotInfoAnswerFAQTemplate, keywordAnswerFAQTemplate, GreetAnswerFAQTemplate, OnlyGreetAnswerFAQTemplate, ExampleAnswerFAQTemplate, HistoryContentMaisEducaAnswerFAQTemplate, AffirmativeAnswerFAQTemplate

class AnswerAdaptiveLearningService(AnswerAdaptiveLearning):
    def __init__(self, llm: LLM, input: str, embedder: AdaEmbedder, gaps_knowledge: bool, aurora_knowledge: str, history_text: str = "Vazio") -> None:
        super().__init__(llm, input, embedder, gaps_knowledge, aurora_knowledge, history_text)
    
    def get_context(self, input_user) -> str:
        vector_store = PineconeDBSearch().pineconedbsearch("mais-educacao")
        embed = self.embedder.embed_query(input_user)
        index_search = vector_store.query(
            vector=embed,
            top_k=10 if self.history_text else 15,
            include_metadata=True
        )
        
        text_context = '\n\n'.join(f'- {item["metadata"]["text"]}' for item in index_search['matches'])
        return text_context
    
    def gap_adaptive_learning(self) -> str:
        kwargs = {
            'history_text': self.history_text if self.history_text else "Vazio"
        }

        response = self.llm.run(
            GapAdaptiveTemplate.SYSTEM_PROMPT_TEMPLATE,
            GapAdaptiveTemplate.HUMAN_PROMPT_TEMPLATE,
            kwargs,
            self.output_schema
        )

        return {"rsp": response['resposta_gpt'], "db": True}
    
    
    def mais_educa_pipe(self, kwargs, greet=False, exemplo_explicacao=False):
        
        response = self.llm.run(
                HistoryContentMaisEducaAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                HistoryContentMaisEducaAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                kwargs,
                self.output_schema
            )

        # Verifica se o usuario solicita um exemplo de explicação
        if exemplo_explicacao:
            response = self.llm.run(
                ExampleAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                ExampleAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                {"input": self.input},
                self.output_schema
            )
            print()
            if response['resposta_gpt'] == "afirmativo":
                response = self.llm.run(
                    HistoryContentMaisEducaAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                    HistoryContentMaisEducaAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                    kwargs,
                    self.output_schema
                )
            else:
                # Verifica se a pergunta do usuario está no contexto do +A Educação
                if self.history_text != "Vazio":
                    response = self.llm.run(
                        HistoryMaisEducaAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                        HistoryMaisEducaAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                        kwargs,
                        self.output_schema
                    )
                    print()
                    return {"rsp": response['resposta_gpt'], "db": True}
                else:
                    return {"rsp": "Não consigo criar exemplos personalizados neste momento, pois ainda não tivemos a oportunidade de conversar sobre nenhum assunto específico. Como não temos um histórico de conversas, não consigo elaborar exemplos direcionados para você. Estou à disposição para fornecer informações e orientações.", "db": False}

        # Classifica a resposta anterior em Afirmativo ou Negativo
        response = self.llm.run(
            IntentClassifierAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
            IntentClassifierAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
            {"context": response['resposta_gpt']},
            self.output_schema
        )

        # Pode retorna uma das duas respostas, uma para o cenario Afirmativo e outra para o Negativo
        if response['resposta_gpt'] == "afirmativo":
            response = self.llm.run(
                AffirmativeMaisEducaAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                AffirmativeMaisEducaAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                kwargs,
                self.output_schema
            )
            response = {"rsp": response['resposta_gpt'], "db": True}
        else:
            if greet:
                response = self.llm.run(
                    GreetAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                    GreetAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                    {"input": self.input},
                    self.output_schema
                )

                response = {"rsp": response['resposta_gpt'], "db": False}

                if  response.get('rsp')=='negativo':
                    response = self.llm.run(
                        OnlyGreetAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                        OnlyGreetAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                        {"input": self.input},
                        self.output_schema
                    )
                    return {"rsp": response['resposta_gpt'], "db": False}

            response = self.llm.run(
                NegativeMaisEducaAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                NegativeMaisEducaAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                {'input': self.input},
                self.output_schema
            )
            response = {"rsp": response['resposta_gpt'], "db": False}
        return response
    

    def aurora_pipe(self, kwargs, greet=False, exemplo_explicacao=False):
        response = self.llm.run(
                HistoryContentMaisEducaAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                HistoryContentMaisEducaAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                kwargs,
                self.output_schema
            )
        # Classifica a resposta anterior em Afirmativo ou Negativo
        response = self.llm.run(
            IntentClassifierAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
            IntentClassifierAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
            {"context": response['resposta_gpt']},
            self.output_schema
        )
        if response['resposta_gpt'] == "negativo":
            response = self.llm.run(
                    AnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                    AnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                    kwargs,
                    self.output_schema
                )
        # Verifica se o usuario solicita um exemplo de explicação
        if exemplo_explicacao:
            response = self.llm.run(
                ExampleAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                ExampleAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                {"input": self.input},
                self.output_schema
            )
            print()
            if response['resposta_gpt'] == "afirmativo":
                response = self.llm.run(
                    AnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                    AnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                    kwargs,
                    self.output_schema
                )
            else:
                # Verifica se a pergunta do usuario está no contexto do +A Educação
                if self.history_text != "Vazio":
                    response = self.llm.run(
                        HistoryMaisEducaAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                        HistoryMaisEducaAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                        kwargs,
                        self.output_schema
                    )
                    print()
                    return {"rsp": response['resposta_gpt'], "db": True}
                else:
                    return {"rsp": "Não consigo criar exemplos personalizados neste momento, pois ainda não tivemos a oportunidade de conversar sobre nenhum assunto específico. Como não temos um histórico de conversas, não consigo elaborar exemplos direcionados para você. Estou à disposição para fornecer informações e orientações.", "db": False}

        # Classifica a resposta anterior em Afirmativo ou Negativo
        response = self.llm.run(
            IntentClassifierAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
            IntentClassifierAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
            {"context": response['resposta_gpt']},
            self.output_schema
        )

        # Pode retorna uma das duas respostas, uma para o cenario Afirmativo e outra para o Negativo
        if response['resposta_gpt'] == "afirmativo":
            response = self.llm.run(
                AffirmativeAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                AffirmativeAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                kwargs,
                self.output_schema
            )
            response = {"rsp": response['resposta_gpt'], "db": True}
        else:
            if greet:
                response = self.llm.run(
                    GreetAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                    GreetAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                    {"input": self.input},
                    self.output_schema
                )

                response = {"rsp": response['resposta_gpt'], "db": False}

                if  response.get('rsp')=='negativo':
                    response = self.llm.run(
                        OnlyGreetAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                        OnlyGreetAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                        {"input": self.input},
                        self.output_schema
                    )
                    return {"rsp": response['resposta_gpt'], "db": False}

            response = self.llm.run(
                NegativeMaisEducaAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                NegativeMaisEducaAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                {'input': self.input},
                self.output_schema
            )
            response = {"rsp": response['resposta_gpt'], "db": False}
        return response

    

    def answer_adaptive_learning(self) -> str:
        # Info do assistente.
        if self.info == "bot_info":
            response = self.llm.run(
                BotInfoAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                BotInfoAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                {"input": self.input},
                self.output_schema
            )
            return {"rsp": response['resposta_gpt'], "db": False}
        
        response = self.llm.run(
                keywordAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
                keywordAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
                {"input": self.input},
                self.output_schema
            )
        
        context = self.get_context(input_user=response['resposta_gpt'])
        kwargs = {
            'context': context,
            'history_text': self.history_text if self.history_text else "Vazio",
            'input': self.input
        }           
        
            
        if self.aurora_knowledge == "mais_educa":
            response = self.mais_educa_pipe(kwargs, greet=self.greet, exemplo_explicacao=self.exemplo_explicacao)

        else: # aurora
            response = self.aurora_pipe(kwargs, greet=self.greet, exemplo_explicacao=self.exemplo_explicacao)
        
        return response

        # short_answer = self.llm.run(
        #     ShortAnswerFAQTemplate.SYSTEM_PROMPT_TEMPLATE,
        #     ShortAnswerFAQTemplate.HUMAN_PROMPT_TEMPLATE,
        #     {'input': self.input, 'context': response},
        #     self.output_schema
        # )

        # return response['resposta_gpt']

