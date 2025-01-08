from __future__ import annotations
import os
import sys
from pathlib import Path
from cli_veripy.argument import CLIArgument

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
    program_path:Path = Path(sys.argv[0])
    raw_arguments:list[str] = sys.argv[1::]

    def __init__(self,
    valid_flags:set[str]|None = None, valid_pargs:list[type[CLIArgumentTypes]]|None = None,
    valid_kwargs:dict[str,type[CLIArgumentTypes]|None]|None = None,
    required_kwargs:list[str]|None = None, usage_string:str|None = None,
    pargs_names:list[None|str]|None = None,
    minimum_pargs:int = -1,
    exit_on_invalid:bool = False,
    description:str = "",
    help_menu:bool = False,
    help_prefix:str = "help:"
    ):
        try:
            self.required_kwargs:list[str]|None = required_kwargs if required_kwargs else []
            self.valid_flags:set[str]|None = valid_flags if valid_flags else set()
            self.valid_kwargs:dict[str,type[CLIArgumentTypes]|None]|None = valid_kwargs if valid_kwargs else {}
            self.valid_pargs:list[type[CLIArgumentTypes]]|None = valid_pargs if valid_pargs else []
            self.pargs_names:list[str]|None = pargs_names if pargs_names else []
            self.minimum_pargs:int = minimum_pargs
            self._usage_string:str|None = usage_string
            self.description = description

            self.kwargs:dict[str, CLIArgumentTypes] = {k:None for k in self.valid_kwargs.keys()}
            self.pargs:list[CLIArgumentTypes] = []
            self.flags:set[str] = set()

            if help_menu and len(self.raw_arguments) and (self.raw_arguments[0].startswith(help_prefix)):
                print(f"""
{self.help(self.raw_arguments[0].removeprefix(help_prefix))}
{self.usage_string}
""")
                exit(0)

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
                    if current_kw and self.kwargs[current_kw] is None:
                        raise CLIError(self, f"Keyword argument '{current_kw}' was not provided with a value.", current_kw)
                    cleaned_arg = arg.removeprefix("--")
                    if cleaned_arg in self.valid_kwargs:
                        current_kw = cleaned_arg
                        self.kwargs[current_kw] = None
                        continue
                    else:
                        raise CLIError(self, f"Invalid keyword provided '{cleaned_arg}'.", cleaned_arg)
                elif current_kw is not None and self.kwargs[current_kw] is None:
                    # Cast using the valid kwargs type dict
                    self.kwargs[current_kw] = self.validate_type_init(self.valid_kwargs, current_kw, arg)
                    continue
                elif len(self.pargs) < len(self.valid_pargs):
                    self.pargs.append(self.validate_type_init(self.valid_pargs, len(self.pargs), arg))
                    continue
                else:
                    raise CLIError(self, f"Unexpected argument '{arg}' provided without keyword.", arg)
                
            if current_kw and self.kwargs[current_kw] is None:
                raise CLIError(self, f"Keyword argument '{current_kw}' was not provided with a value.", current_kw)
        
            pargs_num = (len(self.valid_pargs) if self.minimum_pargs == -1 else self.minimum_pargs)
            if len(self.pargs) < pargs_num:
                raise CLIError(self, f"Expected {pargs_num} positional arguments recieved {len(self.pargs)} positional arguments.", len(self.valid_pargs) if self.minimum_pargs == -1 else self.minimum_pargs, len(self.pargs))

            for k, v in self.kwargs.items():
                if v is None and k in self.required_kwargs:
                    raise CLIError(self, f"Required Keyword argument '{k}' was not provided.", k)
            
            while len(self.pargs) < pargs_num:
                self.pargs.append(None)
            
        except CLIError as e:
            if exit_on_invalid:
                sys.stderr.write('\n' + e.message + '\n')
                sys.stderr.write("\n" + e.cli_arguments.usage_string + '\n\n')
                sys.stderr.flush()
                exit(1)
            else:
                raise e
            
    def validate_type(self, typ:type, argument:str, argument_key:str|None = None):
        if hasattr(typ,"__name__") and typ.__name__ in {"Path", "ExistingPath"}:
            try:
                if ((path:=ExistingPath(argument)).exists() if typ.__name__ == "ExistingPath" else (path:=Path(argument))):
                    return path
                else:
                    raise TypeError(f"Argument {argument_key if argument_key else '\b'} requires an existing file system path. The file path {argument!r} could not be found.")
            except TypeError:
                raise TypeError(f"Argument {argument_key if argument_key else '\b'} must be a valid Path type such as str. {argument} is not a valid Path type.", argument_key, argument)

        try:
            if isinstance(typ, CLIArgument):
                return typ(argument_key, argument)
            else:
                return typ(argument)
        except (ValueError, TypeError) as e:
            raise TypeError(f"Failed to convert '{argument}' to a {typ.type_name if isinstance(typ, CLIArgument) else typ.__name__}.\n\n    Reason: {e.args[0]}", argument, typ)

        
    def validate_type_init(self, collection, argument_key:str|int, argument:str) -> CLIArgumentTypes:
        try:
            typ:type|CLIArgument = collection[argument_key]
        except IndexError:
            raise CLIError(self, f"The program expects {len(collection)} arguments, {argument_key+1} were provided.", len(collection), argument_key+1, argument)
        try:
            return self.validate_type(typ, argument, argument_key)
        except TypeError as e:
            raise CLIError(self, e.args[0], *e.args[1::])
        
    def get_flag_data(self, flag:str) -> bool|CLIArgument|None:
        for item in self.valid_flags:
            if hash(item) == hash(flag):
                return item
        return None
        
    def help(self, key:str|int):
        term_size = os.get_terminal_size()
        arg_type:str|None = None
        arg_prefix:str|None = None
        if isinstance(key, int):
            cli_arg = self.valid_pargs[key]
            arg_type = "Positional Argument"
        elif key in self.valid_flags:
            cli_arg = self.get_flag_data(key)
            arg_type = "Flag"
            arg_prefix = '-'
        elif key in self.pargs_names:
            cli_arg = self.valid_pargs[self.pargs_names.index(key)]
            arg_type = "Positional Argument"
        elif key in self.valid_kwargs:
            cli_arg = self.valid_kwargs[key]
            arg_type = "Keyword Argument"
            arg_prefix = '--'
        else:
            raise CLIError(self, f"Argument '{key}' is not a valid command line argument.", key)
        
        if isinstance(cli_arg, CLIArgument):
            return f"""        {arg_prefix if arg_prefix else ""}{key}{f" ( {arg_type} ) " if arg_type else ""}:

 - Type: {cli_arg.type_name}
{f"\n{cli_arg.full_description}\n" if cli_arg.full_description != "" else ""}
{'_' * (term_size.columns-1)}"""
        else:
            return f"""        {arg_prefix if arg_prefix else ""}{key}{f" ( {arg_type} ) " if arg_type else ""}:
             
 - Type: {cli_arg.__class__.__name__}

 {'_' * (term_size.columns-1)}"""

    @property
    def usage_string(self) -> str:
        term_size = os.get_terminal_size()

        if self._usage_string is not None:
            return self._usage_string
        required = "Required "
        empty_str = ""

        if len(self.valid_flags):
            flag_str = ""
            flag_line = "    "
            padding_size = max(len(flag) + 1 for flag in self.valid_flags) + 2
            for flag in self.valid_flags:
                f_str = f'-{flag}'
                if len(flag_line + f"{f_str: <{padding_size}}") < term_size.columns:
                    flag_line += f"{f_str: <{padding_size}}"
                else:
                    flag_str += flag_line
                    flag_line = f"\n\n    {f_str: <{padding_size}}"

            flag_str += flag_line
        else:
            flag_str = ""

        if len(self.valid_kwargs):
            kwarg_str = ""
            kwarg_line = "    "
            padding_size = max(
                len(f'--{key}({required if key in self.required_kwargs else empty_str}{typ.type_name if isinstance(typ, CLIArgument) else typ.__name__})')
                    for key, typ in sorted(
                        self.valid_kwargs.items(),
                        key=lambda pair:pair[0] in self.required_kwargs,
                        reverse=True
                    )
            ) + 2
            for key, typ in sorted(self.valid_kwargs.items(), key=lambda pair:pair[0] in self.required_kwargs, reverse=True):
                kwarg = f'--{key}({required if key in self.required_kwargs else empty_str}{typ.type_name if isinstance(typ, CLIArgument) else typ.__name__})'
                if len(kwarg_line + f"{kwarg: <{padding_size}}") < term_size.columns:
                    kwarg_line += f"{kwarg: <{padding_size}}"
                else:
                    kwarg_str += kwarg_line
                    kwarg_line = f"\n\n    {kwarg: <{padding_size}}"

            kwarg_str += kwarg_line
        else:
            kwarg_str = ""

        parg_str = ""
        for i, v in enumerate(self.valid_pargs):
            if i < len(self.pargs_names) and self.pargs_names[i] is not None:
                p_name = f'  ({self.pargs_names[i]}({required if i < self.minimum_pargs else empty_str}{v.type_name if isinstance(v, CLIArgument) else v.__name__}))'
            else:
                p_name = f'  (arg{i}({required if i < self.minimum_pargs else empty_str}{v.type_name if isinstance(v, CLIArgument) else v.__name__}))'

            parg_str += p_name

        return "\nusage: " + self.program_path.name + parg_str + "\n\n" + '-'*(term_size.columns-1) +\
            ('\n\n' + self.description + '\n\n' + "-"*(term_size.columns-1) if self.description != "" else "") +\
            ('\n\nFlags:\n\n' if len(self.valid_flags) else '')+\
            flag_str +\
            ('\n\n\nKeyword Arguments:\n\n' if len(self.valid_kwargs) else '')+\
            kwarg_str + '\n'

    @usage_string.setter
    def usage_string(self, value:str):
        if isinstance(value, str):
            self._usage_string = value
            return
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
                self.pargs[parg_index] = self.validate_type(self.valid_pargs[parg_index], value, key)
            elif key in self.valid_flags:
                if self.validate_type(bool, value, key):
                    self.flags.add(key)
                else:
                    self.flags.remove(key)
            elif key in self.kwargs:
                self.kwargs[key] = self.validate_type(self.valid_kwargs[key], value, key)
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
