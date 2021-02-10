#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

#include "qubo_io.h"
#include "qubo_op.h"

//=================================================================================================
// Constants:
static const char comment_symb = 'c';
static const char program_symb = 'p';

//=================================================================================================
// Static function prototypes:


static void PRINT_USAGE(char *p)
{
	fprintf(stderr, "Usage:\t%s qubo\n", (p));
	fprintf(stderr, "Description: This program convert variables that take 1 or 0 into those that take 1 or -1.\n");
	fprintf(stderr, "Limitation: The coefficients of hamiltonians must be integers.\n");
	fprintf(stderr, "Note: This program does not check if input hamiltonian's variables take 1 or 0.\n");
}

//=================================================================================================
// main:

int main(int argc, char** argv)
{
	if (argc =! 1) {
		PRINT_USAGE(argv[0]);
		return 1;
	}

	FILE* in = fopen(argv[1], "rb");
	if (in == NULL) {
		fprintf(stderr, "Could not open: %s\n", argv[1]);
		exit(1);
	}

	char comments[BUFSIZ];
	qubo_ptr Q = qubo_read(in, QUBO_BOOL, comments, BUFSIZ);
	fclose(in);

	double const_term = 0;
	qubo_ptr R = qubo_bimodalize(Q, &const_term);

	fprintf(stdout, "%c ----------------------- Comments before bimodalizing start from here:\n", comment_symb);
	char* ptr = &(comments[0]);
	while(*ptr != '\0') {
		fprintf(stdout, "%c", *ptr);
		ptr++;
	}
	fprintf(stdout, "%c ----------------------- Comments before bimodalizing end.\n", comment_symb);
	fprintf(stdout, "%c minimum energy in bimodal case = minimum energy in boolean case times 4 - (%d) \n", comment_symb, (int)const_term);
	qubo_write(stdout, R);

	qubo_destroy(R);
	qubo_destroy(Q);

    return 0;
}

//=================================================================================================
// Static functions:


