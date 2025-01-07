#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins


#--------------------------------------------------------------------------------
# 클래스 프로퍼티 데코레이터.
# - 사용시 해당 데코레이터의 대상 메서드는 클래스 메서드로 인지.
#--------------------------------------------------------------------------------
T = TypeVar("T")
def classproperty(targetMethod: Callable[[Type[T]], Any]) -> Any:
    class ClassPropertyDescriptor:
        def __init__(self, fget: Callable[[Type[T]], Any]) -> None:
            self.fget = fget
            self.fset: Optional[Callable[[Type[T], Any], None]] = None
            self.fdel: Optional[Callable[[Type[T]], None]] = None
        def __get__(self, obj: Optional[T], cls: Type[T]) -> Any:
            if self.fget is None:
                raise AttributeError("Unreadable attribute")
            return self.fget(cls)
        def __set__(self, obj: Optional[T], value: Any) -> None:
            if self.fset is None:
                raise AttributeError("Can't set attribute")
            if obj is None:
                cls = type(value)
            else:
                cls = type(obj)
            self.fset(cls, value)
        def __delete__(self, obj: Optional[T]) -> None:
            if self.fdel is None:
                raise AttributeError("Can't delete attribute")
            cls = type(obj)
            self.fdel(cls)
        def setter(self, fset: Callable[[Type[T], Any], None]) -> "ClassPropertyDescriptor":
            self.fset = fset
            return self
        def deleter(self, fdel: Callable[[Type[T]], None]) -> "ClassPropertyDescriptor":
            self.fdel = fdel
            return self
    return ClassPropertyDescriptor(targetMethod)