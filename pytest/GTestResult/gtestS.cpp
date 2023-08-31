#include <gtest/gtest.h>

#include "mainMockMock.h"

TEST(abc, xyz ) {
	p_mainMock = new MainmockMock;
	float ff = 3.0f;
	TestStruct ts = {1,2,&ff};

	EXPECT_CALL( *p_mainMock, testStruct( ::testing::_ ) )
		.WillOnce( ::testing::Return(2) );

	EXPECT_EQ( testStruct( ts ), 2 );

	delete p_mainMock;
}
