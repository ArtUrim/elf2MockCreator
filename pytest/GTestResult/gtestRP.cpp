#include <gtest/gtest.h>

#include "mainMockMock.h"

TEST(abc, xyz ) {
	p_mainMock = new MainmockMock;
	float ff = 3.0f;
	TestStruct ts = {1,2,&ff};

	EXPECT_CALL( *p_mainMock, testReturnPointer(1,2,3) ).WillOnce( 
			::testing::Return( &ts ) );

	testReturnPointer(1,2,3);
	delete p_mainMock;
}
