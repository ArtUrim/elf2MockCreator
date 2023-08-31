#include "test.Pointer.h"

int init_by_tydefFunc( f_pointer_type p_func )
{
	if( p_func != NULL )
	{
		if( p_func(13) > 0 )
			return 1;
		return 0;
	}
	return -1;
}
