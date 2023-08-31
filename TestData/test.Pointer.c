#include "test.Pointer.h"

int init_by_pFunc1( void (*p_func)() )
{
	if( p_func != NULL )
	{
		p_func();
		return 0;
	}
	return -1;
}

int init_by_pFunc2( void (*p_func)(void) )
{
	if( p_func != NULL )
	{
		p_func();
		return 0;
	}
	return -1;
}

int init_by_pFunc3( void (*p_func)(int) )
{
	if( p_func != NULL )
	{
		p_func(42);
		return 0;
	}
	return -1;
}

int init_by_pFunc4( int (*p_func)(int) )
{
	if( p_func != NULL )
	{
		p_func(13);
		return 0;
	}
	return -1;
}
