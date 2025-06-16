from .base import Result
from .deco import question, result
from .failure import Err
from .success import Ok

__all__ = ["Err", "Ok", "Result", "question", "result"]
