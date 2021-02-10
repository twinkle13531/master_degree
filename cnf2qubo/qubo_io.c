#include "qubo_io.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

static const char comment_symb = 'c';
static const char program_symb = 'p';

static void skipWhitespace(char** in)
{
   while ((**in >= 9 && **in <= 13) || **in == 32)
        (*in)++;
}

qubo_ptr qubo_read(FILE *from, qubo_var_type type, char comments[], int total_length_of_comments)
{
	char buf[BUFSIZ];
	bool isProblemlineRead = false;

	qubo_ptr Q = NULL;

	int nMaxNodes = 0;
	int nNodes = 0;
	int nCouplers = 0;
	int NofReadEntries = 0;

	fseek(from, 0L, SEEK_SET);
	while(fgets(buf, BUFSIZ, from) != NULL) {
		char* str = buf;
		skipWhitespace(&str);
		if (str[0] == 'p') {
			int res = sscanf(str, "p qubo 0 %d %d %d", &nMaxNodes, &nNodes, &nCouplers);
			if (res == EOF || res != 3) {
				fprintf(stderr, "Could not read the problem line: %s\n", str);
				exit(1);
			}
 			isProblemlineRead = true;

			assert(Q == NULL);
			Q = qubo_create(QUBO_HASH, type, nMaxNodes);

		} else if (str[0] == 'c') {
			while(*str != '\0' && total_length_of_comments > 1) {
				*comments=*str;
				comments++;
				str++;
				total_length_of_comments--;
			}
			if (total_length_of_comments == 1) {
				*comments = '\0'; // just ignore the remaining comments if the limit exceeds.
				total_length_of_comments--;
			}
			
			continue;
		} else {

			if (!isProblemlineRead) {
				fprintf(stderr, "Could not find a problem line before the data lines.\n");
				exit(1);
			}

			if (Q == NULL) {
				fprintf(stderr, "Qubo data was read before creating qubo data structure.\n");
				exit(1);
			}

			{
				skipWhitespace(&str);
				int i, j, v;
				int res = sscanf(str, "%d %d %d", &i, &j, &v);
				if (res == EOF || res != 3) {
					fprintf(stderr, "Could not read the data line: %s\n", str);
					exit(1);
				}
				if (!(i < nMaxNodes && j < nMaxNodes)) {
					fprintf(stderr, "Warning: indices must be less than maxNodes(%d): %s", nMaxNodes, str);
				}

				qubo_set(i+1,j+1,(double)v,Q);
				NofReadEntries++;
			}
		}
	}

	if (NofReadEntries != nNodes+nCouplers) {
		fprintf(stderr, "Warning: number of read entries is less than nNodes plust nCouplers.\n");
	}

	return Q;
}

void qubo_write(FILE* to, qubo_ptr Q)
{
	assert(to != NULL);
	assert(Q != NULL);

	// comment line
	fprintf(to, "%c Variables take value %s.\n", comment_symb, Q->vtype == QUBO_BIMODAL? "1 or -1":"1 or 0");

	// program line
	fprintf(to, "%c qubo 0 %d %d %d\n", program_symb, Q->nMaxNodes, Q->nNodes, Q->nCouplers);
	
	fprintf(to, "%c -----------------------\n", comment_symb);
	for (int i = 1; i <= Q->nMaxNodes; i++) {
		const double val = qubo_get(i,i,Q);
		const int ival = (int)val;

		if (val - ival != 0.0) {
			fprintf(stderr, "qubo coefficients must be integers.\n");
			exit(1);
		}

		if (ival != 0) {
			fprintf(to, "%d %d %d\n", i-1, i-1, ival);
		}
	}

	fprintf(to, "%c -----------------------\n", comment_symb);
	for (int i = 1; i <= Q->nMaxNodes; i++) {
		for (int j = i+1; j <= Q->nMaxNodes; j++) {
			const double val = qubo_get(i,j, Q);
			const int ival = (int)val;

			if (val - ival != 0.0) {
				fprintf(stderr, "qubo coefficients must be integers.\n");
				exit(1);
			}

			if (ival != 0) {
				fprintf(to, "%d %d %d\n", i-1, j-1, ival);
			}
		}
	}
}
