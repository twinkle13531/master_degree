#ifndef qubo_op_h
#define qubo_op_h

#include <stdio.h>
#include "qubo.h"

extern qubo_ptr qubo_booleanize(qubo_ptr Q, double* const_term);
extern qubo_ptr qubo_bimodalize(qubo_ptr Q, double* const_term);

#endif
