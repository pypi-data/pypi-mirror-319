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
from xml.etree.ElementTree import Element


#--------------------------------------------------------------------------------
# 요소.
#--------------------------------------------------------------------------------
class Element:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__element: Element


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__element = None


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Run() -> None:
		builtins.print(f"CommandManager.Run()")