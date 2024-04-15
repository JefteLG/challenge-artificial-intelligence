import json
import traceback
from jsonschema.exceptions import ValidationError

try:
    import sys
    import os
    current_dir = os.path.dirname(__file__)
    src_dir = os.path.abspath(os.path.join(current_dir, './lib_helpers'))
    sys.path.append(src_dir)
    from lib_helpers.llm.llm import LLM
    from lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from lib_helpers.lib_utils.event_handler import EventHandler
    from lib_answer_adaptive_learning.services.answer_adaptive_learning_service import AnswerAdaptiveLearningService
    from lib_helpers.lib_utils.custom_exception import InternalServerErrorException, JsonBodyValidationException, SchemaValidationException, PromptInjectionException, MaximumInputLimitException, LanguageNotSuportedException, LLMOutputParseException, LLMOutputSchemaValidationException, OutOfScopeException
    from conversation_history_db.management_db import ConversationHistory

except ModuleNotFoundError:
    from src.lib_helpers.lib_utils.event_handler import EventHandler
    from src.lib_helpers.llm.llm import LLM
    from src.lib_answer_adaptive_learning.services.answer_adaptive_learning_service import AnswerAdaptiveLearningService
    from src.lib_helpers.lib_utils.ada_embedder import AdaEmbedder
    from src.lib_helpers.lib_utils.custom_exception import InternalServerErrorException, JsonBodyValidationException, SchemaValidationException, PromptInjectionException, MaximumInputLimitException, LanguageNotSuportedException, LLMOutputParseException, LLMOutputSchemaValidationException, OutOfScopeException


def lambda_handler(event, context):
    try:
        schema = {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "minLength": 1,
                },
                "user_id": {
                    "type": "string",
                    "minLength": 1
                },
                "aurora_knowledge":{
                    "type": "string"
                },
                "gaps_knowledge":{
                    "type": "boolean"
                },
            },
            "required": ["input", "user_id", "aurora_knowledge"],
            "additionalProperties": False
        }

        llm = get_llm()
        embedder = get_embedder()
        body = get_event_handler().handle_event(event, schema)
        input = body.get("input")
        user_id = body.get("user_id")
        gaps_knowledge = body.get("gaps_knowledge", False)
        aurora_knowledge = body.get("aurora_knowledge")

    except json.JSONDecodeError:
        print("Invalid body/JSON format")
        return create_response(400, {"output":JsonBodyValidationException.ERROR_CODE})
    except ValidationError as e:
        print(f"Schema validation error: {e.message}")
        return create_response(400, {"output":SchemaValidationException.ERROR_CODE})
    except Exception as e:
        # Capture the traceback
        error_traceback = traceback.format_exc()
        print(f"Internal server error [{error_traceback}]")
        return create_response(500, {"output":f"{InternalServerErrorException.ERROR_CODE} - [{error_traceback}]"})

    try:
        conversation_history = ConversationHistory()
        conversation = conversation_history.buscar_conversa_por_id(user_id, gaps_knowledge)

        if gaps_knowledge:
            if conversation:
                response = get_answer_adaptive_learning_service(llm, input, embedder, gaps_knowledge, aurora_knowledge, conversation).gap_adaptive_learning()
            else:
                response = {"rsp": "0_0", "db": False}
        else:
            response = get_answer_adaptive_learning_service(llm, input, embedder, gaps_knowledge, aurora_knowledge, conversation).answer_adaptive_learning()
        
        response_body = {
            'output':response["rsp"],
            'usage':llm.get_estimated_cost()
        }
        result = create_response(200, response_body)
        print(result)

        if not gaps_knowledge and response["db"]:
            conversation_history.adicionar_pergunta_resposta(user_id, input, response)
        return result
    except PromptInjectionException as e:
        print(f"Error: {e}")
        return create_response(400, {"output":PromptInjectionException.ERROR_CODE})
    except MaximumInputLimitException as e:
        print(f"Error: {e}")
        return create_response(400, {"output":MaximumInputLimitException.ERROR_CODE})
    except LanguageNotSuportedException as e:
        print(f"Error: {e}")
        return create_response(400, {"output":LanguageNotSuportedException.ERROR_CODE})
    except LLMOutputParseException as e:
        print(f"Error: {e}")
        return create_response(500, {"output":LLMOutputParseException.ERROR_CODE})
    except LLMOutputSchemaValidationException as e:
        print(f"Error: {e}")
        return create_response(500, {"output":LLMOutputSchemaValidationException.ERROR_CODE})
    except OutOfScopeException as e:
        print(f"Error: {e}")
        return create_response(400, {"output":OutOfScopeException.ERROR_CODE})
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Internal server error [{error_traceback}]")
        return create_response(500, {"output":f"{InternalServerErrorException.ERROR_CODE} - [{error_traceback}]"})


def get_llm() -> LLM:
    return LLM()
        
def get_embedder() -> AdaEmbedder:
    return AdaEmbedder()

def get_event_handler() -> EventHandler:
    return EventHandler()

def create_response(status_code, data):
    response = {
        "status_code": status_code,
        "body": data
    }
    return response

def get_answer_adaptive_learning_service(llm: LLM, input: str, embedder: AdaEmbedder, gaps_knowledge: bool, aurora_knowledge: str, history: object = None):
    return AnswerAdaptiveLearningService(llm, input, embedder, gaps_knowledge, aurora_knowledge, history)