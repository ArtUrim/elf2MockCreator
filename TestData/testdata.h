#pragma once

typedef struct {
	int a;
	char b;
	float * c;
} TestStruct;

int testVoidInt( int a );
void testIntPointer( char * str, int i );
TestStruct * testReturnPointer( int a, short b, long c );
float testPointerStruct( long a, TestStruct * b, int c );
int testStruct( TestStruct a );
