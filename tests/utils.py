import copy
from typing import (
    TypeVar,
    ContextManager,
)

from contextlib import contextmanager


ObjectType = TypeVar("ObjectType")


@contextmanager
def copy_context(object_: ObjectType) -> ContextManager[ObjectType]:  # PyCharm typing
    yield copy.deepcopy(object_)
