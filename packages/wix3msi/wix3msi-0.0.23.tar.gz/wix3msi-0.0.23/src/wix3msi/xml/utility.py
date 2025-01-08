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
import re
import uuid
from xml.dom import minidom as Minidom
from xml.dom.minidom import Document as MinidomDocument
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
EMPTY: str = ""
# RE_REMOVE_NS0: str = "(ns0:|ns0|:ns0)"
LINEFEED: str = "\n"
NS0: str = "ns0"
NS0FRONTCOLON: str = ":ns0"
NS0BACKCOLON: str = "ns0:"

#--------------------------------------------------------------------------------
# 유틸리티.
#--------------------------------------------------------------------------------
class Utility:
	#--------------------------------------------------------------------------------
	# ns0 제거하고 다시 저장.
	#--------------------------------------------------------------------------------
	@staticmethod
	def SaveXMLFileWithoutNS0(xmlFilePath: str) -> None:
		# 파일 읽기.
		content: str = str()
		with builtins.open(xmlFilePath, mode = FILE_READTEXT, encoding = UTF8) as inputFile:
			content = inputFile.read()

			# 네임스페이스 제거.
			content = content.replace(NS0, EMPTY)
			content = content.replace(NS0FRONTCOLON, EMPTY)
			content = content.replace(NS0BACKCOLON, EMPTY)

		# 재저장.
		with builtins.open(xmlFilePath, mode = FILE_WRITETEXT, encoding = UTF8) as outputFile:
			outputFile.write(content)