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
	EXPECT_CALL( *p_mainMock, init_by_pFunc1 (foo) )
		.WillOnce( ::testing::Return(1) );

	EXPECT_EQ(init_by_pFunc1(foo), 2 );
	delete p_mainMock;
}
