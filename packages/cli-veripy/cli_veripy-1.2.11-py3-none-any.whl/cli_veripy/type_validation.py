from __future__ import annotations
from pathlib import Path
from datetime import datetime, date
from typing import TYPE_CHECKING, Callable, Generic, TypeVar
if TYPE_CHECKING:
    from cli_veripy import CLIArguments, CLIArgument

class ExistingPath(Path):
    pass

# Date-only formats
date_formats:set[str] = {
    "%Y-%m-%d",        # 2025-01-08
    "%d-%m-%Y",        # 08-01-2025
    "%m/%d/%Y",        # 01/08/2025
    "%d/%m/%Y",        # 08/01/2025
    "%b %d, %Y",       # Jan 08, 2025
    "%B %d, %Y",       # January 08, 2025
    "%d %B %Y",        # 08 January 2025
    "%A, %d %B %Y",    # Wednesday, 08 January 2025
    "%Y-%W-%w",        # 2025-02-3 (Year-Week-Weekday)
    "%Y-%U-%w",        # 2025-02-3 (Year-Week-Sunday Start)
    "%x",              # 01/08/25 (Locale's date representation)
}

time_formats:set[str] = {
    "%H:%M:%S",
    "%I:%M:%S %p",
    "%I:%M %p",
    "T%H:%M:%S",
    "T%H:%M:%S.%f",
    "T%H:%M:%S%z",
    "T%H:%M:%S.%f%z",
    "%X",                    # 14:30:45 (Locale's time representation)
}

datetime_formats:set[str] = {
    "%c",                    # Wed Jan  8 14:30:45 2025 (Locale's datetime representation)
    "%x %X",
    "%X %x",
    *[
        ''.join([s1,s2]) for s1 in date_formats for s2 in [
            "T%H:%M:%S",
            "T%H:%M:%S.%f",
            "T%H:%M:%S%z",
            "T%H:%M:%S.%f%z"
        ]
    ],
    *[
        ' '.join([s1,s2]) for s1 in date_formats for s2 in [
            "%H:%M:%S",
            "%I:%M:%S %p",
            "%I:%M %p",
            "%X",
        ]
    ],
    *[# The reverse
        ' '.join([s2,s1]) for s1 in date_formats for s2 in [
            "%H:%M:%S",
            "%I:%M:%S %p",
            "%I:%M %p",
            "%X",
        ]
    ]
}

date_and_time_formats = datetime_formats.union(date_formats).union(time_formats)

# TODO: Make format_set able to take a tuple of 2 strings ("%H:%M:%S", "Hours:Minutes:Seconds").
# The second item is a user friendly representation of the format string which will show on fail.

DATE_T = TypeVar("DATE_T")
def __dt_ext(d_type:type[DATE_T], _range_low:DATE_T|str|None, _range_high:DATE_T|str|None, _format_set:set[str], _now_str:str|set[str]|Callable[[str], bool]|None) -> type[DATE_T]:
    
    return type(
        "DateTime" if d_type.__name__ == "datetime" else "Date",
        (d_type,),
        {
            "now_str": _now_str,
            "range_low": _range_low,
            "range_high": _range_high,
            "format_set": _format_set,
        }
    )

def datetime_ext(range_low:datetime|date|str|None = None, range_high:datetime|date|str|None = None, format_set:set[str]|None = None, now_str:str|set[str]|Callable[[str], bool]|None = None):
    format_set = format_set if format_set else date_and_time_formats
    
    if isinstance(range_low, str):
        for fmt in format_set:
            try:
                range_low = datetime.strptime(range_low, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"The provided range_low DateTime string {range_low!r} does not meet any of the available formatting specifications.  Maybe try providing your own format specification via the format_set argument.", range_low)
    elif isinstance(range_low, date):
        range_low = datetime.combine(range_low, datetime.max.time())

    if isinstance(range_high, str):
        for fmt in format_set:
            try:
                range_high = datetime.strptime(range_high, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"The provided range_high DateTime string {range_high!r} does not meet any of the available formatting specifications.  Maybe try providing your own format specification via the format_set argument.", range_high)
    elif isinstance(range_high, date):
        range_high = datetime.combine(range_high, datetime.min.time())

    return __dt_ext(datetime, range_low, range_high, format_set, now_str)

def date_ext(range_low:date|datetime|str|None = None, range_high:date|datetime|str|None = None, format_set:set[str]|None = None, now_str:str|set[str]|Callable[[str], bool]|None = None):
    format_set = format_set if format_set else date_formats

    if isinstance(range_low, str):
        for fmt in format_set:
            try:
                range_low = datetime.strptime(range_low, fmt).date()
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"The provided range_low Date string {range_low!r} does not meet any of the available formatting specifications.  Maybe try providing your own format specification via the format_set argument.", range_low)
    elif isinstance(range_low, datetime):
        range_low = range_low.date()

    if isinstance(range_high, str):
        for fmt in format_set:
            try:
                range_high = datetime.strptime(range_high, fmt).date()
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"The provided range_high Date string {range_high!r} does not meet any of the available formatting specifications.  Maybe try providing your own format specification via the format_set argument.", range_high)
    elif isinstance(range_high, datetime):
        range_high = range_high.date()

    return __dt_ext(date, range_low, range_high, format_set, now_str)

