class BackofficeEndpointException(Exception):
    ERROR_CODE = "BACKOFFICE_ENDPOINT_ERROR"
    def __init__(self, endpoint, error, request_body=None):
        self.endpoint = endpoint
        self.error = error
        self.request_body = request_body
        super().__init__(f'Backoffice exception at {endpoint} with error {error}; Request body: {request_body}')


class LanguageNotSuportedException(Exception):
    ERROR_CODE = "LANGUAGE_NOT_SUPPORTED_ERROR"
    def __init__(self, message="Language not supported"):
        self.message = message
        super().__init__(self.message)


class OutOfScopeException(Exception):
    ERROR_CODE = "OUT_OF_SCOPE_ERROR"
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PromptInjectionException(Exception):
    ERROR_CODE = "PROMPT_INJECTION_ERROR"
    def __init__(self, message="Prompt injection detected"):
        self.message = message
        super().__init__(self.message)


class MaximumInputLimitException(Exception):
    ERROR_CODE = "MAXIMUM_INPUT_LIMIT_ERROR"
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LLMOutputParseException(Exception):
    ERROR_CODE = "LLM_OUTPUT_PARSE_ERROR"
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LLMOutputSchemaValidationException(Exception):
    ERROR_CODE = "LLM_OUTPUT_SCHEMA_VALIDATION_ERROR"
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SchemaValidationException(Exception):
    ERROR_CODE = "SCHEMA_VALIDATION_ERROR"
    def __init__(self, message):
        super().__init__(message)


class JsonBodyValidationException(Exception):
    ERROR_CODE = "INVALID_BODY_JSON_ERROR"
    def __init__(self, message):
        super().__init__(message)


class InternalServerErrorException(Exception):
    ERROR_CODE = "INTERNAL_SERVER_ERROR"
    def __init__(self, message):
        super().__init__(message)