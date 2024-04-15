class LLMOutputSchemaValidationException(Exception):
    ERROR_CODE = "LLM_OUTPUT_SCHEMA_VALIDATION_ERROR"
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LLMOutputParseException(Exception):
    ERROR_CODE = "LLM_OUTPUT_PARSE_ERROR"
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
