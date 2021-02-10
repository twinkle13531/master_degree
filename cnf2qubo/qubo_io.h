#ifndef qubo_io_h
#define qubo_io_h

#include <stdio.h>
#include "qubo.h"


extern qubo_ptr qubo_read(FILE *from, qubo_var_type type, char comments[], int total_length_of_comments);
extern void qubo_write(FILE* to, qubo_ptr Q);

#endif
