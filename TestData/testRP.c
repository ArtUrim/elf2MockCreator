#include <stdlib.h>
#include "testdata.h"

TestStruct * testReturnPointer( int a, short b, long c )
{
	TestStruct * pStr = (TestStruct *)malloc( sizeof(TestStruct) );
	pStr->a = a;
	pStr->b = (char)b;
	pStr->c = (float *)c;
	return pStr;
}
