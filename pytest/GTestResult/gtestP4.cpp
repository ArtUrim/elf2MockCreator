#include <gtest/gtest.h>

#include "mainMockMock.h"

extern "C" {
#include <stdio.h>
	int foo( int a )
	{
		printf( "ole %d\n", a );
		return a;
	}
}


TEST(abc, xyz ) {
	p_mainMock = new MainmockMock;
	EXPECT_CALL( *p_mainMock, init_by_pFunc4 (foo) )
		.WillOnce( ::testing::Return(1) );

	EXPECT_EQ(init_by_pFunc4(foo), 1 );
	delete p_mainMock;
}
