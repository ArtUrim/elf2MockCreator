##################################
# elf2MockCreator/locateUndef
#
# Locate symbol in the compilation unit
#
# Artur Lozinski (lozinski dot artur at gmail dor com)
# This code is the public domain
# #######################################
import sys

from elftools.elf.elffile import ELFFile
from elftools.common.py3compat import itervalues

class LocateUndef(object):
    """ Locate symbol in the compilation unit. For each symbol (by a name string) returns an
        object of the pyelftools/dwarf/die type (with includes reference to the compilation
        unit as an attribute.

        Public methods:

            findDies -- for the list of names (of the symbols) prepares the list of
                references to DIE
                
            getDies -- return the list of found DIEs
    """

    def __init__(self,fname):
        """ fname:
                file name of object file 
        """
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

    def findDies( self, namesList ):
        """ namesList -- list of symbol names (strings). Each symbols is expected to be once
            in the nameList"""
        for cu in self.dwarfinfo.iter_CUs():
            for die in cu.iter_DIEs():
                if die.is_null():
                    continue

                if 'DW_AT_name' in die.attributes:
                    name = die.attributes['DW_AT_name'].value.decode('ascii')
                    if name in namesList:
                        self.dies[name] = (cu,die)
                        namesList.remove(name) # not sure whether it works
                                               # have to check false definitions 
                        if len(namesList) < 1:
                            return

    def getDies(self):
        """ returns list of DIEs object (its name is DIE.attributes['DW_AT_name'] """
        return self.dies

if __name__ == '__main__':
    if len(sys.argv) > 2:
        try:
            lu = LocateUndef( sys.argv[1] )
            fList = []
            if '-f' == sys.argv[2]:
                if len(sys.argv) > 3:
                    with open( sys.argv[3], "rt" ) as fh:
                        for line in fh:
                            names = line.split()
                            if len(names) > 1:
                                fList.append(names[1])
            else:
                fList = sys.argv[2:]

            if fList:
                lu.findDies( fList )
                ddies = lu.getDies()
                for idx, kdie in enumerate(ddies.keys()):
                    print( "{}: {}\t{}".format(idx,kdie,ddies[kdie][0].get_top_DIE().get_full_path()) )
        except IOError as ioe:
            print( "Cannot open file {}".format( sys.argv[1] ) )
    else:
        print( "No input file" )
