from typing import Callable, TypeVar, Generic

from cli_veripy.type_validation import validate_type

T = TypeVar("T")
class CLIArgument(Generic[T]):
    def __init__(self, type_name:str, _type:type[T] = bool,
    description:str|None = None, long_description:str|None = None,
    validation_function:Callable[[str], bool] = lambda a:True,
    fail_validation_callback_msg:Callable[[str|int, str, str], str] = 
        lambda key, arg, type_name: f"Invalid value '{arg}' for argument '{key}'.  '{key}' must be a valid {type_name}."
    ):
        self.type = _type
        self.type_name = type_name
        self.validation_function = validation_function
        self.fail_validation_callback_msg = fail_validation_callback_msg
        self.description = description
        self.long_description = long_description

    def __hash__(self):
        return hash(self.type_name)
    
    def __len__(self):
        return len(self.type_name)

    def __eq__(self, value):
        return self.type_name == value
    
    def __call__(self, key:str|int, arg:str) -> T:
        return validate_type(self, arg, key)
        
    @property
    def __doc__(self):
        return (self.description if self.description else "") + (f"\n\n{self.long_description}" if self.long_description else "")
    
    def __str__(self):
        return self.type_name

    @property
    def full_description(self):
        return self.__doc__
