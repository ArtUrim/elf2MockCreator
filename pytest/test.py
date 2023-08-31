#!/usr/bin/env python3
# coding: utf-8

import subprocess
import os

testDataPath = os.path.dirname(os.environ['PWD'])
testDataPath += '/TestData'

p=subprocess.run( ['make','-C',testDataPath], env={'PATH':'/usr/bin'} )

p = subprocess.run( ['make','clean','-C','GTestResult'], env={"GTEST_FILE": "gtestS.o", "PATH":"/usr/bin"} )
p = subprocess.run( ['make','-C','GTestResult'], env={"GTEST_FILE": "gtestS.o", "PATH":"/usr/bin"} )
p.returncode
