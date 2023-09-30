#include <stdarg.h>
#include "testVarArgs.h"

unsigned var_sum( unsigned n, ... )
{
	unsigned result = 0;
	unsigned count;
	va_list args;
	va_start( args, n );

	for( count = 0; count < n; count++ )
	{
		result += va_arg( args, unsigned );
	}

	va_end(args );

	return result;
}

