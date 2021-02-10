#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<stdbool.h>
#include<assert.h>

#include "be_xor.h"

//=================================================================================================
// Major functions:

/* \brief Creates be from xor.
 * \param f xor
 * \return be
 */
be_ptr create_be_from_xor(vecp* f)
{

	be_ptr result = NULL;

	const int nof_constraints = vecp_size(f);
	
	for (int i = 0; i < nof_constraints; i++) {
		veci* v = vecp_begin(f)[i];

		be_ptr p = NULL;

		const int nof_literals = veci_size(v)-1; // remove parity
		assert(veci_begin(v)[nof_literals] == -1 || veci_begin(v)[nof_literals] == -2);
		const int parity = abs(veci_begin(v)[nof_literals]); // parity

		for (int j = 0; j < nof_literals; j++) {
			intptr_t var = veci_begin(v)[j];
			assert(var > 0);

			be_ptr q = be_find_node(ATOM, (be_ptr)var, NULL);
			be_ptr nq = be_find_node(NOT, q, NULL);
			be_ptr np = be_find_node(NOT, p, NULL);

			if (p == NULL) {
				p = q;
			} else if (parity == 1) { // odd
				be_ptr t = be_find_node(AND, q, np);
				be_ptr tt = be_find_node(AND, nq, p);
				p = be_find_node(OR, t, tt);
			} else if (parity == 2) { // even
				be_ptr t = be_find_node(OR, q, np);
				be_ptr tt = be_find_node(OR, nq, p);
				p = be_find_node(AND, t, tt);
			} else {
				assert(0);
			}
		}

		result = (result == NULL)? p: be_find_node(AND, result, p);

	}

	be_check_valid(result);

	return result;
}


