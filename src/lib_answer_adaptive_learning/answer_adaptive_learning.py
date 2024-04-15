try:
    import sys
    import os
    import json
    current_dir = os.path.dirname(__file__)
    src_dir = os.path.abspath(os.path.join(current_dir, '../lib_helpers'))
    sys.path.append(src_dir)
    from lib_helpers.llm.llm import LLM
    from lib_helpers.decorators.language import check_language
    from lib_helpers.decorators.out_of_scope import check_out_of_scope
    from lib_helpers.decorators.prompt_injection import check_prompt_injection
    from lib_helpers.decorators.maximum_input_limit import check_maximum_input_limit
    from lib_helpers.lib_utils.ada_embedder import AdaEmbedder
except ModuleNotFoundError:
    from src.lib_helpers.llm.llm import LLM
    from src.lib_helpers.decorators.language import check_language
    from src.lib_helpers.decorators.out_of_scope import check_out_of_scope
    from src.lib_helpers.decorators.prompt_injection import check_prompt_injection
    from src.lib_helpers.decorators.maximum_input_limit import check_maximum_input_limit
    from src.lib_helpers.lib_utils.ada_embedder import AdaEmbedder

class AnswerAdaptiveLearning:
    def __init__(self, llm: LLM, input: str, embedder: AdaEmbedder, gaps_knowledge: bool, aurora_knowledge: str, history_text: str = "Vazio") -> None:
        self.llm = llm
        self.input = input
        self.embedder = embedder.embedder
        self.aurora_knowledge = aurora_knowledge
        self.history_text = history_text if history_text else "Vazio"
        self.info = "no_bot_info"
        self.greet = False
        self.exemplo_explicacao = False

        if gaps_knowledge:
            return True, input

        # Apply decorators;
        # Note: input is used through decorators
        @check_maximum_input_limit()
        # @check_language(self.llm)
        @check_prompt_injection(self.llm, self.history_text)
        @check_out_of_scope(self.llm, self.history_text)
        def validate_input(input, info="no_bot_info", greet=False, exemplo_explicacao=False):
            self.info = info
            self.greet = greet
            self.exemplo_explicacao = exemplo_explicacao
            return True, input

        validate_input(self.input)
    
    @property
    def output_schema(self):
        return {
            "type": "object",
            "properties": {
                "resposta_gpt": {"type": "string"}
            },
            "required": ["resposta_gpt"],
            "additionalProperties": False
        }