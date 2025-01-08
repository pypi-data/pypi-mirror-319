

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
	def __compileFileNamePatternToRegExStr_part(fileNamePattern:str) -> str:
		assert isinstance(fileNamePattern, str)
		assert fileNamePattern

		ret = []

		for c in fileNamePattern:
			if c == "?":
				ret.append(".")
			elif c == "*":
				ret.append(".*")
			else:
				ret.append(re.escape(c))

		return "".join(ret)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	#
	# This method will first invoke <c>compileToRegExStr(..)</c> and then compile the regex string to an instance of <c>re.Pattern</c>.
	#
	@staticmethod
	def compileToRegEx(fileNamePattern:typing.Union[str,typing.List[str],typing.Tuple[str],typing.Set[str],typing.FrozenSet[str]]) -> re.Pattern:
		return re.compile(FileNamePatternToRegExCompiler.compileToRegExStr(fileNamePattern))
	#

	#
	# This method will first invoke <c>compileToRegExStrList(..)</c> and then join all fragments using '(..)|(..)'.
	# Therefore this method will group every fragment (thus introducing new unnamed regex groups).
	#
	@staticmethod
	def compileToRegExStr(fileNamePattern:typing.Union[str,typing.List[str],typing.Tuple[str],typing.Set[str],typing.FrozenSet[str]]) -> str:
		ret = []

		singles = FileNamePatternToRegExCompiler.compileToRegExStrList(fileNamePattern)
		for i,s in enumerate(singles):
			if i > 0:
				ret.append("|")
			ret.append("(")
			ret.append(s)
			ret.append(")")

		return "".join(ret)
	#

	#
	# @return		Returns a list of regex fragments. For use concat those fragments using '(..)|(..)'.
	#
	@staticmethod
	def compileToRegExStrList(fileNamePattern:typing.Union[str,typing.List[str],typing.Tuple[str],typing.Set[str],typing.FrozenSet[str]]) -> typing.List[str]:
		assert isinstance(fileNamePattern, (str,list,tuple,set,frozenset))

		ret = []

		if isinstance(fileNamePattern, str):
			if "|" in fileNamePattern:
				fileNamePattern = fileNamePattern.split("|")

		if isinstance(fileNamePattern, str):
			ret.append(FileNamePatternToRegExCompiler.__compileFileNamePatternToRegExStr_part(fileNamePattern))
		else:
			assert isinstance(fileNamePattern, (list,tuple,set,frozenset))
			for s in fileNamePattern:
				ret.append(FileNamePatternToRegExCompiler.__compileFileNamePatternToRegExStr_part(s))

		return ret
	#

#








