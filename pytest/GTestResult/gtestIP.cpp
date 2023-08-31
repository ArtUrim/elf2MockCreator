#include <gtest/gtest.h>
#include <string.h>

#include "mainMockMock.h"

TEST(abc, xyz ) {
	p_mainMock = new MainmockMock;
	int a = 7;

	EXPECT_CALL( *p_mainMock, testIntPointer(::testing::_,a) ).WillOnce( 
			::testing::Return() );

	std::string vv("ole");
	testIntPointer( const_cast<char *>(vv.c_str()), a );
	delete p_mainMock;
}
