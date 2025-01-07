#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core import ManagedObject, ManagedObjectGarbageCollection, WeakedReference
from .component import Component


#--------------------------------------------------------------------------------
# 엔티티.
# - 고유식별자를 지니고 있으며 컴포넌트 컨테이너의 역할을 수행.
#--------------------------------------------------------------------------------
T = TypeVar("TComponent", bound = Component)
class Entity(ManagedObject):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__componentIdentifiers: list


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnCreate(self, *argumentTuple, **argumentDictionary) -> None:
		base = super()
		base.OnCreate(*argumentTuple, **argumentDictionary)
		self.__componentIdentifiers = list()


	#--------------------------------------------------------------------------------
	# 파괴 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnDestroy(self) -> None:
		for componentIdentifier in self.__componentIdentifiers:
			ManagedObject.Destroy(componentIdentifier)
		self.__componentIdentifiers.clear()
		base = super()
		base.OnDestroy()


	#--------------------------------------------------------------------------------
	# 컴포넌트 추가.
	#--------------------------------------------------------------------------------
	def AddComponent(self, componentType: Type[T], *argumentTuple, **argumentDictionary) -> Optional[WeakedReference[T]]:
		keywordArguments["ownerIdentifer"] = self.Identifier
		component: WeakedReference[T] = ManagedObject.Instantiate(componentType, *argumentTuple, **argumentDictionary)
		self.__componentIdentifiers.append(component.Identifier)
		return component
	

	#--------------------------------------------------------------------------------
	# 컴포넌트 제거.
	#--------------------------------------------------------------------------------
	def RemoveCompoent(self, componentType: Type[T]) -> bool:
		for componentIdentifier in self.__componentIdentifiers:
			obj: ManagedObject = ManagedObjectGarbageCollection.Find(componentIdentifier)
			if not obj:
				continue
			if not isinstance(obj, componentType):
				continue
			ManagedObject.Destroy(obj)
			self.__componentIdentifiers.remove(componentIdentifier)
			return True
		return False
	

	#--------------------------------------------------------------------------------
	# 컴포넌트 반환.
	#--------------------------------------------------------------------------------
	def GetComponent(self, componentType: Type[T]) -> Optional[WeakedReference[T]]:
		for componentIdentifier in self.__componentIdentifiers:
			component: WeakedReference[T] = ManagedObjectGarbageCollection.FindWeakedReference(componentIdentifier)
			if component:
				return component
		return None