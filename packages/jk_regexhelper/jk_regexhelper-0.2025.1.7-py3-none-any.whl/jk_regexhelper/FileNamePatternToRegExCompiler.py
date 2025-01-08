

import re
import typing







#
# Static tool class to compile file name patterns such as like "testCase*.py|testcase_*.py|*Test.py" to a regular expression.
#
class FileNamePatternToRegExCompiler(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	@staticmethod
	def __compileFileNamePatternToRegExStr_part(fileNamePattern:str, ret:typing.List[str]):
		assert isinstance(fileNamePattern, str)
		assert fileNamePattern

		for c in fileNamePattern:
			if c == "?":
				ret.append(".")
			elif c == "*":
				ret.append(".*")
			else:
				ret.append(re.escape(c))
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	@staticmethod
	def compileToRegEx(fileNamePattern:typing.Union[str,typing.List[str],typing.Tuple[str],typing.Set[str],typing.FrozenSet[str]]) -> re.Pattern:
		return re.compile(FileNamePatternToRegExCompiler.compileToRegExStr(fileNamePattern))
	#

	@staticmethod
	def compileToRegExStr(fileNamePattern:typing.Union[str,typing.List[str],typing.Tuple[str],typing.Set[str],typing.FrozenSet[str]]) -> str:
		assert isinstance(fileNamePattern, (str,list,tuple,set,frozenset))

		ret = [ "^" ]

		if isinstance(fileNamePattern, str):
			if "|" in fileNamePattern:
				fileNamePattern = fileNamePattern.split("|")

		if isinstance(fileNamePattern, str):
			FileNamePatternToRegExCompiler.__compileFileNamePatternToRegExStr_part(fileNamePattern, ret)
		else:
			assert isinstance(fileNamePattern, (list,tuple,set,frozenset))
			for i,s in enumerate(fileNamePattern):
				if i > 0:
					ret.append("|")
				ret.append("(")
				FileNamePatternToRegExCompiler.__compileFileNamePatternToRegExStr_part(s, ret)
				ret.append(")")

		ret.append("$")

		return "".join(ret)
	#

#








