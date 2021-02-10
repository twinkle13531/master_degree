#include "qubo_op.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>


qubo_ptr qubo_booleanize(qubo_ptr Q, double* const_term)
{
	assert(const_term != NULL);
	assert(Q != NULL);

	if (Q->vtype != QUBO_BIMODAL) {
		fprintf(stderr, "Booleanizing Qubo of Boolean variables!\n");
		exit(1);
	}

	const int size = Q->nMaxNodes;
	qubo_ptr R = qubo_create(Q->dtype, QUBO_BOOL, size);

	*const_term = 0;

	for (int i = 1; i <= size; i++) {
		const double val = qubo_get(i,i,Q);
		qubo_set(i,i, 2.0*val, R);

		*const_term += -val;
	}

	for (int i = 1; i <= size; i++) {
		for (int j = i+1; j <= size; j++) {
			const double val = qubo_get(i,j,Q);

			qubo_set(i, j,  4.0*val, R);
			qubo_add(i, i, -2.0*val, R);
			qubo_add(j, j, -2.0*val, R);

			*const_term += val;
		}
	}

	return R;
}

qubo_ptr qubo_bimodalize(qubo_ptr Q, double* const_term)
{
	assert(const_term != NULL);
	assert(Q != NULL);

	if (Q->vtype != QUBO_BOOL) {
		fprintf(stderr, "Bimodalizing Qubo of Bimodal variables!\n");
		exit(1);
	}

	const int size = Q->nMaxNodes;
	qubo_ptr R = qubo_create(Q->dtype, QUBO_BIMODAL, size);

	*const_term = 0;

	for (int i = 1; i <= size; i++) {
		const double val = qubo_get(i,i,Q);
		qubo_set(i,i, 2.0*val, R);

		*const_term += 2.0*val;
	}

	for (int i = 1; i <= size; i++) {
		for (int j = i+1; j <= size; j++) {
			const double val = qubo_get(i,j,Q);

			qubo_set(i,j,val,R);
			qubo_add(i,i,val,R);
			qubo_add(j,j,val,R);

			*const_term += val;  
		}
	}

	return R;
}
