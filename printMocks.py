##################################
# elf2MockCreator/printMocks
#
# An example of tool to create mocks. Print defs all undefined symbols.
#
# Artur Lozinski (lozinski dot artur at gmail dor com)
# This code is the public domain
# #######################################
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

    def createProtos(self):
        self.mocksProto = []
        for und in self.undefDies:
            self.mocksProto.append( MockProto.findMockType( self.undefDies[und][1] ) )
        return self.mocksProto

    def getFileIndex(self):
        self.fileIndex = FileIndexCu( self.objFileName )
        self.filesInCu = self.fileIndex.filesIn()
        if len(self.filesInCu) != 1:
            print( "Unexpected number of CU: {}".format( len(self.filesInCu) ) )
        return self.filesInCu.popitem()[1]

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
        fic = printMocks.getFileIndex()
        print( "Files:" )
        co = 1
        for ff in fic:
            print( "{}:{}".format(co,ff) )
            co += 1
        print( "" )
        print( str(printMocks) )
        print( '\n' )
        for mp in printMocks.createProtos():
            print( str(mp) )

