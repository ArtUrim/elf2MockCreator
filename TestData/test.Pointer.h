#pragma once

#include <stddef.h>

int init_by_pFunc1( void (*)() );
int init_by_pFunc2( void (*p_func)(void) );
int init_by_pFunc3( void (*p_func)(int) );
int init_by_pFunc4( int (*p_func)(int) );

typedef int (*f_pointer_type)(int);

int init_by_tydefFunc( f_pointer_type );
