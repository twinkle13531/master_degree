#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

#include "qubo_io.h"

static void PRINT_USAGE(char *p)
{
	fprintf(stderr, "Usage:\t%s binary_sequence qubo [-s]\n", (p));
	fprintf(stderr, "Description: This program applies a variable assignment to a qubo formula and evaluate the energy of the formula.\n");
	fprintf(stderr, "Limitation: The coefficients of hamiltonians must be integers.\n");
        fprintf(stderr, "-s\tComputes Ising model whose variables take value 1 or -1. If this option is not specified, variables take value 1 or 0.\n");
}

//=================================================================================================
// main:

int main(int argc, char** argv)
{
	if (!(argc == 3 || argc == 4)) {
		PRINT_USAGE(argv[0]);
		return 1;
	}

	int size = 0;
	while(argv[1][size] == '0' || argv[1][size] == '1') {
		size++;
	}

	int* assign = (int*)malloc(sizeof(int)*(size+1));
	assert(assign != NULL);

	FILE* in = NULL;
	in = fopen(argv[2], "rb");
	if (in == NULL) {
		fprintf(stderr, "Could not open: %s\n", argv[2]);
		exit(1);
	}

	qubo_var_type vtype = QUBO_BOOL;
	if (argc == 4) {
		if (argv[3][0] == '-' && argv[3][1] == 's') {
			vtype = QUBO_BIMODAL; 
		} 
	}

	for (int i = 0; i < size; i++) {
		if (vtype == QUBO_BOOL) {
			assign[i+1] = (argv[1][i] == '0'?  0: 1);
		} else {
			assign[i+1] = (argv[1][i] == '0'? -1: 1);
		}
	}

	char comments[BUFSIZ];
	qubo_ptr Q = qubo_read(in, vtype, comments, BUFSIZ);
	fclose(in);

	double sum = 0;
	const int nMaxNodes = Q->nMaxNodes;
	assert(nMaxNodes == size);
	for (int i = 1; i <= nMaxNodes; i++) {
		double val = qubo_get(i,i,Q);
		sum = sum + val*assign[i];

		for (int j = i+1; j <= nMaxNodes; j++) {
			val = qubo_get(i,j,Q);
			sum = sum + val*assign[i]*assign[j]; 
		}
	}

	fprintf(stdout, "Energy: %d\n", (int)sum);

	qubo_destroy(Q);

	free(assign);

    return 0;
}

//=================================================================================================
// Static functions:


