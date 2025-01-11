#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..ecs import Entity, Component
from .target import Target


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
LINEFEED: str = "\n"
READTEXT: str = "rt"
READBINARY: str = "rb"
WRITETEXT: str = "wt"
WRITEBINARY: str = "wb"
UTF8: str = "utf-8"
TAB: str = "\t"


#------------------------------------------------------------------------
# 작업 공정.
#------------------------------------------------------------------------
class Task(Entity):
	#------------------------------------------------------------------------
	# 멤버 변수 목록.
	#------------------------------------------------------------------------


	#------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#------------------------------------------------------------------------
	def OnCreate(self, *argumentTuple, **argumentDictionary) -> None:
		base = super()
		base.OnCreate(*argumentTuple, **argumentDictionary)
		

	#------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#------------------------------------------------------------------------
	def OnDestroy(self) -> None:
		base = super()
		base.OnDestroy()


	#------------------------------------------------------------------------
	# 시작됨.
	#------------------------------------------------------------------------
	def OnStart(self, target: Target) -> None:
		return


	#------------------------------------------------------------------------
	# 종료됨.
	#------------------------------------------------------------------------
	def OnComplete(self, target: Target, resultCode: int) -> None:
		return


	#------------------------------------------------------------------------
	# 실행됨.
	#------------------------------------------------------------------------
	def OnExecute(self, target: Target, *argumentTuple, **argumentDictionary) -> int:
		return 0
	

	#------------------------------------------------------------------------
	# 실행.
	#------------------------------------------------------------------------
	def Execute(self, target: Target, *argumentTuple, **argumentDictionary) -> int:
		try:
			self.OnStart(target)
			resultCode = self.OnExecute(target, *argumentTuple, **argumentDictionary)
			self.OnComplete(target, resultCode)
			return resultCode
		except Exception as exception:
			raise
