#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<stdbool.h>
#include<assert.h>

#include "be_cnf.h"

//=================================================================================================
// Major functions:

/* \brief Creates be from cnf.
 * \param f cnf
 * \return be
 */
be_ptr create_be_from_cnf(const cnf_ptr f)
{
	cnf_check_valid(f);

	be_ptr result = NULL;

	const int nof_clauses = cnf_get_size(f);
	
	for (int i = 0; i < nof_clauses; i++) {
		clause_ptr cls = cnf_get(f, i);

		be_ptr p = NULL;

		const int nof_literals = clause_get_size(cls);

		for (int j = 0; j < nof_literals; j++) {
			int literal = clause_get(cls, j);
			intptr_t var = abs(literal);

			be_ptr q = be_find_node(ATOM, (be_ptr)var, NULL);
			if (literal < 0) {
				q = be_find_node(NOT, q, NULL);	
			}

			p = (p == NULL)? q: be_find_node(OR, p, q);

		}

		result = (result == NULL)? p: be_find_node(AND, result, p);

	}

	be_check_valid(result);

	return result;
}


