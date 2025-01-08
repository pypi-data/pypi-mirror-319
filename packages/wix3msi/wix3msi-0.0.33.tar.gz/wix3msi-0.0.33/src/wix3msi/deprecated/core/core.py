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
import os
import msilib # type: ignore
from xpl import BaseClass
# from xpl import Interface, BaseClass, abstractmethod


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
SQL_CREATE_PROPERTYTABLE: str = "CREATE TABLE Property (Property TEXT NOT NULL PRIMARY KEY, Value TEXT)"
SQL_EXISTS_TABLE: str = "SELECT Name FROM _Tables WHERE Name = ?"
UNDEFINED: str = "undefined"


#--------------------------------------------------------------------------------
# 데이터베이스 인터페이스.
#--------------------------------------------------------------------------------
class Database(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: msilib.Database	


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self, database: msilib.Database) -> None:
		self.__database = database


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __str__(self) -> str:
		return str(self.__database)
	

	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	def GetRawData(self) -> msilib.Database:
		return self.__database


	#--------------------------------------------------------------------------------
	# 테이블 반환.
	#--------------------------------------------------------------------------------
	def GetTable(self, tableName: str) -> Table:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 적용.
	#--------------------------------------------------------------------------------
	def Commit(self) -> None:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 닫기.
	#--------------------------------------------------------------------------------
	def Close(self) -> None:
		raise NotImplementedError()


#--------------------------------------------------------------------------------
# 테이블 인터페이스.
#--------------------------------------------------------------------------------
class Table(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: Database
	__tableName: str
	# __columnNames: list
	# __columnTypes: list

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self, database: Database, tableName: str) -> None:
		self.__database = database
		self.__tableName = tableName
		self.__columnNames = list()
		self.__columnTypes = list()
		# for column in self.GetColumns():
		# 	self.__columnNames.append(column[0])
		# 	self.__columnTypes.append(column[1])


	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	def GetDatabase(self) -> msilib.Database:
		return self.__database
	

	#--------------------------------------------------------------------------------
	# 테이블 이름.
	#--------------------------------------------------------------------------------
	def GetTableName(self) -> str:
		return self.__tableName
	

	#--------------------------------------------------------------------------------
	# 컬럼 정보 반환.
	#--------------------------------------------------------------------------------
	def GetColumns(self) -> list: pass


	#--------------------------------------------------------------------------------
	# 모든 레코드 반환.
	#--------------------------------------------------------------------------------		
	def GetAllRecords(self) -> list: pass


	#--------------------------------------------------------------------------------
	# 레코드 추가.
	#--------------------------------------------------------------------------------	
	def Insert(self, record: Record) -> None: pass


	#--------------------------------------------------------------------------------
	# 레코드 제거.
	#--------------------------------------------------------------------------------
	def Remove(self, record: Record) -> None: pass


	#--------------------------------------------------------------------------------
	# 레코드 갱신.
	#--------------------------------------------------------------------------------
	def Update(self, record: Record) -> None: pass


	#--------------------------------------------------------------------------------
	# 레코드 업데이트.
	#--------------------------------------------------------------------------------
	def UpdateRecords(self, whereFieldName: str, whereFieldValue: Union[int, str, None], updateFieldName: str, updateFieldValue: Union[int, str, None]) -> None: pass


#--------------------------------------------------------------------------------
# 쿼리 인터페이스.
#--------------------------------------------------------------------------------
class Query(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__view: msilib.View


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self, view: msilib.View) -> None:
		self.__view = view


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __str__(self) -> str:
		return str(self.__view)
	

	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	def GetRawData(self) -> msilib.View:
		return self.__view


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Execute(self, value: Union[Record, Tuple, None] = None) -> None:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 가져오기.
	#--------------------------------------------------------------------------------
	def Fetch(self) -> Optional[Record]:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 닫기.
	#--------------------------------------------------------------------------------
	def Close(self) -> None:
		raise NotImplementedError()


