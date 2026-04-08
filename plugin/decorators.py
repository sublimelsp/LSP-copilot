from __future__ import annotations

from functools import wraps
from typing import Any, Callable, cast

from .types import T_Callable
from .utils import is_active_view


def must_be_active_view(*, failed_return: Any = None) -> Callable[[T_Callable], T_Callable]:
    def decorator(func: T_Callable) -> T_Callable:
        @wraps(func)
        def wrapped(self: Any, *arg, **kwargs) -> Any:
            if is_active_view(self.view):
                return func(self, *arg, **kwargs)
            return failed_return

        return cast(T_Callable, wrapped)

    return decorator
