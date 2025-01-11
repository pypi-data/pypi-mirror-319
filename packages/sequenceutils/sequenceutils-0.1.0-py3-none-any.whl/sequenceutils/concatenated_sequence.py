from collections.abc import Iterable, Sequence
from typing import TypeVar
import bisect


T = TypeVar('T')
class ConcatenatedSequence(Sequence[T]):
    _sequence_by_start_index: dict[int, Sequence[T]]
    _start_indices: list[int]
    _range: range

    def __init__(self, sequences: Iterable[Sequence[T]] | dict[int, Sequence[T]], length: int | range | None = None):
        """Construct a sequence that is the concatenation of the given sequences.
        :param sequences: An iterable of sequences, or a dictionary mapping start
            indices to sequences. If a dictionary, then each sequence is assumed
            to start at the given index. Otherwise, if an iterable, then the
            sequences are concatenated in the order they are given.
        :param length: The length of the concatenated sequence. If a range, then
            __getitem__ will index into the range to compute the index for the
            concatenated sequence. If None, the length will be the sum of the
            lengths of the sequences."""
        # Construct _sequence_by_start_index
        if isinstance(sequences, dict):
            self._sequence_by_start_index = sequences
            if length is None:
                max_start_index = max(sequences)
                length = max_start_index + len(sequences[max_start_index])
        else:
            self._sequence_by_start_index = {}
            total_length = 0
            for s in sequences:
                if not isinstance(s, Sequence):
                    raise TypeError(f"Expected a sequence, but got {s!r}")
                if len(s) == 0:
                    continue
                self._sequence_by_start_index[total_length] = s
                total_length += len(s)
            if length is None:
                length = total_length

        # Construct _start_indices
        self._start_indices = sorted(self._sequence_by_start_index)

        # Construct _range
        if not isinstance(length, range):
            length = range(length)
        self._range = length

    def __getitem__(self, index):
        if isinstance(index, slice):
            return ConcatenatedSequence(self._sequence_by_start_index, self._range[index])
        index = self._range[index]
        start = self._start_indices[bisect.bisect_right(self._start_indices, index) - 1]
        return self._sequence_by_start_index[start][index - start]

    def __len__(self):
        return len(self._range)
