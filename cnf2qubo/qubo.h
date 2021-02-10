#ifndef qubo_h
#define qubo_h

#include <stdio.h>
#include "my_hash2.h"

typedef enum qubo_data_type_TAG {
	QUBO_MATRIX,
	QUBO_HASH
} qubo_data_type;

typedef enum qubo_var_type_TAG {
	QUBO_BIMODAL,
	QUBO_BOOL
} qubo_var_type;

typedef struct qubo_TAG {
	qubo_data_type	dtype;
	qubo_var_type   vtype;
	void*		data;
	int 		nMaxNodes;
	int 		nNodes;
	int 		nCouplers;
	double		scale;		//
	double		constant;	// set and get this by specifying i=0 and j=0, which does not increase nor decrease nMaxNodes, nNodes, and nCouplers.
} qubo_t;

typedef qubo_t* qubo_ptr;

extern qubo_ptr qubo_create(qubo_data_type dt, qubo_var_type vt, int nMaxNodes);
extern void qubo_destroy(qubo_ptr q);
extern void qubo_clear(qubo_ptr q);
extern void qubo_set(int i, int j, double v, qubo_ptr q);
extern double qubo_get(int i, int j, qubo_ptr q);
extern double qubo_mult(int i, int j, double v, qubo_ptr q);
extern double qubo_add(int i, int j, double v, qubo_ptr q);

extern void qubo_setScale(double v, qubo_ptr q);
extern double qubo_getScale(qubo_ptr q);

#endif