#--------------------------------------------------------------------------------
# 레코드 인터페이스.
#--------------------------------------------------------------------------------
class Record(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__record: msilib.Record


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(self, record: msilib.Record) -> None:
		self.__record = record


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __str__(self) -> str:
		return str(self.__record)
	

	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	def GetRawData(self) -> msilib.Record:
		return self.__record


	#--------------------------------------------------------------------------------
	# 필드 갯수 반환.
	#--------------------------------------------------------------------------------
	def GetFieldCount(self) -> int:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	def GetFieldValueAsInteger(self, fieldIndex: int) -> int:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	def GetFieldValueAsString(self, fieldIndex: int) -> str:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	def GetFieldValue(self, fieldIndex: int) -> Union[int, str, None]:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValueAsInteger(self, fieldIndex: int, value: int) -> None:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValueAsString(self, fieldIndex: int, value: str) -> None:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValueAsStream(self, fieldIndex: int, filePath: str) -> None:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValue(self, fieldIndex: int, value: Union[int, str, None]) -> None:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValues(self, fieldValues: Tuple) -> None:
		raise NotImplementedError()


#--------------------------------------------------------------------------------
# 인스톨러.
#--------------------------------------------------------------------------------
class Installer(BaseClass):
	#--------------------------------------------------------------------------------
	# GUID 생성.
	# - 생성된 값: "{12345678-1234-1234-1234-123456789ABC}"
	# - uuid4로 대체 가능.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateGUID() -> str:
		try:
			return msilib.gen_uuid()
		except Exception as exception:
			builtins.print(exception)
			raise
	

	#--------------------------------------------------------------------------------
	# 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateDatabase(msiFilePath: str) -> Database:
		try:
			msilib.init_database(msiFilePath, msilib.schema, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED)
		except Exception as exception:
			builtins.print(exception)
			raise
		
		database: Database = Installer.OpenDatabase(msiFilePath)
		return database


	#--------------------------------------------------------------------------------
	# 불러오기.
	#--------------------------------------------------------------------------------
	@staticmethod
	def OpenDatabase(msiFilePath: str) -> Database:
		try:
			database: msilib.Database = msilib.OpenDatabase(msiFilePath, msilib.MSIDBOPEN_TRANSACT)
		except Exception as exception:
			builtins.print(exception)
			raise

		from .databaseimpl import DatabaseImpl
		return DatabaseImpl(database)


	#--------------------------------------------------------------------------------
	# 불러오기. (읽기전용)
	#--------------------------------------------------------------------------------
	@staticmethod
	def OpenDatabaseAsReadonly(msiFilePath: str) -> Database:
		try:
			database: msilib.Database = msilib.OpenDatabase(msiFilePath, msilib.MSIDBOPEN_READONLY)
		except Exception as exception:
			builtins.print(exception)
			raise

		from .databaseimpl import DatabaseImpl
		return DatabaseImpl(database)
	

	#--------------------------------------------------------------------------------
	# 테이블 존재 유무.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ExistsTable(database: Database, tableName: str) -> bool:
		fieldValues: Tuple = (tableName,)
		record: Record = Installer.CreateRecordFromFieldValues(fieldValues)
		try:
			query: Query = Installer.CreateQuery(database, SQL_EXISTS_TABLE)
			query.Execute(record)
			data = query.Fetch()
			query.Close()
			if data == None:
				return False
			elif data.GetFieldCount() == 0:
				return False
			return True
		except Exception as exception:
			return False


	#--------------------------------------------------------------------------------
	# 테이블 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateTable(database: Database, tableName: str, fields: list) -> Table:
		if not Installer.ExistsTable(database, tableName):
			fieldsString: str = str() # Component TEXT PRIMARY KEY, Directory_ TEXT, Attributes INTEGER, Guid TEXT

			fieldCount: int = builtins.len(fields)
			for index in range(fieldCount):
				field: str = fields[index]
				if not field:
					raise ValueError()
				
				values = field.split(" ")
				name: str = values[0]
				type: str = "TEXT"
				isPrimaryKey: bool = False
				wordCount: int = builtins.len(values)

				# 문제가 있음.
				if wordCount == 0:
					raise IndexError()

				if wordCount > 0:
					name: str = values[0]
				if wordCount > 1:
					type = values[1]
				if wordCount > 2:
					isPrimaryKey = True

				if index + 1 < fieldCount:
					if isPrimaryKey:
						fieldsString += f"{name} {type} PRIMARY KEY, "
					else:
						fieldsString += f"{name} {type}, "
				else:
					if isPrimaryKey:
						fieldsString += f"{name} {type} PRIMARY KEY"
					else:
						fieldsString += f"{name} {type}"

		query: Query = Installer.CreateQuery(database, f"CREATE TABLE {tableName} ({fieldsString})")
		query.Execute()
		from .tableimpl import TableImpl
		table = TableImpl(database, tableName)
		query.Close()


	#--------------------------------------------------------------------------------
	# 쿼리 생성하기. (뷰)
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateQuery(database: Database, sqlString: str) -> Query:
		try:
			builtins.print(sqlString)
			rawdata: msilib.Databse = database.GetRawData()
			view: msilib.View = rawdata.OpenView(sqlString)
		except Exception as exception:
			builtins.print(exception)
			raise
	
		from .queryimpl import QueryImpl
		return QueryImpl(view)
	

	#--------------------------------------------------------------------------------
	# 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateRecord(fieldCount: int) -> Record:
		try:
			record: msilib.Record = msilib.CreateRecord(fieldCount)
		except Exception as exception:
			builtins.print(exception)
			raise

		from .recordimpl import RecordImpl
		return RecordImpl(record)
	

	#--------------------------------------------------------------------------------
	# 필드값 목록으로부터 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateRecordFromFieldValues(fieldValues: Tuple) -> Record:
		try:
			fieldCount: int = builtins.len(fieldValues)
			if fieldCount == 0:
				raise ValueError(f"invalid field values: {fieldValues}")
			record: Record = Installer.CreateRecord(fieldCount)
			record.SetFieldValues(fieldValues)
			return record
		except Exception as exception:
			builtins.print(exception)
			raise
	

	#--------------------------------------------------------------------------------
	# 필드값 목록으로부터 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFieldValuesFromRecord(record: Record) -> Optional[Tuple]:
		try:
			if not record:
				raise ValueError(f"invalid record.")
			if record.GetFieldCount() == 0:
				raise ValueError(f"invalid record.")
			return tuple(record.GetFieldValue(index) for index in range(record.GetFieldCount()))
		except Exception as exception:
			builtins.print(exception)
			raise