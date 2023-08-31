#include "testdata.h"

int init_by_pFunc2( void (*p_func)(void) )
{
	if( p_func != NULL )
	{
		p_func();
		return 0;
	}
	return -1;
}
