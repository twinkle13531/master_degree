#include "qubo.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

qubo_ptr qubo_create(qubo_data_type dt, qubo_var_type vt, int nMaxNodes)
{
	qubo_ptr q = (qubo_ptr)malloc(sizeof(qubo_t));
	if (q == NULL) {
		fprintf(stderr, "Memory Allocation Failed.\n");
		exit(1);
	}

	q->dtype     = dt;
	q->vtype     = vt;
	q->nMaxNodes = nMaxNodes;
	q->nNodes    = 0;
	q->nCouplers = 0;

	q->scale     = 1.0;
	q->constant  = 0.0;

	if (dt == QUBO_MATRIX) {
		double** M = (double**)malloc(sizeof(double*)*(nMaxNodes+1));
		if (M == NULL) {
			fprintf(stderr, "Memory Allocation Failed.\n");
			exit(1);
		}
		for (int i = 0; i <= nMaxNodes; i++) {
			M[i] = (double*)malloc(sizeof(double)*(nMaxNodes+1));
			if (M[i] == NULL) {
				fprintf(stderr, "Memory Allocation Failed.\n");
				exit(1);
			}
			for (int j = 0; j <= nMaxNodes; j++) {
				M[i][j] = 0;
			}
		}

		q->data = (void*)M;

	} else if (dt == QUBO_HASH) {
		q->data = (void*)ht2_create(0);
		if (q->data == NULL) {
			fprintf(stderr, "hash creation failed.\n");
			exit(1);
		}

	} else {
		assert(0);
	}


	return q;
}


void qubo_destroy(qubo_ptr q)
{
	assert(q != NULL);

	if (q->dtype == QUBO_MATRIX) {
		double **M = (double**)q->data;
		for (int i = 0; i <= q->nMaxNodes; i++) {
			free(M[i]);
		}
		free(M);

	} else if (q->dtype == QUBO_HASH) {
		ht2_destroy((my_hash2*)q->data);
	} else {
		assert(0);
	}

	free(q);
}

void qubo_clear(qubo_ptr q)
{
	assert(q != NULL);

	if (q->dtype == QUBO_MATRIX) {
		double **M = (double**)q->data;
		for (int i = 0; i <= q->nMaxNodes; i++) {
			for (int j = 0; j <= q->nMaxNodes; j++) {
				M[i][j] = 0;
			}
		}

	} else if (q->dtype == QUBO_HASH) {
		ht2_clear((my_hash2*)q->data);
	} else {
		assert(0);
	}

	q->nNodes = 0;
	q->nCouplers = 0;

	q->scale    = 1.0;
	q->constant = 0.0;
}

void qubo_set(int i, int j, double v, qubo_ptr q)
{
	assert(q != NULL);

	if (i == 0 && j == 0) {
		q->constant = v;
	}

	assert(0 < i && i <= q->nMaxNodes);
	assert(0 < j && j <= q->nMaxNodes);

	if (i > j) {
		int tmp = i;
		i = j;
		j = tmp;
	}

	if (q->dtype == QUBO_MATRIX) {
		double **M = (double**)q->data;
		if (M[i][j] == 0.0 && v != 0.0) {
			if (i == j) {
				q->nNodes++;
			} else {
				q->nCouplers++;
			}
		} else if (M[i][j] != 0.0 && v == 0.0) {
			if (i == j) {
				q->nNodes--;
				assert(q->nNodes >= 0);
			} else {
				q->nCouplers--;
				assert(q->nCouplers >= 0);
			}
		}
		M[i][j] = v;
	} else if (q->dtype == QUBO_HASH) {
		double w = 0.0;
		bool found = ht2_search(i, j, &w, (my_hash2*)q->data);
		if (found == true) {
			assert(w != 0.0);

			if (v == 0.0) {
				if (i == j) {
					q->nNodes--;
					assert(q->nNodes >= 0);
				} else {
					q->nCouplers--;
					assert(q->nCouplers >= 0);
				}

				ht2_remove(i,j,(my_hash2*)q->data);
			} else {
				ht2_set(i,j,v,(my_hash2*)q->data); // overwrite.
			}
		} else { // not found

			if (v != 0.0) {
				if (i == j) {
					q->nNodes++;
				} else {
					q->nCouplers++;
				}

				ht2_set(i,j,v,(my_hash2*)q->data); // newly add.
			}
		}
	
	} else {
		assert(0);
	}
}

