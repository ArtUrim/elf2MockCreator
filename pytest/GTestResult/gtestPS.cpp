#include <gtest/gtest.h>

#include "mainMockMock.h"

TEST(abc, xyz ) {
	p_mainMock = new MainmockMock;
	float ff = 3.0f;
	TestStruct ts = {1,2,&ff};

	EXPECT_CALL( *p_mainMock, testPointerStruct( 7, &ts, 4 ) )
		.WillOnce( ::testing::Return(2.3f) );

	EXPECT_FLOAT_EQ( testPointerStruct( 7, &ts, 4 ), 2.3f );

	delete p_mainMock;
}
