#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include <time.h>
#include <unistd.h>
#include <math.h>

#include "qubo_io.h"


//=================================================================================================
// Constants:

static const char comment_symb = 'c';
static const char program_symb = 'p';

//=================================================================================================
// Static function prototypes:

static int first(int i, int n);
static int second(int i, int n);
static int third(int i, int n);
static int var(int a, int b, int c, int n);

static void PRINT_USAGE(char *p)
{
	fprintf(stderr, "Usage:\t%s [options] size_N\n", (p));
	fprintf(stderr, "Description: This program computes the hamiltonian of the Edwards-Anderson ising spin glass where variables take value 1 or -1 and they corresnd with veritces in hypercubic lattice in three dimension in N^3 sites.\n");
}

//=================================================================================================
// main:

int main(int argc, char** argv)
{

		int size_N = 0;
		int nof_vars = 0;

		if (!(argc == 3 || argc == 2)) {
			PRINT_USAGE(argv[0]);
			return 1;
		}

		for (int i = 1; i < argc; i++) {
			if (argv[i][0] == '-') {
				switch (argv[i][1]) {
					case '?': case 'h': default:
						PRINT_USAGE(argv[0]);
						return 0;
				}
			} else {
				if (size_N != 0) {
						PRINT_USAGE(argv[0]);
						return 1;
				}
				size_N = atoi(argv[i]);
				if (size_N <= 0) {
						PRINT_USAGE(argv[0]);
						return 1;
				}
			}
		}



		// Initialize M.
		nof_vars = size_N*size_N*size_N;	// number of vertices in hypercubic lattice

		// Tests
		for (int i = 0; i < nof_vars; i++) {
			assert(i == var(first(i,size_N), second(i,size_N), third(i,size_N), size_N));
		}
		for (int i = 0; i < size_N; i++) {
			for (int j = 0; j < size_N; j++) {
				for (int k = 0; k < size_N; k++) {
					assert(first(var(i,j,k,size_N), size_N) == i);
					assert(second(var(i,j,k,size_N), size_N) == j);
					assert(third(var(i,j,k,size_N), size_N) == k);
				}
			}
		}

		qubo_ptr Q = qubo_create(QUBO_HASH, QUBO_BIMODAL, nof_vars);

		srand((unsigned int)time(NULL));

		for (int i = 0; i < nof_vars; i++) {
			for (int j = i+1; j < nof_vars; j++) {
				const int ai = first(i, size_N);
				const int bi = second(i, size_N);
				const int ci = third(i, size_N);

				const int aj = first(j, size_N);
				const int bj = second(j, size_N);
				const int cj = third(j, size_N);

				if (abs(ai-aj)+abs(bi-bj)+abs(ci-cj) == 1) { // adjacent vertices
					const int ival = 2*(rand()%2)-1;
					qubo_set(i+1, j+1, (double)ival, Q);
				}
			}
		}



		fprintf(stdout, "%c The Edwards-Anderson ising spin grass for hypercubic lattice in three dimension of %d^3 sites.\n", comment_symb, size_N);

		qubo_write(stdout, Q);
		qubo_destroy(Q);

    return 0;
}



//=================================================================================================
// Static functions:

static int var(int a, int b, int c, int n)
{
	assert(0 <= a && a < n);
	assert(0 <= b && b < n);
	assert(0 <= c && c < n);

	return a + b * n + c * n * n;
}

static int third(int i, int n)
{
	return i/(n*n);
}

static int second(int i, int n)
{
	return (i%(n*n))/n;
}

static int first(int i, int n)
{
	return (i%(n*n))%n;
}
