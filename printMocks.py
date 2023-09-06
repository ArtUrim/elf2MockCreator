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
from dieByOffset import DieByOffset

import argparse
import os

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
        DieByOffset.CUs = {}
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


def writeMockHeader( fname, printMocks ):
    className = fname.capitalize() + 'Mock'
    className = className.replace('.','_')
    pointerName = 'p_' + fname
    pointerName = pointerName.replace('.','_')
    fname += 'Mock.h'

    wrtStr = """#pragma once

#include <gmock/gmock.h>
extern "C" {
#include "!!!! PLACE FOR YOUR HEADER(S) !!!"
}

class """

    wrtStr += className
    wrtStr += '{\n'
    with open( fname, 'wt' ) as fh:
        fh.write( wrtStr )
        fh.write( "   public:\n" )
        fh.write( "      virtual ~" + className + "() {}\n" )
        for mp in printMocks.createProtos():
            vmp = mp.mockData()
            ostr  = "      MOCK_METHOD" + str(len(vmp.args)) + '( ' + vmp.name + ', '
            ostr += vmp.retv + '(' 
            for i,vv in enumerate(vmp.args):
                if i > 0:
                    ostr += ', '
                ostr += vv[1]
            ostr += ') )'
            fh.write( ostr + ";\n")
        fh.write( "};\n\n\n" )
        fh.write( "extern " + className + " * " + pointerName + ';\n' )

def writeMockCpp( fname, printMocks ):
    className = fname.capitalize() + 'Mock'
    className = className.replace('.','_')
    pointerName = 'p_' + fname
    pointerName = pointerName.replace('.','_')
    fname += 'Mock.'

    with open( fname + 'cpp', 'wt' ) as fh:
        fh.write( "#include \"" + fname + 'h"\n\n' )
        fh.write( className + " * " + pointerName + ';\n\n' )
        fh.write( 'extern "C" {\n\n' ) 
        for mp in printMocks.createProtos():
            vmp = mp.mockData()
            fh.write( vmp.retv + " " + vmp.name + '( ' )
            for i,vv in enumerate(vmp.args):
                if i > 0:
                    fh.write( ', ' )
                (newStr,nocc) = re.subn( '\(\*\)', '(*' + vv[0] + ')',
                                        vv[1] )
                if nocc:
                    fh.write(newStr)
                else:
                    fh.write( vv[1] + ' ' + vv[0] )
            fh.write( ' )\n{\n   ' )
            if 'void' != vmp.retv:
                fh.write( 'return ' )
            fh.write( pointerName + '->' + vmp.name + '( ' )
            for i,vv in enumerate(vmp.args):
                if i > 0:
                    fh.write( ', ' )
                fh.write( vv[0] )
            fh.write( ' );\n}\n\n' )
        fh.write( '}\n' ) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument( 'input', nargs='+', help=" 2 inputs are: 1) elf file for whole app 2) obj for the source to mock" )
    parser.add_argument( '-o', action='store_true', help="store to h and cpp mock files" )
    args = parser.parse_args()
    if len(args.input) < 2:
        args.print_help()
    else:
        printMocks = PrintMocks(args.input[0], args.input[1] )
        if args.o:

            mockFileBaseName  = os.path.splitext(os.path.basename(args.input[1]))[0]
            mockFileBaseName += 'Mock'
            writeMockHeader( mockFileBaseName, printMocks )
            writeMockCpp( mockFileBaseName, printMocks )

        else:
            print( "Files:" )
            co = 1
            fic = printMocks.getFileIndex()
            for ff in fic:
                print( "{}:{}".format(co,ff) )
                co += 1
            print( "" )
            print( str(printMocks) )
            print( '\n' )
            for mp in printMocks.createProtos():
                print( str(mp) )
                vmp = mp.mockData()
                if vmp:
                    print( "|{}|{}|".format( vmp.retv, vmp.name ) )
                    for avmp in vmp.args:
                        print( "  {}:{}".format( *avmp ) )

