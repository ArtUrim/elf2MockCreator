#pragma once

#include <gmock/gmock.h>
extern "C" {
#include "dep.h"
}

class DepMock {
	public:
		virtual ~DepMock() {}
		MOCK_METHOD1( depfunc, int(int) );
};


extern DepMock * p_depMock;
