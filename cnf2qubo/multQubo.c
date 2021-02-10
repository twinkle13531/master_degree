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
	fprintf(stderr, "Usage:\t%s k qubo\n", (p));
	fprintf(stderr, "Description: This program simply multiplies a given hamiltonian by k.\n");
	fprintf(stderr, "Limitation: The coefficients of hamiltonians must be integers.\n");
}

//=================================================================================================
// main:

int main(int argc, char** argv)
{
	if (argc != 3) {
		PRINT_USAGE(argv[0]);
		return 1;
	}

	{
		const int k = atoi(argv[1]);
		if (k <= 0) {
			fprintf(stderr, "Multiplier must be a positive integer.\n");
			exit(1);
		}
		FILE* in = fopen(argv[2], "rb");
		if (in == NULL) {
			fprintf(stderr, "Could not open: %s\n", argv[2]);
			exit(1);
		}

		char comments[BUFSIZ];
		qubo_ptr Q = qubo_read(in, QUBO_BIMODAL, comments, BUFSIZ);
		fclose(in);

		for (int i = 1; i <= Q->nMaxNodes; i++) {
			for (int j = i; j <= Q->nMaxNodes; j++) {
				double val = qubo_get(i,j,Q);
				qubo_set(i,j,k*val,Q);
			}
		}

		qubo_write(stdout, Q);
		qubo_destroy(Q);
	}

    return 0;
}

//=================================================================================================
// Static functions:


