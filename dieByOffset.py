# ########################################################################
# elf2MockCreator/dieByOffset
#
# Overall dictionary of DIE sorted by offset in CU
#
# Artur Lozinski (lozinski dot artur at gmail dor com)
# This code is the public domain
# ########################################################################
import sys

from elftools.dwarf.die import DIE
from elftools.dwarf.compileunit import CompileUnit
from mockProtos import *

class DieByOffset(object):
    """ Overall dictionary of DIE sorted by offset in CU. Main goal of the class is to
        provide simple method of getting DIE by its offset in the CU.

        There are two ways of receiving reference to DIE:
           * globally (by static method), by providing offset (an integer) and reference 
             to CU object (getDieInCu)
           * locally, referenced by the wrapper object of the CU class (type DieByOffset).
             This option need only one param, the offset itself (getDieInCu)

        By default, offset as a parameter of the above is relatively to the cu_offset. The
        option can be changed by the relOffset static method.

        In both cases the CU must be registered before use (by contructing DieByOffset
        object).

        Public methods:
            
            contructor (arg: reference to CU object)

            getDie, getDieInCu -- see desription above

            relOffset -- static method to change serching offset style, globally. If true
            offset is relatively to cu_offset, when False offset is global to whole ELF.
    """

    CUs = {}

    relativeOffset = True

    def __init__(self,cu):
        """ cu:
                reference to elftool/dwarf/CU object
        """
        self.cu = cu
        if cu.cu_offset not in DieByOffset.CUs:
            DieByOffset.CUs[cu.cu_offset] = (cu,self._addCu(cu))

    def _addCu(self,cu):
        cuByOffset = {}
        for dd in cu.iter_DIEs():
            cuByOffset[dd.offset] = dd
        return cuByOffset

    def getDie(self,offset,rel=None):
        """ offset:
                offset of DIE. If rel is:
                    True:  relative to cu_offset
                    False: global
                    None:  depends on static relativeOffset
        """
        return DieByOffset.getDieInCu(offset,self.cu,rel)

    def __getitem__(self,offset):
        self.getDie(offset)

    @staticmethod
    def getDieInCu(offset,cu,rel=None):
        """ offset:
                offset of DIE. If rel is:
                    True:  relative to cu_offset
                    False: global
                    None:  depends on static relativeOffset
            cu:
                reference to elftool/dwarf/CU object
        """
        if hasattr(cu,'cu_offset') and cu.cu_offset in DieByOffset.CUs: 
            if None == rel:
                rel = DieByOffset.relativeOffset
            if True == rel:
                offset += cu.cu_offset
            if offset in DieByOffset.CUs[cu.cu_offset][1]:
                return DieByOffset.CUs[cu.cu_offset][1][offset]

        return None

    @staticmethod
    def relOffset(ro):
        """ ro:
                new value of global relativeOffset:
                    True:  relative
                    False: global
        """
        DieByOffset.relativeOffset = ro

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
