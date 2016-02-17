import sys
from elftools.elf.elffile import ELFFile

class FileIndexCu(object):

	def __init__(self,fname):
		self.dies = {}
		self.fh = open( fname, 'rb' )
		if self.fh:
			self.elffile = ELFFile(self.fh)
			if not self.elffile.has_dwarf_info():
				return

			self.dwarfinfo = self.elffile.get_dwarf_info()

		else:
			raise IOError

	def __del__(self):
		if self.fh:
			self.fh.close()

	def filesIn( self ):
		self.files = {}
		for cu in self.dwarfinfo.iter_CUs():
			(compFile, allFiles) = self.filesInCu(cu)
			self.files[compFile] = allFiles;
		return self.files

	def filesInCu(self,cu):
		lineprog = self.dwarfinfo.line_program_for_CU(cu)
		compFile = None
		files = []
		if lineprog:
			compFile = lineprog['file_entry'][0].name.decode('ascii')
			for ff in lineprog['file_entry']:
				di = ff.dir_index
				dname = b'.'
				if di > 0:
					dname = lineprog['include_directory'][di-1]
				files.append( "{}/{}".format( dname.decode('ascii'),
					ff.name.decode('ascii') ) )

		return (compFile,files)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		try:
			fic = FileIndexCu( sys.argv[1] )
			fi = fic.filesIn()
			for kf in fi:
				print( "{}:".format( kf ) )
				for af in fi[kf]:
					print( "\t{}".format( af ) )
		except IOError as ioe:
			print( "Cannot open file {}".format( sys.argv[1] ) )
	else:
		print( "No input file" )
