import sys

from findUndefs import FindUndefs
from locateUndef import LocateUndef
from mockProtos import *
from printFileIndexCu import FileIndexCu

class PrintMocks(object):

    def __init__(self,elfFileName,objFileName):
        self.elfFileName = elfFileName
        self.objFileName = objFileName

        self.undefs = FindUndefs( objFileName ).findUndef()

        self.locateUndef = LocateUndef( elfFileName )
        self.locateUndef.findDies( self.undefs )
        self.undefDies = self.locateUndef.getDies()

    def __str__(self):
        strPrintMocks = 'Undefs:\n'
        for idx, und in enumerate(self.undefs):
            strPrintMocks += "  {}: {}".format(idx,und) + '\n'
        strPrintMocks += '\nLocated:\n'
        for idx, und in enumerate(self.undefDies.keys()):
            strPrintMocks += "  {}: {}\t{}".format( idx, und,
                self.undefDies[und][0].get_top_DIE().get_full_path()) + '\n'

        return strPrintMocks + '\n'

    @staticmethod
    def printHelp():
        print( """printMocks  --  tools for creation mocks from source code
                  
   2 inputs are:
     1) elf file for whole app
     2) obj for the source to mock""" )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        PrintMocks.printHelp()
    else:
        printMocks = PrintMocks(sys.argv[1], sys.argv[2] )
        print( str(printMocks) )

