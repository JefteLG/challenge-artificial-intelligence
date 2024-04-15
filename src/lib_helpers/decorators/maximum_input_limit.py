try:
    from lib_helpers.lib_utils.token_controller import TokenController
    from lib_helpers.lib_utils.custom_exception import MaximumInputLimitException
except ModuleNotFoundError:
    from src.lib_helpers.lib_utils.token_controller import TokenController
    from src.lib_helpers.lib_utils.custom_exception import MaximumInputLimitException

def check_maximum_input_limit():
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Access the first argument if args is not empty
            _input = args[0] if args else kwargs.get('input')
            token_count = TokenController().count_tokens(_input)
            if token_count > 70:
                raise MaximumInputLimitException(f'The user input is too long. TOKEN: {token_count}.')
            return func(*args, **kwargs)
        return wrapper
    return decorator
