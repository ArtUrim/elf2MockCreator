#include "depMock.h"

DepMock * p_depMock;

extern "C" {
int depfunc( int a )
{
	return p_depMock->depfunc( a );
}
}
