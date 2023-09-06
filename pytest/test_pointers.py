#!/usr/bin/env python3
# coding: utf-8

import subprocess
import os
import pytest
from pathlib import Path
import re

from printMocks import PrintMocks, writeMockHeader, writeMockCpp

@pytest.fixture
def currDir():
    currD = Path.cwd()
    if currD.name == 'elf2MockCreator':
        currD = currD / 'pytest'
    return currD

@pytest.fixture
def data_prep(currDir):
    if not data_prep.is_make_done:
        testDataPath = currDir / '..' / 'TestData'

        p=subprocess.run( ['make','-C',testDataPath], env={'PATH':'/usr/bin'} )
        data_prep.is_make_done = True
    return currDir

data_prep.is_make_done = False

def correctPathInMockH(currDir):
    hf = currDir / '..' / 'mainMockMock.h'
    l2 = []
    for l in hf.read_text().split('\n'):
        l2.append( re.sub('!.*!', 'testdata.h', l  ) )
    hf.write_text('\n'.join(l2))
    return hf

def test_gTestPointerII(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'test.PointerII.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestP4.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestP4.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0

def test_gTestPointerV(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'test.PointerV.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestP1.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestP1.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0

def test_gTestPointerVV(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'test.PointerVV.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestP2.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestP2.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0

def test_gTestPointerVI(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'test.PointerVI.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestP3.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestP3.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0

def test_gTestPointerTypef(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'test.PointerTypedef.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'],
                       env={"GTEST_FILE": "gtestPTypedef.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'],
                       env={"GTEST_FILE": "gtestPTypedef.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0
