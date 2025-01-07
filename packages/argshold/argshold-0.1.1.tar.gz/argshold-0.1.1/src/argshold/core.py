from __future__ import annotations

import abc
import functools
from typing import *

from datarepr import datarepr
from frozendict import frozendict

__all__ = ["ArgumentHolder", "FrozenArgumentHolder"]


class BaseArgumentHolder(abc.ABC):

    __slots__ = ("_args", "_kwargs")

    def __eq__(self, other, /) -> bool:
        "This magic method returns self==other."
        if not isinstance(other, BaseArgumentHolder):
            return False
        return self.args == other.args and self.kwargs == other.kwargs

    @abc.abstractmethod
    def __init__(self, *args, **kwargs): ...

    def __len__(self) -> int:
        "This magic method returns len(self)."
        return len(self.args) + len(self.kwargs)

    def __repr__(self) -> str:
        "This magic method returns repr(self)."
        return datarepr(type(self).__name__, *self.args, **self.kwargs)

    @property
    @abc.abstractmethod
    def args(self): ...

    def call(self, callable: Callable) -> Any:
        "This method calls a callable using the arguments in the current instance."
        return callable(*self.args, **self.kwargs)

    def copy(self):
        "This method makes a copy of the current instance."
        return self.call(type(self))

    @property
    @abc.abstractmethod
    def kwargs(self): ...

    def partial(self, callable: Callable) -> functools.partial:
        return functools.partial(callable, *self.args, **self.kwargs)

    def partialmethod(self, callable: Callable) -> functools.partial:
        return functools.partialmethod(
            callable,
            *self.args,
            **self.kwargs,
        )

    def toArgumentHolder(self) -> ArgumentHolder:
        return self.call(ArgumentHolder)

    def toFrozenArgumentHolder(self) -> FrozenArgumentHolder:
        return self.call(FrozenArgumentHolder)


class ArgumentHolder(BaseArgumentHolder):

    def __init__(self, *args, **kwargs) -> None:
        "This magic method sets up the current instance."
        self._args = list(args)
        self._kwargs = dict(kwargs)

    @property
    def args(self) -> list:
        "This property holds the positional arguments."
        return self._args

    @args.setter
    def args(self, value: Any) -> None:
        value = list(value)
        self._args.clear()
        self._args.extend(value)

    @args.deleter
    def args(self) -> None:
        self._args.clear()

    @property
    def kwargs(self) -> dict:
        "This property holds the keyword arguments."
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value: Any) -> None:
        value = dict(value)
        self._kwargs.clear()
        self._kwargs.update(value)

    @kwargs.deleter
    def kwargs(self) -> None:
        self._kwargs.clear()


class FrozenArgumentHolder(BaseArgumentHolder):
    def __hash__(self) -> int:
        "This magic method returns hash(self)."
        return (self.args, self.kwargs).__hash__()

    def __init__(self, *args, **kwargs) -> None:
        "This magic method sets up the current instance."
        self._args = tuple(args)
        self._kwargs = frozendict(kwargs)

    @property
    def args(self) -> tuple:
        "This property holds the positional arguments."
        return self._args

    @property
    def kwargs(self) -> frozendict:
        "This property holds the keyword arguments."
        return self._kwargs
