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
import traceback
from. core import Database, Installer


#--------------------------------------------------------------------------------
# Microsoft Installer Database Creator With Context Manager.
#--------------------------------------------------------------------------------
class DatabaseScope:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: Database
	__msiFilePath: str

	
	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self, msiFilePath: str) -> None:
		self.__database = None
		self.__msiFilePath = msiFilePath


	#--------------------------------------------------------------------------------
	# With 시작됨.
	#--------------------------------------------------------------------------------
	def __enter__(self) -> Database:
		self.__database = Installer.CreateDatabase(self.__msiFilePath)
		return self.__database


	#--------------------------------------------------------------------------------
	# With 종료됨.
	#--------------------------------------------------------------------------------
	def __exit__(self, exceptionType : Optional[type], exceptionValue: Optional[BaseException],
			  tracebackException: Optional[traceback.TracebackException]) -> bool:
		if self.__database:
			self.__database.Commit()
			self.__database.Close()
			return True
		if tracebackException:
			traceback.print_tb(tracebackException)  
		return False
