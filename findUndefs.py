# ########################################################################
# elf2MockCreator/findUndefs
#
# Find undefined symbols reffered in the elf object
#
# Artur Lozinski (lozinski dot artur at gmail dor com)
# This code is the public domain
# ########################################################################
import sys

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

class FindUndefs(object):
    """ Find undefined symbols reffered in the elf object. Object file after
        compilation, but before linking includes information about all symbols which are
        referenced in the compiled code, but not defined in the compilation unit. The class
        is defined for searching for the undefs likt this. 

        Public methods:
            findUndefs -- returns a list of all found undefined objects
    """

    def __init__(self,fname):
        """ fname:
                file name of object file 
        """
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

    def findUndef(self):
        """ returns a list of strings """
        self.undefs = []
        for ss in self.secSymbols:
            self.undefs.extend( self.__findUndefInSec(ss) )
        return self.undefs

    def __findUndefInSec(self,sec):
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
