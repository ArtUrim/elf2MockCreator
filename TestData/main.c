#include "testdata.h"
#include "test.Pointer.h"

static unsigned a = 4;

void ala()
{
	if( a > 2 )
		a++;
}

int main() 
{
	if( testVoidInt(7) > 2 ) {
		TestStruct *pStr = testReturnPointer( 2, 7, 13 );
		testIntPointer( (char *)pStr, 77 );
		float vv =testPointerStruct( 6, pStr, 11 );
		pStr->b = vv;
		if( 4 > testStruct( *pStr ) )
			return -2;
	} else {
		init_by_pFunc( ala );
		return -1;
	}

	return 0;
}
