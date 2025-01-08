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
from xml.etree.ElementTree import Element as XMLElement
from ..console import Console


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
XMLNAMESPACE: str = "xmlns"
OPENINGCURLYBRACE: str = "{"
CLOSINGCURLYBRACE: str = "}"


#--------------------------------------------------------------------------------
# 요소.
#--------------------------------------------------------------------------------
class LazyXMLElement:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__xmlElement: XMLElement


	# #--------------------------------------------------------------------------------
	# # XML 부모 요소 프로퍼티.
	# #--------------------------------------------------------------------------------
	# @property
	# def Parent(self) -> LazyXMLElement:
	# 	self.__xmlElement.
	

	#--------------------------------------------------------------------------------
	# 네임스페이스 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Namespace(self) -> str:
		tag, namespace = LazyXMLElement.GetTagAndNamespaceFromElement(self.__xmlElement)
		return namespace
		

	#--------------------------------------------------------------------------------
	# 네임스페이스 프로퍼티.
	#--------------------------------------------------------------------------------
	@Namespace.setter
	def Namespace(self, value: str) -> None:
		tag, namespace = LazyXMLElement.GetTagAndNamespaceFromElement(self.__xmlElement)
		# 추가 or 수정.
		if value:
			self.__xmlElement.tag = f"{{{value}}}{self.__xmlElement.tag.split(CLOSINGCURLYBRACE)[-1]}"
		# 제거.
		elif namespace:
			self.__xmlElement.tag = self.__xmlElement.tag.split(CLOSINGCURLYBRACE)[-1]


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self, tag: str, internalElement: Optional[XMLElement] = None, **argumentDictionary) -> None:
		if self.__xmlElement != None:
			self.__xmlElement = internalElement
		else:
			self.__xmlElement = XMLElement(tag, **argumentDictionary)


	#--------------------------------------------------------------------------------
	# 자식 추가.
	#--------------------------------------------------------------------------------
	def AddChild(self, element: LazyXMLElement) -> None:
		self.__xmlElement.append(element)


	#--------------------------------------------------------------------------------
	# 자식 제거.
	#--------------------------------------------------------------------------------
	def RemoveChild(self, element: LazyXMLElement) -> None:
		self.__xmlElement.remove(element)


	#--------------------------------------------------------------------------------
	# 모든 자식 제거.
	#--------------------------------------------------------------------------------
	def RemoveAllChildren(self) -> None:
		self.__xmlElement.clear()


	#--------------------------------------------------------------------------------
	# 자식 찾기.
	#--------------------------------------------------------------------------------
	def FindChild(self, path: str, namespaces: Optional[Dict[str, str]]) -> Optional[LazyXMLElement]:
		child: XMLElement = self.__xmlElement.find(path, namespaces)
		if child == None:
			return None
		child = cast(XMLElement, child)


	#--------------------------------------------------------------------------------
	# 모든 자식 찾기.
	#--------------------------------------------------------------------------------
	def FindAllChildren(self, path: str, namespaces: Optional[Dict[str, str]]) -> List[LazyXMLElement]:
		children = list()
		for child in self.__xmlElement.findall(path, namespaces):
			child = cast(XMLElement, child)
			element = LazyXMLElement.CreateElement(child)
			children.append(element)
		return children


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateElement(tag: str, element: XMLElement = None, **argumentDictionary) -> LazyXMLElement:
		return LazyXMLElement(tag, element, **argumentDictionary)
	

	#--------------------------------------------------------------------------------
	# 태그에서 이름과 네임스페이스를 분리.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetTagAndNamespaceFromElement(element: XMLElement) -> Tuple[str, str]:
		if CLOSINGCURLYBRACE in element.tag:
			namespace, tag = element.tag[1:].split(CLOSINGCURLYBRACE)
			return tag, namespace
		else:
			return element.tag, str()