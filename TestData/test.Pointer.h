#pragma once

#include <stddef.h>

int init_by_pFunc( void (*)() );

typedef int (*f_pointer_type)(int);

int init_by_tydefFunc( f_pointer_type );
