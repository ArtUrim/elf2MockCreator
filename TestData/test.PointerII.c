#include "testdata.h"

int init_by_pFunc4( int (*p_func)(int) )
{
	if( p_func != NULL )
	{
		p_func(13);
		return 0;
	}
	return -1;
}
