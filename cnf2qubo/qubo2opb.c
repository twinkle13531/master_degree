/**************************************************************************************************
MiniSat -- Copyright (c) 2005, Niklas Sorensson
http://www.cs.chalmers.se/Cs/Research/FormalMethods/MiniSat/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
**************************************************************************************************/
// Modified to compile with MS Visual Studio 6.0 by Alan Mishchenko


#include "vec.h"

#include "be.h"
#include "be_qubo.h"
#include "qubo_io.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>

//=================================================================================================
// Constants:

static const char comment_symb = 'c';
static const char program_symb = 'p';

//=================================================================================================
// Static function prototypes:

static void check_memalloc(void* x);

static void PRINT_USAGE(char *p)
{
	fprintf(stderr, "Usage:\t%s qubo\n", (p));
	fprintf(stderr, "Note: Qubo variables must have 1 or 0.\n");
}

//=================================================================================================
// main:

int main(int argc, char** argv)
{
	if (argc != 2) {
		PRINT_USAGE(argv[0]);
		exit(1);
	}


	FILE* in = fopen(argv[1], "rb");
	if (in == NULL) {
		fprintf(stderr, "ERROR! Could not open file: %s\n", argc == 1 ? "<stdin>" : argv[1]);
			PRINT_USAGE(argv[0]);
		exit(1);
	}

        char comments[BUFSIZ];
        qubo_ptr Q = qubo_read(in, QUBO_BOOL, comments, BUFSIZ);
        fclose(in);

	int nextvar = Q->nMaxNodes+1;

	FILE *out = stdout;
	fprintf(out, "min: ");
	for (int i = 1; i <= Q->nMaxNodes; i++) {
		int val = (int)qubo_get(i,i,Q);
		if (val != 0) {
	 		fprintf(out, " %c%d*x%d ", val > 0? '+': '-',abs(val),i);
		}

		for (int j = i+1; j <= Q->nMaxNodes; j++) {
			int val = (int)qubo_get(i,j,Q);
			if (val != 0) {
	 			fprintf(out, " %c%d*x%d ", val > 0? '+': '-', abs(val), nextvar++);
			}
		}
	}
	fprintf(out, ";\n");

	nextvar = Q->nMaxNodes+1;
	for (int i = 1; i <= Q->nMaxNodes; i++) {
		for (int j = i+1; j <= Q->nMaxNodes; j++) {
			int val = (int)qubo_get(i,j,Q);
			if (val != 0) {
				int k = nextvar++;
				fprintf(out,  " +1*x%d -1*x%d >= 0;\n",i,k);
				fprintf(out,  " +1*x%d -1*x%d >= 0;\n",j,k);
				fprintf(out,  " -1*x%d -1*x%d +1*x%d >= -1;\n",i,j,k);
			}
		}
	}

	// delete
	qubo_destroy(Q);

    return 0;
}

//=================================================================================================
// Static functions:

static void check_memalloc(void* x)
{
	if(x == NULL) {
		fprintf(stderr, "memory allocation failed\n");	
		exit(1);
	}
}



