import sys
from elftools.dwarf.die import DIE
from elftools.dwarf.compileunit import CompileUnit

class DieByOffset(object):

	CUs = {}

	def __init__(self,cu):
		self.cu = cu
		if cu.cu_offset not in DieByOffset.CUs:
			DieByOffset.CUs[cu.cu_offset] = (cu,self._addCu(cu))

	def _addCu(self,cu):
		cuByOffset = {}
		for dd in cu.iter_DIEs():
			cuByOffset[dd.offset] = dd
		return cuByOffset

	def getDie(self,offset):
		DieByOffset.getDieInCu(offset,self.cu)

	def __getitem__(self,offset):
		self.getDie(offset)

	@staticmethod
	def getDieInCu(offset,cu):
		if hasattr(cu,'cu_offset') and cu.cu_offset in DieByOffset.CUs: 
			if offset in DieByOffset.CUs[cu.cu_offset][1]:
				return DieByOffset.CUs[cu.cu_offset][1][offset]

		return None

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		from elftools.elf.elffile import ELFFile
		with open( sys.argv[1], 'rb' ) as fh:
			elfFile = ELFFile( fh )
			if elfFile.has_dwarf_info():
				dwInfo = elfFile.get_dwarf_info()
				for cu in dwInfo.iter_CUs():
					dbo = DieByOffset(cu)
		for ic, cc in enumerate(DieByOffset.CUs):
			td = DieByOffset.CUs[cc][0].get_top_DIE()
			print( "{}: {} ({})".format( ic, len(DieByOffset.CUs[cc][1]),
				td.get_full_path() ) )
