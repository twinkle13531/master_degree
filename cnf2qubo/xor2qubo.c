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


#include "xor2qubo.h"

#include "vec.h"

#include "be.h"
#include "xor.h"
#include "be_xor.h"
#include "be_qubo.h"
#include "be_dot.h"
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
	fprintf(stderr, "Usage:\t%s [options] xor-file\n", (p));
	fprintf(stderr, "-d\tPrints out a Boolean expression in DOT format.\n");
	fprintf(stderr, "-s\tComputes Ising model whose variables take value 1 or -1. If this option is not specified, variables take value 1 or 0.\n");
}

//=================================================================================================
// main:

int main(int argc, char** argv)
{
    FILE *  in;
		char header[BUFSIZ];
		char dotfname[BUFSIZ];
		char * input_file = NULL;

		// for dot file
		FILE *  out = NULL;
		bool    d_specified = false;
		bool    s_specified = false;

		int size = 0;

		vecp* f = xor_create();
		be_ptr g;

		veci inputs;
		veci_new(&inputs);

		for (int i = 1; i < argc; i++) {
			if (argv[i][0] == '-') {
				switch (argv[i][1]) {
					case 'd':
						d_specified = true;
						break;
					case 's':
						s_specified = true;
						break;
					case '?': case 'h': default:
						PRINT_USAGE(argv[0]);
						return 0;
				}
			} else {
				if (input_file != NULL) {
						PRINT_USAGE(argv[0]);
						return 1;
				}
				input_file = argv[i];
			}
		}

		if (input_file == NULL) {
			PRINT_USAGE(argv[0]);
			return 1;
		}

		{
			int i = 0;
			while(i < BUFSIZ && input_file[i] != '\0' && input_file[i] != '.') {
				header[i] = input_file[i];
				dotfname[i] = header[i];
				i++;
			}

			if (i == BUFSIZ) {
				fprintf(stderr, "could not find the end of string\n");
				exit(1);
			}
			dotfname[i++] = '.';
			dotfname[i++] = 'd';
			dotfname[i++] = 'o';
			dotfname[i++] = 't';
			dotfname[i]   = '\0';
			header[i] = '\0';
		}

		// Parse XOR constraints.
		in = fopen(input_file, "rb");
		if (in == NULL) {
			fprintf(stderr, "ERROR! Could not open file: %s\n", argc == 1 ? "<stdin>" : input_file);
				PRINT_USAGE(argv[0]);
			exit(1);
		}
		xor_parse(in, f);
		fclose(in);

		be_init();

		// Create a Boolean expression.
		g = create_be_from_xor(f);
		be_assign_vars(g, xor_get_maxvar(f)+1);
		size = be_get_assigned_var(g);

		// Print be in DOT if specified.
		if (d_specified) {
			out = fopen(dotfname, "w");
			if (out == NULL) {
				fprintf(stderr, "ERROR! Could not open file: %s\n", dotfname);
				PRINT_USAGE(argv[0]);
				exit(1);
			}
			beDot_print(out, header, g);
		}

		// Collect input variables.
		be_collect_inputs(g, &inputs);


		// Initialize qubo data structure.
		qubo_ptr Q = qubo_create(QUBO_HASH, s_specified? QUBO_BIMODAL:QUBO_BOOL, size);

		// Compute qubo.
		int minimum_energy = beIsing_compute_qubo(Q, g);


		// comment line
		fprintf(stdout, "%c %d minimum energy of solution\n", comment_symb, minimum_energy);
		// list of input variables in one line
		fprintf(stdout, "%c Important Variables:", comment_symb);
		for (int i = 0; i < veci_size(&inputs); i++) {
			fprintf(stdout, " %d", veci_begin(&inputs)[i]);	
		}
		fprintf(stdout, "\n");

		qubo_write(stdout, Q);

		// delete
		xor_destroy(f);
		be_quit();
		veci_delete(&inputs);

		if (d_specified) fclose(out);

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



