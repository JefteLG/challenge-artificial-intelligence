
from lib_helpers.lib_utils.token_controller import TokenController


try:
    from lib_helpers.llm.llm import LLM
    from lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from lib_helpers.example_loader.example_loader import ExampleLoader
    from lib_helpers.decorators.templates_ import PromptInjectionTemplate
    from lib_helpers.lib_utils.custom_exception import PromptInjectionException
    from lib_helpers.decorators.examples.prompt_injection_examples import PromptInjectionExamples
except ModuleNotFoundError:
    from src.lib_helpers.llm.llm import LLM
    from src.lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from src.lib_helpers.example_loader.example_loader import ExampleLoader
    from src.lib_helpers.decorators.templates_ import PromptInjectionTemplate
    from src.lib_helpers.lib_utils.custom_exception import PromptInjectionException
    from src.lib_helpers.decorators.examples.prompt_injection_examples import PromptInjectionExamples

def check_prompt_injection(llm_instance: LLM, history_text: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Access the first argument if args is not empty
            _input = args[0] if args else kwargs.get('input')
            try:
                TokenController().raise_for_special_token(_input)
            except ValueError:
                raise PromptInjectionException("Detected special token attempt.")
            if is_prompt_injection(llm_instance, _input, history_text):
                raise PromptInjectionException("Detected prompt injection attempt.")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def is_prompt_injection(llm_instance: LLM, _input: str, history_text: str) -> bool:
    prompt_injection_examples = PromptInjectionExamples()
    example_loader = ExampleLoader(get_embedder())
    positive_prompt_injection_examples = example_loader.relevant_examples_as_md(prompt_injection_examples.is_prompt_injection, _input, 15,
        kwargs={
            "new_columns":{"injeção de prompt":True},
            "rename_columns":{"doc":"entrada"},
            "select_columns":["entrada", "injeção de prompt"],
            "assign_random_on_missmatch":True
        }
    )
    negative_prompt_injection_examples = example_loader.relevant_examples_as_md(prompt_injection_examples.is_not_prompt_injection, _input, 15, 
        kwargs={
            "new_columns":{"injeção de prompt":False},
            "rename_columns":{"doc":"entrada"},
            "select_columns":["entrada", "injeção de prompt"],
            "assign_random_on_missmatch":True
        }
    )

    output_schema = {
        "type": "object",
        "properties": {
            "prompt_injection": {"type": "boolean"}
        },
        "required": ["prompt_injection"],
        "additionalProperties": False
    }

    kwargs = {
        'input':_input,
        'positive_prompt_injection_examples': positive_prompt_injection_examples,
        'negative_prompt_injection_examples': negative_prompt_injection_examples,
        'static_output_examples':prompt_injection_examples.static_output_examples,
        'history_text':history_text
    }

    response = llm_instance.run(
        PromptInjectionTemplate.SYSTEM_PROMPT_TEMPLATE,
        PromptInjectionTemplate.HUMAN_PROMPT_TEMPLATE,
        kwargs,
        output_schema
    )

    return response['prompt_injection']


def get_embedder() -> AdaEmbedder:
    return AdaEmbedder()