import sys
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

class FindUndefs(object):

	def __init__(self,fname):
		self.secSymbols = []
		self.fh = open( fname, 'rb' )
		if self.fh:
			self.elffile = ELFFile(self.fh)

			for section in self.elffile.iter_sections():
				if isinstance( section, SymbolTableSection ):
					self.secSymbols.append( section )
		else:
			raise IOError

	def __del__(self):
		if self.fh:
			self.fh.close()

	def getSec(self):
		return self.secSymbols

	def findUndef(self):
		self.undefs = []
		for ss in self.secSymbols:
			self.undefs.extend( self.findUndefInSec(ss) )
		return self.undefs

	def findUndefInSec(self,sec):
		undefs = []
		for sb in sec.iter_symbols():
			if sb['st_shndx'] == 'SHN_UNDEF' and sb.name:
				undefs.append( sb.name )
		return undefs

if __name__ == '__main__':
	if len(sys.argv) > 1:
		try:
			fu = FindUndefs( sys.argv[1] )
			for ius, us in enumerate(fu.findUndef()):
				print( "{}: {}".format( ius, us ) )
		except IOError as ioe:
			print( "Cannot open file {}".format( sys.argv[1] ) )
	else:
		print( "No input file" )
