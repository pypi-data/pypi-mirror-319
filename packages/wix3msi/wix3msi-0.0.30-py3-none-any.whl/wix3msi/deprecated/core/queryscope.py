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
from .core import Database, Query, Installer


#--------------------------------------------------------------------------------
# Microsoft Installer View Creator With Context Manager.
#--------------------------------------------------------------------------------
class QueryScope:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: Database
	__query: Query
	__sqlString: str

	
	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self, database: Database, sqlString: str) -> None:
		self.__database = database
		self.__query = None
		self.__sqlString = sqlString


	#--------------------------------------------------------------------------------
	# With 시작됨.
	#--------------------------------------------------------------------------------
	def __enter__(self) -> Query:
		self.__query = Installer.CreateQuery(self.__database, self.__sqlString)
		return self.__query


	#--------------------------------------------------------------------------------
	# With 종료됨.
	#--------------------------------------------------------------------------------
	def __exit__(self, exceptionType : Optional[type], exceptionValue: Optional[BaseException],
			  tracebackException: Optional[traceback.TracebackException]) -> bool:
		if self.__query:
			self.__query.Close()
			return True
		if tracebackException:
			traceback.print_tb(tracebackException)  
		return False