IS_FIRST_PARTY_TYPE:dict[str, Callable[[str], bool]] = {
    # returns true if the specified type meets all the requirements to act as a first-party type
    "ExistingPath":lambda t: isinstance(t, ExistingPath),
    "datetime":lambda t: isinstance(t, datetime),
    "date":lambda t: isinstance(t, date),
    "Date":lambda t: all(
        hasattr(t, at) and (isinstance(attr:=getattr(t, at), (str, date, set, list, type(None))) or callable(attr))
        for at in [
            "now_str",
            "range_low",
            "range_high",
            "format_set"
        ]
    ),
    "DateTime":lambda t: all(
        hasattr(t, at) and (isinstance(attr:=getattr(t, at), (str, datetime, set, list, type(None))) or callable(attr))
        for at in [
            "now_str",
            "range_low",
            "range_high",
            "format_set"
        ]
    )
}

T = TypeVar("T")
def validate_type(_type:type[T]|CLIArgument, argument:str, key:str) -> T:
    if hasattr(_type, "__name__"): # type
        type_name = _type.__name__
    else: # CLIArgument
        if not _type.validation_function(argument):
            raise ValueError(_type.fail_validation_callback_msg(key, argument, _type.type_name))
        type_name = _type.type_name
        _type = _type.type
    
    if type_name in IS_FIRST_PARTY_TYPE and IS_FIRST_PARTY_TYPE[type_name](_type):
        match type_name:
            case "ExistingPath":
                try:
                    if (path:=ExistingPath(argument)).exists():
                        return path
                    else:
                        raise TypeError(f"Argument {key} requires an existing file system path. The file path {argument!r} could not be found.")
                except TypeError:
                    raise TypeError(f"Argument {key} must be a valid Path type such as str. {argument} is not a valid Path type.", key, argument)
                
            case "datetime":
                try:
                    for fmt in date_and_time_formats:
                        try:
                            return datetime.strptime(argument, fmt)
                        except ValueError:
                            continue
                    raise ValueError
                except ValueError:
                    raise TypeError(f"The value '{argument}' of argument '{key}' is of an invalid datetime format.\n\nValid datetime formats include:\n\n{'\n'.join([f'    {fmt}' for fmt in date_and_time_formats])}", key, argument)
                
            case "date":
                try:
                    for fmt in date_formats:
                        try:
                            return datetime.strptime(argument, fmt).date()
                        except ValueError:
                            continue
                    raise ValueError
                except ValueError:
                    raise TypeError(f"The value '{argument}' of argument '{key}' is of an invalid date format.\n\nValid date formats include:\n\n{'\n'.join([f'    {fmt}' for fmt in date_formats])}", key, argument)
                
            case "DateTime"|"Date":
                # annotate metaclass types
                format_set:list[str] = _type.format_set
                range_low:datetime|date|None = _type.range_low
                range_high:datetime|date|None = _type.range_high
                now_str:str|set[str]|None = _type.now_str
                _date:datetime|date|None = None
                
                if now_str and (
                    (isinstance(now_str, set) and argument in now_str) or 
                    (isinstance(now_str, str) and argument == now_str) or 
                    (callable(now_str) and now_str(argument))
                ):
                    _date = datetime.now()
                    if type_name == "Date":
                        _date = _date.date()
                else:
                    for fmt in format_set:
                        try:
                            _date = datetime.strptime(argument, fmt)
                            if type_name == "Date":
                                _date = _date.date()
                        except ValueError:
                            continue
                        break
                if _date:
                    if range_low and range_high:
                        if range_low <= _date <= range_high:
                            return _date
                        else:
                            err_msg_dyn_part = f"The provided date is before {range_low}." if _date < range_low else f"The provided date is after {range_high}."
                            raise TypeError(f"The provided date '{_date}' for argument '{key}' must be within the range from {range_low} to {range_high}.  {err_msg_dyn_part}", _date, range_low, range_high, key, err_msg_dyn_part)
                    elif range_low and not range_high:
                        if range_low <= _date:
                            return _date
                        else:
                            err_msg_dyn_part = f"The provided date is before {range_low}."
                            raise TypeError(f"The provided date '{_date}' for argument '{key}' must be after {range_low}.  {err_msg_dyn_part}", _date, range_low, key, err_msg_dyn_part)
                    elif not range_low and range_high:
                        if _date <= range_high:
                            return _date
                        else:
                            err_msg_dyn_part = f"The provided date is after {range_high}."
                            raise TypeError(f"The provided date '{_date}' for argument '{key}' must be before {range_high}.  {err_msg_dyn_part}", _date, range_high, key, err_msg_dyn_part)
                    else:
                        return _date
                raise TypeError(f"The value '{argument}' of argument '{key}' is of an invalid date format.\n\nValid date formats include:\n\n{'\n'.join([f'    {fmt}' for fmt in format_set])}", key, argument)

    try:
        return _type(argument)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Failed to convert '{argument}' to a {type_name}.\n\n    Reason: {e.args[0]}", argument, _type)