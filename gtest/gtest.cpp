#include <gtest/gtest.h>

#include "depMock.h"

extern "C" {
void foo();
}

TEST(abc, xyz ) {
	p_depMock = new DepMock;
	EXPECT_CALL( *p_depMock, depfunc(14) ).WillOnce( ::testing::Return(1) );

	foo();
	delete p_depMock;
}
