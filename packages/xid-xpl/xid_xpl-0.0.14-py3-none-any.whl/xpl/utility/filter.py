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
# 필터 클래스.
#--------------------------------------------------------------------------------
T = TypeVar("T")
class Filter(Generic[T]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__iterable: Iterable[T]
	__predicate: Callable[[T], bool]


	#--------------------------------------------------------------------------------
	# 반복자가 반복하기 위해 반복 될 수 있는 대상 목록.
	#--------------------------------------------------------------------------------
	@property
	def Iterable(self) -> Iterable[T]:
		return self.__iterable

	#--------------------------------------------------------------------------------
	# 반복자가 반복하기 위해 반복 될 수 있는 대상 목록.
	#--------------------------------------------------------------------------------
	@Iterable.setter
	def Iterable(self, iterable: Iterable[T]) -> None:
		self.__iterable = iterable


	#--------------------------------------------------------------------------------
	# 조건 평가를 위한 함수 객체.
	# - None이면 조건 평가를 하지 않고 무조건 True.
	#--------------------------------------------------------------------------------
	@property
	def Predicate(self) -> Callable[[T], bool]:
		return self.__predicate


	#--------------------------------------------------------------------------------
	# 조건 평가를 위한 함수 객체.
	# - None이면 조건 평가를 하지 않고 무조건 True.
	#--------------------------------------------------------------------------------
	@Predicate.setter
	def Predicate(self, predicate: Callable[[T], bool]) -> None:
		self.__predicate = predicate


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self):
		self.__iterable = None
		self.__predicate = None


	#--------------------------------------------------------------------------------
	# 반복문 순회.
	#--------------------------------------------------------------------------------
	def __iter__(self) -> Iterator[T]:
		if self.__predicate:
			for item in self.__iterable:
				if self.__predicate(item):
					yield item
		else:
			for item in self.__iterable:
				yield item