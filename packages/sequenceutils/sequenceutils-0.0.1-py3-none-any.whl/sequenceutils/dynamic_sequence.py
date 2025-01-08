from collections.abc import Sequence
from typing import Callable, TypeVar


T = TypeVar('T')
class DynamicSequence(Sequence[T]):
    _item_getter: Callable[[int], T]
    _range: range

    def __init__(self, item_getter: Callable[[int], T], length: int | range):
        """Construct a sequence of the given length, where each element is
        determined by the given item getter.
        :param item_getter: A function that takes an index and returns the
            corresponding item.
        :param length: The length of the sequence. If a range, the sequence
            will be of the same length as the range, and the __getitem__
            function will index into the range to compute the index for the
            item getter.
        """
        self._item_getter = item_getter
        if not isinstance(length, range):
            length = range(length)
        self._range = length

    def __getitem__(self, index) -> T | 'DynamicSequence[T]':
        if isinstance(index, slice):
            return DynamicSequence(self._item_getter, self._range[index])
        return self._item_getter(self._range[index])

    def __len__(self) -> int:
        return len(self._range)
