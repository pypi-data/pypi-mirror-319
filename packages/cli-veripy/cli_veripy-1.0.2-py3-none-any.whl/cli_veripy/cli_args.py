from __future__ import annotations
import sys
from pathlib import Path

class CLIError(Exception):
    def __init__(self, cli_arguments:CLIArguments, message:str, *args:list):
        self.args:list = args
        self.message:str = message
        self.cli_arguments:CLIArguments = cli_arguments
        super().__init__(self.message)

class ExistingPath(Path):
    pass

CLIArgumentTypes = float|int|str|bool|Path|ExistingPath

class CLIArguments:
    program_name:str = sys.argv[0]
    raw_arguments:list[str] = sys.argv[1::]

    def __init__(self,
    valid_flags:set[str]|None = None, valid_pargs:list[type[CLIArgumentTypes]]|None = None,
    valid_kwargs:dict[str,type[CLIArgumentTypes]|None]|None = None,
    required_kwargs:list[str]|None = None, usage_string:str|None = None,
    pargs_names:list[None|str]|None = None,
    minimum_pargs:int = -1,
    exit_on_invalid:bool = False
    ):
        try:
            self.required_kwargs:list[str]|None = required_kwargs if required_kwargs else []
            self.valid_flags:set[str]|None = valid_flags if valid_flags else set()
            self.valid_kwargs:dict[str,type[CLIArgumentTypes]|None]|None = valid_kwargs if valid_kwargs else {}
            self.valid_pargs:list[type[CLIArgumentTypes]]|None = valid_pargs if valid_pargs else []
            self.pargs_names:list[str]|None = pargs_names if pargs_names else []
            self.minimum_pargs:int = minimum_pargs
            self._usage_string:str|None = usage_string

            self.kwargs:dict[str, CLIArgumentTypes] = {k:None for k in self.valid_kwargs.keys()}
            self.pargs:list[CLIArgumentTypes] = []
            self.flags:set[str] = set()
            
            current_kw:str|None = None
            for arg in self.raw_arguments:
                if not arg.startswith("--") and arg.startswith("-"):
                    cleaned_arg = arg.removeprefix("-")
                    if cleaned_arg in self.valid_flags:
                        self.flags.add(cleaned_arg)
                        continue
                    else:
                        raise CLIError(self, f"Invalid flag provided '{cleaned_arg}'.", cleaned_arg)
                elif arg.startswith("--"):
                    cleaned_arg = arg.removeprefix("--")
                    if cleaned_arg in self.valid_kwargs:
                        current_kw = cleaned_arg
                        self.kwargs[current_kw] = None
                        continue
                    else:
                        raise CLIError(self, f"Invalid keyword provided '{cleaned_arg}'.", cleaned_arg)
                elif current_kw is not None and self.kwargs[current_kw] is None:
                    # Cast using the valid kwargs type dict
                    self.kwargs[current_kw] = self.validate_type(self.valid_kwargs, current_kw, arg)
                    continue
                elif len(self.pargs) < len(self.valid_pargs):
                    self.pargs.append(self.validate_type(self.valid_pargs, len(self.pargs), arg))
                    continue
                else:
                    raise CLIError(self, f"Unexpected argument '{arg}' provided without keyword.", arg)

            for k, v in self.kwargs.items():
                if v is None:
                    raise CLIError(self, f"Keyword argument {k} was not provided with a value.", k)
                
            for k in self.required_kwargs:
                if k not in self.kwargs:
                    raise CLIError(self, f"Required keyword argument {k} was not provided.")
                
            pargs_num = (len(self.valid_pargs) if self.minimum_pargs == -1 else self.minimum_pargs)
            if len(self.pargs) < pargs_num:
                raise CLIError(self, f"Expected {pargs_num} positional arguments recieved {len(self.pargs)} positional arguments.", len(self.valid_pargs) if self.minimum_pargs == -1 else self.minimum_pargs, len(self.pargs))
            
            while len(self.pargs) < pargs_num:
                self.pargs.append(None)
            
        except CLIError as e:
            if exit_on_invalid:
                sys.stderr.write('\n' + e.message + '\n')
                sys.stderr.write("\nusage: " + e.cli_arguments.usage_string + '\n\n')
                sys.stderr.flush()
                exit(1)
            else:
                raise e
        
    def validate_type(self, collection, argument_key:str|int, argument:str) -> CLIArgumentTypes:
        try:
            typ:type = collection[argument_key]
        except IndexError:
            raise CLIError(self, f"The program expects {len(collection)} arguments, {argument_key+1} were provided.", len(collection), argument_key+1, argument)
        
        if typ.__name__ in {"Path", "ExistingPath"}:
            try:
                if ((path:=ExistingPath(argument)).exists() if typ.__name__ == "ExistingPath" else (path:=Path(argument))):
                    return path
                else:
                    raise CLIError(self, f"Argument {argument_key} requires an existing file system path. The file path {argument!r} could not be found.")
            except TypeError:
                raise CLIError(self, f"Argument {argument_key} must be a valid Path type such as str. {argument} is not a valid Path type.", argument_key, argument)

        try:
            return typ(argument)
        except ValueError or TypeError:
            raise CLIError(self, f"Failed to convert {argument} to a {typ.__name__}.", argument, typ)
        


    @property
    def usage_string(self) -> str:
        if self._usage_string is not None:
            return self._usage_string
        required = "Required "
        empty_str = ""
        return self.program_name +\
            (' '*5 + empty_str.join([f' arg{i}({required if i < self.minimum_pargs else empty_str}{v.__name__})' for i, v in enumerate(self.valid_pargs)]) if len(self.valid_pargs) else '') +\
            (' '*5 + (f"(flags:[{', '.join([f'-{flag}' for flag in self.valid_flags])}])") if len(self.valid_flags) else empty_str) +\
            (' '*5 + f"(KeywordArguments:{{{', '.join([f'--{key}({required if key in self.required_kwargs else empty_str}{typ.__name__})' for key, typ in sorted(self.valid_kwargs.items(), key=lambda pair:pair[0] in self.required_kwargs)])}}})")

    @usage_string.setter
    def usage_string(self, value:str) -> str:
        if isinstance(value, str):
            self._usage_string = value
        raise TypeError(f"{value.__class__.__name__} is not a valid type for CLIArguments.usage_string.  CLIArguments.usage_string must be of type str.", type(value))

    def get_flag(self, key:str) -> bool:
        return key in self.flags
    
    def get_kwarg(self, key:str) -> CLIArgumentTypes:
        return self.kwargs[key]
    
    def get_parg(self, index:int) -> CLIArgumentTypes:
        return self.pargs[index]

    def __getitem__(self, key:str|int) -> CLIArgumentTypes:
        if isinstance(key, str):
            if flag_res:=(key in self.flags):
                return flag_res
            elif key in self.pargs_names:
                return self.pargs[self.pargs_names.index(key)]
            elif key in self.kwargs:
                return self.kwargs[key]
            elif is_flag:=(key in self.valid_flags):
                return False
            else:
                raise KeyError(f"'{key}' is not a valid key.", key)
        
        elif isinstance(key, int):
            try:
                return self.pargs[key]
            except IndexError:
                raise IndexError(f"Index {key} exceeds the number of positional arguments {len(self.pargs)}.", key, len(self.pargs))
        else:
            raise KeyError(f"{key.__class__.__name__} is not a valid key type.", type(key))
        
    def __setitem__(self, key:str|int, value):
        if isinstance(key, str):
            if key in self.pargs_names:
                parg_index = self.pargs_names.index(key)
                if isinstance(value, self.valid_pargs[parg_index]):
                    self.pargs[parg_index] = value
                else:
                    raise TypeError(f"'{key}' argument must be of {self.valid_pargs[parg_index].__name__} type.", key, self.valid_pargs[parg_index], type(value))
            elif key in self.valid_flags:
                if isinstance(value, bool):
                    if value:
                        self.flags.add(key)
                    else:
                        self.flags.remove(key)
                else:
                    raise TypeError(f"'{key}' is a flag and therefore must be of bool type.", key, bool, type(value))
            elif key in self.kwargs:
                if isinstance(value, self.valid_kwargs[key]):
                    self.kwargs[key] = value
                else:
                    raise TypeError(f"'{key}' keyword argument must be of {self.valid_kwargs[key].__name__} type.", key, self.valid_kwargs[key], type(value))
            else:
                raise KeyError(f"'{key}' is not a valid key.", key)
        
        elif isinstance(key, int):
            try:
                if isinstance(value, self.valid_pargs[key]):
                    self.pargs[key] = value
                else:
                    raise TypeError(f"'{key}' argument must be of {self.valid_pargs[key].__name__} type.", key, self.valid_pargs[key], type(value))
            except IndexError:
                raise IndexError(f"Index {key} exceeds the number of positional arguments {len(self.pargs)}.", key, len(self.pargs))
        else:
            raise KeyError(f"{key.__class__.__name__} is not a valid key type.", type(key))
