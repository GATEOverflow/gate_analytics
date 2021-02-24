from typing import TypeVar

T = TypeVar("T")


def make_batch(items: list[T], size: int) -> list[tuple[T, ...]]:
    return list(zip(*([iter(items)] * size)))
