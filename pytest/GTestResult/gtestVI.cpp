#include <gtest/gtest.h>

#include "mainMockMock.h"

TEST(abc, xyz ) {
	p_mainMock = new MainmockMock;
	int a = 7;

	EXPECT_CALL( *p_mainMock, testVoidInt(a) ).WillOnce( ::testing::Return(1) );

	EXPECT_EQ( testVoidInt(a), 1 );
	delete p_mainMock;
}
