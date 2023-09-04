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

def test_gTestS(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'testS.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestS.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestS.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0

def test_gTestIP(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'testIP.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestIP.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestIP.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0

def test_gTestVI(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'testVI.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestVI.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestVI.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0

def test_gTestRP(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'testRP.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestRP.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestRP.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0

def test_gTestPS(data_prep):
    currD = data_prep
    testDataDir = currD / '..' / 'TestData'
    pm = PrintMocks(  testDataDir / 'testPS.o', testDataDir / 'main.o' )
    assert pm
    writeMockHeader( 'mainMock', pm )
    hh = correctPathInMockH(currD)
    assert hh
    writeMockCpp( 'mainMock', pm )
    p = subprocess.run( ['make','clean','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestPS.o", "PATH":"/usr/bin"} )
    p = subprocess.run( ['make','-C',currD / 'GTestResult'], env={"GTEST_FILE": "gtestPS.o", "PATH":"/usr/bin"} )
    assert p.returncode == 0
