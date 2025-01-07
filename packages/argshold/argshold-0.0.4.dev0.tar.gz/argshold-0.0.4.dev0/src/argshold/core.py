from __future__ import annotations

import functools
from typing import *

from datarepr import datarepr
from frozendict import frozendict


class FrozenArgumentHolder:
    def __eq__(self, other, /) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.args == other.args and self.kwargs == other.kwargs

    def __hash__(self) -> int:
        return (self.args, self.kwargs).__hash__()

    def __len__(self) -> int:
        return len(self.args) + len(self.kwargs)

    def __init__(self, *args, **kwargs) -> None:
        self._args = tuple(args)
        self._kwargs = frozendict(kwargs)

    def __repr__(self) -> str:
        return datarepr(type(self).__name__, *self.args, **self.kwargs)

    def __setattr__(self, name, value) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            msg = "%r object has no attribute %r"
            msg %= (name, value)
            raise AttributeError(msg)

    @property
    def args(self) -> tuple:
        "This property holds the positional arguments."
        return self._args

    def call(self, callable: Callable) -> Any:
        "This method calls a callable using the arguments in the current instance."
        return callable(*self.args, **self.kwargs)

    def copy(self) -> FrozenArgumentHolder:
        "This method makes a copy of the current instance."
        return self.call(type(self))

    @property
    def kwargs(self) -> frozendict:
        "This property holds the keyword arguments."
        return self._kwargs

    def partial(self, callable: Callable) -> functools.partial:
        return functools.partial(callable, *self.args, **self.kwargs)

    def partialmethod(self, callable: Callable) -> functools.partial:
        return functools.partialmethod(
            callable,
            *self.args,
            **self.kwargs,
        )
