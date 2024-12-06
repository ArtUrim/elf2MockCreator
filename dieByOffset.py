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

from typing import Dict, Optional, Tuple
from elftools.dwarf.die import DIE
from elftools.dwarf.compileunit import CompileUnit

class DieByOffset:
    """Dictionary of DIE (Debug Information Entry) sorted by offset in Compilation Unit.
    
    This class provides methods to access DIEs by their offset within a compilation unit.
    DIEs can be accessed either globally via static methods or locally via instance methods.
    
    Attributes:
        CUs: Dict mapping CU offsets to tuples of (CompileUnit, Dict[int, DIE])
        relativeOffset: Boolean flag indicating if offsets are relative to CU
    """

    CUs: Dict[int, Tuple[CompileUnit, Dict[int, DIE]]] = {}
    relativeOffset: bool = True

    def __init__(self, cu: CompileUnit) -> None:
        """Initialize DieByOffset with a compilation unit.
        
        Args:
            cu: CompileUnit object to index DIEs from
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

    def _addCu(self, cu: CompileUnit) -> Dict[int, DIE]:
        """Index all DIEs in a compilation unit by their offset.
        
        Args:
            cu: CompileUnit object to index DIEs from
            
        Returns:
            Dictionary mapping DIE offsets to DIE objects
        """
        return {die.offset: die for die in cu.iter_DIEs()}

    def getDie(self, offset: int, rel: Optional[bool] = None) -> Optional[DIE]:
        """Get DIE by offset in current compilation unit.
        
        Args:
            offset: Offset of DIE to retrieve
            rel: If True, offset is relative to CU offset
                 If False, offset is global
                 If None, uses class relativeOffset setting
        
        Returns:
            DIE object if found, None otherwise
        """
        return DieByOffset.getDieInCu(offset, self.cu, rel)

    def __getitem__(self,offset):
        self.getDie(offset)

    @staticmethod
    def getDieInCu(offset: int, cu: CompileUnit, rel: Optional[bool] = None) -> Optional[DIE]:
        """Get DIE by offset in specified compilation unit.
        
        Args:
            offset: Offset of DIE to retrieve
            cu: CompileUnit object to search in
            rel: If True, offset is relative to CU offset
                 If False, offset is global
                 If None, uses class relativeOffset setting
        
        Returns:
            DIE object if found, None otherwise
        """
        if not hasattr(cu, 'cu_offset') or cu.cu_offset not in DieByOffset.CUs:
            return None
            
        rel = DieByOffset.relativeOffset if rel is None else rel
        search_offset = offset + cu.cu_offset if rel else offset
        
        return DieByOffset.CUs[cu.cu_offset][1].get(search_offset)

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
