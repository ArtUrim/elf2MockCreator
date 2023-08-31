#include <stdlib.h>
#include "testdata.h"

void testIntPointer( char * str, int i )
{
	if( str[0] >= str[2] )
		str[1]= i;
}
