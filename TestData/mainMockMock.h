#pragma once

#include <gmock/gmock.h>
extern "C" {
#include "!!!! PLACE FOR YOUR HEADER(S) !!!"
}

class MainmockMock{
   public:
      virtual ~MainmockMock() {}
      MOCK_METHOD1( testStruct, int(TestStruct) );
      MOCK_METHOD3( testPointerStruct, float(long int, TestStruct *, int) );
      MOCK_METHOD3( testReturnPointer, TestStruct *(int, short int, long int) );
      MOCK_METHOD2( testIntPointer, void(char *, int) );
      MOCK_METHOD1( testVoidInt, int(int) );
};


extern MainmockMock * p_mainMock;
