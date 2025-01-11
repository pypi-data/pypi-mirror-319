from __future__ import annotations

import functools
import inspect
import logging
from collections.abc import Callable, Iterable
from typing import Any, ClassVar, TypeVar

__all__ = ['StrJoiner', 'SpaceJoiner', 'LineBreakJoiner', 'DotJoiner', 'StrJoinerT', ]
WrappedFuncT = Callable[..., Iterable]


class StrJoiner:
    """Decorator to join strings, emitted by generator function

    Examples:

    >>> @SpaceJoiner()
    ... def test():
    ...     yield None # will be excluded
    ...     yield 'test1'
    ...     yield 't'
    ...     yield '' # also excluded
    ...

    >>> test()
    'test1 t'

    """
    __slots__ = ['delimiter', 'wrapper', 'max_width', 'min_width', ]
    DEFAULT_DELIMITER: ClassVar[Any] = ''

    def __init__(self,
                 __func: Any = None,
                 *,
                 delimiter: str = None,
                 max_width: int | None = None,
                 min_width: int | None = None):
        if __func is not None:
            raise ValueError('Do not use Joiner as direct decorator like StrJoiner(func), '
                             'always create new objects, then decorate: StrJoiner()(func)')

        self.max_width: int | None = max_width
        self.min_width: int | None = min_width

        if delimiter is None:
            delimiter = self.DEFAULT_DELIMITER
        self.delimiter: str = delimiter

    def __parser__(self, __obj: Any) -> str | None:
        if __obj is not None:
            try:
                return str(__obj)
            except RecursionError as ex:
                logging.exception('%s while parsing %s', f'{ex!r}', f'{self!r}')
            return ''
        return None

    def _pad_value(self, value: str) -> str:
        if (min_width := self.min_width) is not None:
            if len(value) < min_width:
                return value.ljust(min_width)
        return value

    def _to_str_iter(self, __iter: Iterable) -> Iterable[str]:
        parser = self.__parser__

        for part in __iter:
            if part is None:
                continue

            if len(str_part := parser(part)) == 0:
                continue

            yield str_part

    def _to_str_iter_limited(self, __iter: Iterable) -> Iterable[str]:
        width = 0
        max_width = self.max_width
        delimiter_width = len(self.delimiter)
        prev_part = None

        for part in self._to_str_iter(__iter):
            if (new_width := width + delimiter_width + len(part)) > max_width:
                yield f'{prev_part}...'
                return

            if prev_part is not None:
                yield prev_part

            prev_part = part
            width = new_width

        if prev_part is not None:
            yield prev_part

    def __call__(self, func: WrappedFuncT) -> Callable[..., str]:
        """Actual wrapping of """
        if not inspect.isgeneratorfunction(func):
            raise TypeError(f'{self.__class__} expected to decorate generator, got {func}')

        _joiner = self.join

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            func_result = func(*args, **kwargs)
            return _joiner(func_result)

        return wrapped

    def join_parts(self, *parts: Any) -> str:
        return self.join(parts)

    def join(self, __iter: Iterable) -> str:
        parts = self._to_str_iter(__iter) \
            if self.max_width is None else \
            self._to_str_iter_limited(__iter)

        value = self.delimiter.join(parts)
        return self._pad_value(value)

    def _repr_args_iter(self):
        yield '<'
        yield self.__class__.__name__

        if (delimiter := self.delimiter) != self.DEFAULT_DELIMITER:
            yield f'{delimiter=}'

        yield '>'

    def __repr__(self):
        return _str_joiner.join(self._repr_args_iter())


class SpaceJoiner(StrJoiner):
    DEFAULT_DELIMITER = " "


class LineBreakJoiner(StrJoiner):
    DEFAULT_DELIMITER = "\n"


class DotJoiner(StrJoiner):
    DEFAULT_DELIMITER = "."


_str_joiner = StrJoiner()
StrJoinerT = TypeVar('StrJoinerT', bound=StrJoiner)
