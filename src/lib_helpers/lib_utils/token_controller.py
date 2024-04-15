import os
import tiktoken

class TokenController:
    def __init__(self) -> None:
        self.encoder = tiktoken.encoding_for_model(os.environ.get('MODEL_NAME_OPENAI'))

    def encode(self):
        raise NotImplementedError()
    
    def raise_for_special_token(self, input: str) -> None:
        """
        raises a value error if a special token is encountered.
        This can be modified to add more special tokens
        >>> encoder.special_tokens_set
        {'<|endofprompt|>',
        '<|endoftext|>',
        '<|fim_middle|>',
        '<|fim_prefix|>',
        '<|fim_suffix|>'}
        """
        self.encoder.encode(input)
            
    def encode_ordinary(self, input: str) -> list[int]:
        return self.encoder.encode_ordinary(input)

    def decode(self, tokens: list[int]) -> str:
        return self.encoder.decode(tokens)
    
    def count_tokens(self, input: str) -> int:
        return len(self.encode_ordinary(input))