import pytest


def split_at_values(lst, values):
    indices = [i for i, x in enumerate(lst) if x in values]
    size = len(lst)
    res = [lst[indices[i] + 1: indices[i + 1] if i + 1 <= len(indices) - 1 else size ] for i in
           range(0, len(indices))]
    return res, indices

def test_split_at_values():
    list1 = ["vehicle0", "W2", "vehicle1", "H1", "W1"]
    list2 = ["vehicle0", "vehicle1", "H1", "W1"]
    list3 = ["vehicle0", "vehicle1"]
    list4 = ["vehicle0", "vehicle1", "H1", "W1", "vehicle2"]
    list5 = ["vehicle0", "vehicle1", "H1", "W1"]

    assert split_at_values(list1, ["vehicle0", "vehicle1"]) == ([["W2"], ["H1", "W1"]], [0, 2])
    assert split_at_values(list2, ["vehicle0", "vehicle1"]) == ([[], ["H1", "W1"]], [0, 1])
    assert split_at_values(list3, ["vehicle0", "vehicle1"]) == ([[], []], [0, 1])
    assert split_at_values(list4, ["vehicle0", "vehicle1", "vehicle2"]) == ([[], ["H1", "W1"], []], [0, 1, 4])
    assert split_at_values(list5, ["vehicle0", "vehicle1"]) == ([[], ["H1", "W1"]], [0,1])

