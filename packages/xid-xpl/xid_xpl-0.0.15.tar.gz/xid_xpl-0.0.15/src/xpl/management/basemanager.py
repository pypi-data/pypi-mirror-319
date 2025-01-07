#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from threading import Lock
from ..core import BaseClass
from ..decorator import classproperty


#--------------------------------------------------------------------------------
# 베이스 매니저 클래스.
#--------------------------------------------------------------------------------
T = TypeVar("T", bounds = "BaseManager")
class BaseManager(BaseClass, Generic[T]):
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__SharedInstance: T = None
	__Lock: Lock = Lock()


	#--------------------------------------------------------------------------------
	# 공유 인스턴스 프로퍼티.
	#--------------------------------------------------------------------------------
	@classproperty
	def Instance(classType: Type[T]) -> T:
		if classType.__SharedInstance is None:
			with classType.__Lock:
				if classType.__SharedInstance is None:
					classType.__SharedInstance = classType()
		return classType.__SharedInstance


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		# base = super()
		# base.__init__()
		pass