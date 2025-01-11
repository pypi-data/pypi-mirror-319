from typing import Any, Iterable, List, Optional, Set, Union


def try_int(value: Any) -> Optional[int]:
    """ Convert any value to int or None (if impossible) """
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def try_float(value: Any) -> Optional[float]:
    """ Convert any value to float or None (if impossible) """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def as_bool(value: Any) -> bool:
    """ Return True if value like true """
    return value in {True, '1', 'True', 'true', 't', b'1', b'True', b'true', b't'}


def to_string(val: Any) -> str:
    """ Convert value to string """
    if isinstance(val, bytes):
        return str(val, 'utf8', 'strict')

    if not isinstance(val, str):
        return str(val)

    return val


def to_bytes(value: Union[bytes, str, int], encoding: Optional[str] = None) -> bytes:
    if isinstance(value, str):
        return bytes(value, encoding or 'utf8')
    elif isinstance(value, int):
        return value.to_bytes((value.bit_length() + 7) // 8, 'big')
    else:
        return value


def int_list(values: Iterable[Any]) -> List[int]:
    """ Take list of any values and return list of integer where value is convertible """
    return list(filter(None, map(try_int, values)))


def int_set(values: Iterable[Any]) -> Set[int]:
    """ Like int_list but return set """
    return set(int_list(values))