double qubo_get(int i, int j, qubo_ptr q)
{
	assert(q != NULL);

	if (i == 0 & j == 0) {
		return q->constant;
	}

	assert(0 < i && i <= q->nMaxNodes);
	assert(0 < j && j <= q->nMaxNodes);

	double result = 0;

	if (i > j) {
		int tmp = i;
		i = j;
		j = tmp;
	}

	if (q->dtype == QUBO_MATRIX) {
		double** M = (double**)q->data;
		result = M[i][j];
	} else if (q->dtype == QUBO_HASH) {
		double w = 0.0;
		bool found = ht2_search(i, j, &w, (my_hash2*)q->data);
		if (found == true) assert(w != 0.0);

		result = w;
	} else {
		assert(0);
	}

	return result;
}

double qubo_mult(int i, int j, double v, qubo_ptr q)
{
	assert(q != NULL);

	if (i == 0 && j == 0) {
		q->constant *= v;
		return q->constant;
	}

	assert(0 < i && i <= q->nMaxNodes);
	assert(0 < j && j <= q->nMaxNodes);
	
	double result = 0.0;

	if (i > j) {
		int tmp = i;
		i = j;
		j = tmp;
	}

	if (v == 0.0) {
		fprintf(stderr, "Multiplier must be nonzero.");
		exit(1);
	}

	if (q->dtype == QUBO_MATRIX) {
		double** M = (double**)q->data;
		M[i][j] *= v;
		result = M[i][j];
	} else if (q->dtype == QUBO_HASH) {
		double w = 0.0;
		bool found = ht2_search(i, j, &w, (my_hash2*)q->data);
		if (found == true) {
			assert(w != 0.0);
			w = v*w;
			ht2_set(i, j, w, (my_hash2*)q->data);  // overwite.
		}

		result = w;
	} else {
		assert(0);
	}

	return result;
}

double qubo_add(int i, int j, double v, qubo_ptr q)
{
	assert(q != NULL);

	if (i == 0 && j == 0) {
		q->constant += v;
		return q->constant;
	}
	
	assert(0 < i && i <= q->nMaxNodes);
	assert(0 < j && j <= q->nMaxNodes);
	
	double result = 0.0;

	if (i > j) {
		int tmp = i;
		i = j;
		j = tmp;
	}

	if (q->dtype == QUBO_MATRIX) {
		double** M = (double**)q->data;
		result = M[i][j] + v;
		if (M[i][j] != 0.0 && result == 0.0) {
			if (i == j) {
				q->nNodes--;
				assert(q->nNodes >= 0);
			} else {
				q->nCouplers--;
				assert(q->nCouplers >= 0);
			}
		} else if (M[i][j] == 0.0 && result != 0.0) {
			if (i == j) {
				q->nNodes++;
			} else {
				q->nCouplers++;
			}
		}
		M[i][j] = result;
	} else if (q->dtype == QUBO_HASH) {
		double w = 0.0;
		bool found = ht2_search(i, j, &w, (my_hash2*)q->data);
		result = v+w;
		if (found == true && result != 0.0) {
			assert(w != 0.0);
			ht2_set(i, j, result, (my_hash2*)q->data); // overwrite
		} else if (found == true && result == 0.0){
			if (i == j) {
				q->nNodes--;
				assert(q->nNodes >= 0);
			} else {
				q->nCouplers--;
				assert(q->nCouplers >= 0);
			}

			ht2_remove(i,j,(my_hash2*)q->data); // just remove.
		} else if (found == false && v != 0.0) {
			assert(result == v);
			if (i == j) {
				q->nNodes++;
			} else {
				q->nCouplers++;
			}

			ht2_set(i,j,result,(my_hash2*)q->data); // newly add
		}
	} else {
		assert(0);
	}

	return result;
}

void qubo_setScale(double v, qubo_ptr q)
{
	q->scale = v;
}

double qubo_getScale(qubo_ptr q)
{
	return q->scale;
}

