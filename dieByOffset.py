import sys
from elftools.dwarf.die import DIE
from elftools.dwarf.compileunit import CompileUnit
from mockProtos import *

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
        return DieByOffset.getDieInCu(offset,self.cu)

    def __getitem__(self,offset):
        self.getDie(offset)

    @staticmethod
    def getDieInCu(offset,cu):
        if hasattr(cu,'cu_offset') and cu.cu_offset in DieByOffset.CUs: 
            offset += cu.cu_offset
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
            cu = DieByOffset.CUs[cc][0]
            td = DieByOffset.CUs[cc][0].get_top_DIE()
            print( "{}: 0x{:X} 0x{:X} 0x{:X} ({})".format( ic, len(DieByOffset.CUs[cc][1]),
                cc, td.offset, td.get_full_path() ) )
            for ctd in td.iter_children():
                if 'DW_AT_name' in ctd.attributes and 'DW_AT_type' in ctd.attributes:
                    print( "{} 0x{:X} 0x{:X}".format(
                        ctd.attributes['DW_AT_name'].value.decode('utf-8'),
                        ctd.offset,
                        ctd.attributes['DW_AT_type'].value+cc) )
                    ttd = DieByOffset.getDieInCu(ctd.attributes['DW_AT_type'].value,cu)
                    if ttd:
                        if 'DW_AT_name' in ttd.attributes:
                            print( "\t{}".format(
                                ttd.attributes['DW_AT_name'].value.decode('utf-8') ) )
                        elif 'DW_TAG_pointer_type' == ttd.tag:
                            print( "\t*" );
