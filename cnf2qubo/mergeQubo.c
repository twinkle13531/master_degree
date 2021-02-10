#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

#include "qubo_io.h"

//=================================================================================================
// Constants:

//=================================================================================================
// Static function prototypes:


static void PRINT_USAGE(char *p)
{
	fprintf(stderr, "Usage:\t%s qubo1 qubo2 ...\n", (p));
	fprintf(stderr, "Description: This program simply does the summation over all given hamiltonians.\n");
	fprintf(stderr, "Limitation: The coefficients of hamiltonians must be integers.\n");
}

//=================================================================================================
// main:

int main(int argc, char** argv)
{
	if (argc <= 0) {
		PRINT_USAGE(argv[0]);
		return 1;
	}

	qubo_ptr Accum = qubo_create(QUBO_HASH, QUBO_BIMODAL, 1);

	for (int i = 1; i < argc; i++) {
		FILE* in = fopen(argv[i], "rb");
		if (in == NULL) {
			fprintf(stderr, "Could not open: %s\n", argv[i]);
			exit(1);
		}

		char comments[BUFSIZ];
		qubo_ptr Q = qubo_read(in, QUBO_BIMODAL, comments, BUFSIZ);
		fclose(in);

		if (Accum->nMaxNodes < Q->nMaxNodes) {
			qubo_ptr tmp = Accum;
			Accum = Q;
			Q = tmp;
		}

		for (int i = 1; i <= Q->nMaxNodes; i++) {
			for (int j = i; j <= Q->nMaxNodes; j++) {
				double val = qubo_get(i,j,Q);
				qubo_add(i,j,val,Accum);
			}
		}

		qubo_destroy(Q);
	}

	qubo_write(stdout, Accum);
	qubo_destroy(Accum);

    return 0;
}

//=================================================================================================
// Static functions:


