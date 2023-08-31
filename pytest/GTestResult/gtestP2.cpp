#include <gtest/gtest.h>

#include "mainMockMock.h"

extern "C" {
#include <stdio.h>
	void foo()
	{
		printf( "ole\n" );
	}
}


TEST(abc, xyz ) {
	p_mainMock = new MainmockMock;
	EXPECT_CALL( *p_mainMock, init_by_pFunc2 (foo) )
		.WillOnce( ::testing::Return(3) );

	EXPECT_EQ(init_by_pFunc2(foo), 3 );
	delete p_mainMock;
}
