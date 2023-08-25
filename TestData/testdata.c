#include <stdlib.h>
#include "testdata.h"

int testVoidInt( int a )
{
	if( a > 0 )
		return 5;
	return 0;
}

void testIntPointer( char * str, int i )
{
	if( str[0] >= str[2] )
		str[1]= i;
}

TestStruct * testReturnPointer( int a, short b, long c )
{
	TestStruct * pStr = (TestStruct *)malloc( sizeof(TestStruct) );
	pStr->a = a;
	pStr->b = (char)b;
	pStr->c = (float *)c;
	return pStr;
}

float testPointerStruct( long a, TestStruct * b, int c )
{
	if( NULL != b )
		return (float)a;
	return (float)c;
}

int testStruct( TestStruct a )
{
	return a.a;
}
