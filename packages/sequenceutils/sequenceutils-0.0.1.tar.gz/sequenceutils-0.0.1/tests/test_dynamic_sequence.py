from sequenceutils import DynamicSequence
import pytest


def test_empty_sequence():
    def raise_error():
        raise RuntimeError("This should not be called")
    seq = DynamicSequence(raise_error, length=0)
    assert len(seq) == 0
    with pytest.raises(IndexError):
        seq[0]
    with pytest.raises(IndexError):
        seq[1]
    with pytest.raises(IndexError):
        seq[-1]
    assert list(seq) == []


def test_single_element_sequence():
    element = object()
    def get_item(index):
        assert index == 0
        return element
    seq = DynamicSequence(get_item, length=1)
    assert len(seq) == 1
    assert seq[0] is element
    with pytest.raises(IndexError):
        seq[1]
    assert seq[-1] is element
    with pytest.raises(IndexError):
        seq[-2]


def test_huge_sequence():
    def get_item(index):
        return index + 1
    seq = DynamicSequence(get_item, length=10**15)
    assert len(seq) == 10**15
    assert seq[0] == 1
    assert seq[1] == 2
    assert seq[::-1][-1] == 1
    assert seq[-1] == 10**15
