#include "testdata.h"
#include "test.Pointer.h"

static unsigned a = 4;

void ala()
{
	if( a > 2 )
		a++;
}

void bla( int b )
{
	if( b )
		a += b;
}

int cla( int c )
{
	if( c )
		a -= c;
	return a;
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
		if( init_by_pFunc1( ala ) )
			return -1;
		if( init_by_pFunc2( ala ) )
			return -3;
		if( init_by_pFunc3( bla ) )
			return -5;
		if( init_by_pFunc4( cla ) )
			return -4;
		if( init_by_tydefFunc( cla ) )
			return -7;
	}

	return 0;
}
