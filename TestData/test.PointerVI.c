#include "test.Pointer.h"

int init_by_pFunc3( void (*p_func)(int) )
{
	if( p_func != NULL )
	{
		p_func(42);
		return 0;
	}
	return -1;
}
