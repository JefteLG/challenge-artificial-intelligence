try:
    from lib_helpers.llm.llm import LLM
    from lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from lib_helpers.decorators.templates_ import OutOfScopeTemplate, ContextOutOfScopeTemplate, AuroraInfoOutOfScopeTemplate, GreetOutOfScopeTemplate, ExampleOutOfScopeTemplate
    from lib_helpers.example_loader.example_loader import ExampleLoader
    from lib_helpers.lib_utils.custom_exception import OutOfScopeException
    from lib_helpers.decorators.examples.out_of_scope_examples import OutOfScopeExamples

except ModuleNotFoundError:
    from src.lib_helpers.llm.llm import LLM
    from src.lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from src.lib_helpers.decorators.templates_ import OutOfScopeTemplate, ContextOutOfScopeTemplate, AuroraInfoOutOfScopeTemplate, GreetOutOfScopeTemplate, ExampleOutOfScopeTemplate
    from src.lib_helpers.example_loader.example_loader import ExampleLoader
    from src.lib_helpers.lib_utils.custom_exception import OutOfScopeException
    from src.lib_helpers.decorators.examples.out_of_scope_examples import OutOfScopeExamples

def check_out_of_scope(llm_instance: LLM, history: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Access the first argument if args is not empty
            _input = args[0] if args else kwargs.get('input')
            out_of_scope = is_out_of_scope(llm_instance, _input, history)
            if out_of_scope["rsp"]:
                raise OutOfScopeException("The user input is Out of Scope")
            return func(
                info = out_of_scope.get("info", "no_bot_info"),
                greet = out_of_scope.get("saudacao", False),
                exemplo_explicacao = out_of_scope.get("exemplo_explicacao", False),
                *args,
                **kwargs)

        return wrapper
    return decorator


def is_out_of_scope(llm_instance: LLM, _input: str, history: str) -> bool:
    out_of_scope_examples = OutOfScopeExamples()
    example_loader = ExampleLoader(get_embedder())
    positive_out_of_scope_examples = example_loader.relevant_examples_as_md(out_of_scope_examples.is_out_of_scope, _input, 8,
        kwargs={
            "new_columns":{"fora de escopo":True},
            "rename_columns":{"doc":"entrada"},
            "select_columns":["entrada", "fora de escopo"],
            "assign_random_on_missmatch":True
        }
    )
    negative_out_of_scope_examples = example_loader.relevant_examples_as_md(out_of_scope_examples.is_not_out_of_scope, _input, 8, 
        kwargs={
            "new_columns":{"fora de escopo":False},
            "rename_columns":{"doc":"entrada"},
            "select_columns":["entrada", "fora de escopo"],
            "assign_random_on_missmatch":True
        }
    )
    output_schema = {
        "type": "object",
        "properties": {
            "out_of_scope": {"type": "boolean"},
            "saudacao": {"type": "boolean"},
            "exemplo_explicacao": {"type": "boolean"},
            "sobre_exemplo": {"type": "boolean"},
            "mensagem": {"type": "string"}
        },
        "additionalProperties": False
    }
    kwargs = {
        'input':_input,
        'positive_out_of_scope_examples': positive_out_of_scope_examples,
        'negative_out_of_scope_examples': negative_out_of_scope_examples,
        'static_output_examples': out_of_scope_examples.static_output_examples,
        'history_text':history
    }
    ## Verifica se o usuario perguntou sobre o bot.
    response = llm_instance.run(
        AuroraInfoOutOfScopeTemplate.SYSTEM_PROMPT_TEMPLATE,
        AuroraInfoOutOfScopeTemplate.HUMAN_PROMPT_TEMPLATE,
        kwargs,
        output_schema
    )
    if not response["out_of_scope"]:
        return {"rsp": False, "info": "bot_info"}

    ## Verificar se o usuario fez uma saudação ou despedida.
    response = llm_instance.run(
        GreetOutOfScopeTemplate.SYSTEM_PROMPT_TEMPLATE,
        GreetOutOfScopeTemplate.HUMAN_PROMPT_TEMPLATE,
        kwargs,
        output_schema
    )
    if response["saudacao"]:
        return {"rsp": False, "saudacao": response["saudacao"]}

    ## Verifica se o usuario deseja um exemplo
    response = llm_instance.run(
        ExampleOutOfScopeTemplate.SYSTEM_PROMPT_TEMPLATE,
        ExampleOutOfScopeTemplate.HUMAN_PROMPT_TEMPLATE,
        kwargs,
        output_schema
    )
    if response["exemplo_explicacao"]:
        return {"rsp": False, "exemplo_explicacao": response["exemplo_explicacao"]}

    # response = llm_instance.run(
    #     OutOfScopeTemplate.SYSTEM_PROMPT_TEMPLATE,
    #     OutOfScopeTemplate.HUMAN_PROMPT_TEMPLATE,
    #     kwargs,
    #     output_schema
    # )
    # response = {"rsp": response["out_of_scope"], "info": "no_bot_info"}
    # if response["rsp"]:
    #     kwargs['history']=history
    #     response = llm_instance.run(
    #         ContextOutOfScopeTemplate.SYSTEM_PROMPT_TEMPLATE,
    #         ContextOutOfScopeTemplate.HUMAN_PROMPT_TEMPLATE,
    #         kwargs,
    #         output_schema
    #     )
    #     response = {"rsp": response["out_of_scope"], "info": "no_bot_info"}

    return {"rsp": False, "info": "no_bot_info"}


def get_embedder() -> AdaEmbedder:
    return AdaEmbedder()