#include <stdlib.h>
#include "testdata.h"

float testPointerStruct( long a, TestStruct * b, int c )
{
	if( NULL != b )
		return (float)a;
	return (float)c;
}
