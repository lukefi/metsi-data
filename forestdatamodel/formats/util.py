from typing import Optional, Any


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
