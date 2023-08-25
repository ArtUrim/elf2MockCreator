#include "test.Pointer.h"

int init_by_pFunc( void (*p_func)() )
{
	if( p_func != NULL )
	{
		p_func();
		return 0;
	}
	return -1;
}
