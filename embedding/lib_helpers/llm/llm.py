import os
import json
from jsonschema import validate
from langchain_community.callbacks import get_openai_callback
from jsonschema.exceptions import ValidationError
from langchain_community.chat_models import AzureChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

try:
    from lib_helpers.lib_utils.custom_exception import LLMOutputSchemaValidationException, LLMOutputParseException
except ModuleNotFoundError:
    from src.lib_helpers.lib_utils.custom_exception import LLMOutputSchemaValidationException, LLMOutputParseException

class Wrapper:
    def __init__(self, wrapped_class, debug = True):
        self.wrapped_class = wrapped_class
        self.debug = debug
        self.attr_list = []
        self.args_list = []
        self.kwargs_list = []
        self.result_list = []

    def __getattr__(self, attr):
        original_func = getattr(self.wrapped_class, attr)

        def wrapper(*args, **kwargs):
            result = original_func(*args, **kwargs)
            if self.debug:
                print(f"Start client Wrapper:")
                print(f"attr: [{attr}]")
                print(f"args: [{args}]")
                print(f"kwargs: [{kwargs}]")
                print(f"result: [{result}]")
            self.attr_list.append(attr)
            self.args_list.append(args)
            self.kwargs_list.append(kwargs)
            self.result_list.append(result)
            return result

        return wrapper

class LLM:

    def __init__(self, temperature = 0, model_kwargs={}) -> None:
        self.model = os.environ.get('MODEL_NAME_OPENAI')
        self.api_key_openai = os.environ.get('API_KEY_OPENAI')
        self.api_type_openai = os.environ.get('API_TYPE_OPENAI')
        self.api_base_openai = os.environ.get('API_BASE_OPENAI')
        self.api_version_openai = os.environ.get('API_VERSION_OPENAI')
        self.deployment_name_gpt = os.environ.get('DEPLOYMENT_NAME_GPT')
        self.temperature = temperature
        self.model_kwargs = model_kwargs
        self.llm_cost_tracker = self._start_estimated_cost()
        self.llm = self._get_llm()

    def _get_llm(self):
        llm = AzureChatOpenAI(
            model=self.model,
            deployment_name=self.deployment_name_gpt,
            openai_api_version=self.api_version_openai,
            openai_api_key=self.api_key_openai,
            openai_api_type=self.api_type_openai,
            openai_api_base=self.api_base_openai,
            temperature=self.temperature,
            model_kwargs=self.model_kwargs, 
        )
        llm.client = Wrapper(llm.client)
        return llm
     
    def _start_estimated_cost(self):
        return {
            'total_tokens': 0,
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'total_cost': 0,
            'prompts_sent': 0
        }
    
    def _set_estimated_cost(self, cb) -> None:
        self.llm_cost_tracker['total_tokens'] += cb.total_tokens
        self.llm_cost_tracker['prompt_tokens'] += cb.prompt_tokens
        self.llm_cost_tracker['completion_tokens'] += cb.completion_tokens
        self.llm_cost_tracker['total_cost'] += cb.total_cost
        self.llm_cost_tracker['prompts_sent'] += 1

    def get_estimated_cost(self) -> dict:
        return self.llm_cost_tracker
    
    def verify_response(self, response: dict) -> dict:
        """
        Iterates over the key-value pairs in the 'response' dictionary.

        For each key-value pair, checks if the value is a list.
        If the value is a list, replaces the value associated with the key by the first element of the list.

        Args:
            response (dict): The dictionary to be processed.

        Returns:
            dict: The modified dictionary with lists replaced by their first elements.
        """
        for key, value in response.items():
            if isinstance(value, list):
                response[key] = value[0]
        return response

    
    def parse_output(self, response, schema) -> dict:
        try:
            rsp = {"response": response.content}
            # rsp = {"response": response.content.replace('\n', '').replace('json', '').replace('`', '')}
            _response = self.verify_response(rsp)
            validate(instance=_response, schema=schema)
            return _response
        except json.JSONDecodeError as e:
            print(f"Error: {e}")
            raise LLMOutputParseException(f"LLM output could not be parsed to JSON: {e}")
        except ValidationError as e:
            print(f"Error: {e}")
            raise LLMOutputSchemaValidationException(f"LLM output schema validation failed: {e}")
        
    def run(self, system_message_template: str, human_message_template: str, kwargs: dict, output_schema: dict) -> dict:
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_template)
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template)

        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        with get_openai_callback() as cb:
            # Unpack kwargs dictionary as dynamic keyword arguments
            formatted_prompt = chat_prompt.format_prompt(**kwargs).to_messages()
            
            response = self.llm(formatted_prompt)
            self._set_estimated_cost(cb)
        return self.parse_output(response, output_schema)

