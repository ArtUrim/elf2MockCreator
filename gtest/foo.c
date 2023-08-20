#include "dep.h"
#include <stdio.h>

void foo()
{
	int i = depfunc( 14 );
	printf( "result is %d\n", i );

}
