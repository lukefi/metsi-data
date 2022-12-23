from typing import Optional, Any, List, Callable


def parse_int(source: str) -> Optional[int]:
    try:
        return int(source)
    except (ValueError, TypeError):
        return None


def parse_float(source: str) -> Optional[float]:
    try:
        return float(source)
    except (ValueError, TypeError):
        return None


def get_or_default(maybe: Optional[Any], default: Any = None) -> Any:
    return default if maybe is None else maybe


def multifilter(data: List, *predicates: Callable) -> List:
    """Filter given data list using given predicate functions i.e. the returned list contains elements for which
    each predicate function returns True."""
    return list(filter(
        lambda item: all(p(item) for p in predicates),
        data
    ))


def neg(predicate: Callable) -> Callable:
    return lambda x: not predicate(x)
