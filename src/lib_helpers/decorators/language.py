from enum import Enum

try:
    from lib_helpers.llm.llm import LLM
    from lib_helpers.decorators.templates_ import LanguageTemplate
    from lib_helpers.lib_utils.custom_exception import LanguageNotSuportedException
    from lib_helpers.lib_utils.token_controller import TokenController

except ModuleNotFoundError:
    from src.lib_helpers.llm.llm import LLM
    from src.lib_helpers.decorators.templates_ import LanguageTemplate
    from src.lib_helpers.lib_utils.custom_exception import LanguageNotSuportedException
    from src.lib_helpers.lib_utils.token_controller import TokenController


class AllowedLanguages(Enum):
    PORTUGUESE = 'pt'

def check_language(llm_instance: LLM):
    def decorator(func):
        def wrapper(*args, **kwargs):
            _input = args[0] if args else kwargs.get('input')
            
            # Determine if the language verification is needed based on token count
            valid_language = True
            token_count = TokenController().count_tokens(_input)
            if token_count > 3:
                language, valid_language = verify_language(llm_instance, _input)
                if not valid_language:
                    raise LanguageNotSuportedException(f"Language [{language}] detected is not supported.")

            # Proceed with the original function if the language is valid
            if valid_language:
                return func(*args, **kwargs)

        return wrapper
    return decorator

def verify_language(llm_instance: LLM, _input: str) -> bool:
    output_schema = {
        "type": "object",
        "properties": {
            "language": {"type": ["string", "null"]}
        },
        "required": ["language"],
        "additionalProperties": False
    }
    kwargs = {
        'input':_input
    }
    response = llm_instance.run(
        LanguageTemplate.SYSTEM_PROMPT_TEMPLATE,
        LanguageTemplate.HUMAN_PROMPT_TEMPLATE,
        kwargs,
        output_schema)
    language = response['language']
    if language is None:
        return None, False
    
    return language, language in (lang.value for lang in AllowedLanguages)