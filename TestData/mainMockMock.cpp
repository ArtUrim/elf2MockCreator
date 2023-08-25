#include "mainMockMock..h"

MainmockMock * p_mainMock;

extern "C" {

int testStruct( TestStruct a )
{
   return p_mainMock->testStruct( a );
}

float testPointerStruct( long int a, TestStruct * b, int c )
{
   return p_mainMock->testPointerStruct( a, b, c );
}

TestStruct * testReturnPointer( int a, short int b, long int c )
{
   return p_mainMock->testReturnPointer( a, b, c );
}

void testIntPointer( char * str, int i )
{
   p_mainMock->testIntPointer( str, i );
}

int testVoidInt( int a )
{
   return p_mainMock->testVoidInt( a );
}

}
