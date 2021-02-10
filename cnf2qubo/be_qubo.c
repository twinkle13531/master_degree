#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<stdbool.h>
#include<assert.h>

#include "be_qubo.h"

#include <limits.h>

#define VERBOSE 1

//=================================================================================================
// Static function prototypes:
static int beIsing_compute_qubo_recur(qubo_ptr q, const be_ptr f);

static void beIsing_set_minimumEnergy(qubo_var_type type);

static int beIsing_compute_minimumEnergy_binaryOP(int coeff_x, int coeff_y, int coeff_z, int coeff_x_z, int coeff_y_z, int coeff_x_y, int mode);
static int beIsing_compute_minimumEnergy_unaryOP(const int coeff_x, const int coeff_z, const int coeff_x_z, int mode);
static int beIsing_compute_minimumEnergy_constantOP(const int coeff_z, int mode);

static int beIsing_add_OR_primitive(qubo_ptr q, const int x, const int y, const int z);
static int beIsing_add_AND_primitive(qubo_ptr q, const int x, const int y, const int z);
static int beIsing_add_NOT_primitive(qubo_ptr q, const int x, const int z);
static int beIsing_add_identity_primitive(qubo_ptr q, const int x, const int z);
static int beIsing_add_one_primitive(qubo_ptr q, const int z);


static int or_energy_Bimodal = 0;
static int and_energy_Bimodal = 0;
static int not_energy_Bimodal = 0;
static int identity_energy_Bimodal = 0;
static int one_energy_Bimodal = 0;

static int or_energy_Boolean = 0;
static int and_energy_Boolean = 0;
static int not_energy_Boolean = 0;
static int identity_energy_Boolean = 0;
static int one_energy_Boolean = 0;

static int  bc_count  = 0;
static char bc_id[] = "bc";
static char bc_energy_symbol = 'e';
 
//=================================================================================================
// Major functions:

int beIsing_compute_qubo(qubo_ptr q, const be_ptr f)
{
	bc_count = 0;
	beIsing_set_minimumEnergy(q->vtype);

	assert(!be_is_checked(f));
	int energy = beIsing_compute_qubo_recur(q, f);
	energy += beIsing_add_one_primitive(q, be_get_assigned_var(f)); // fix the final output to 1.
	be_uncheck_recur(f);

#ifdef VERBOSE
	fprintf(stdout, "c %s%d %c /*Energy of solution*/\n", bc_id, ++bc_count, bc_energy_symbol);
#endif

	return energy;
}

// The following getter functions are available only after beIsing_compute_qubo is executed.
int beIsing_get_mininumEnergy_or(qubo_var_type type)
{
	int result = 0;
	if (type == QUBO_BIMODAL) {
		result = or_energy_Bimodal;
	} else if (type == QUBO_BOOL) {
		result = or_energy_Boolean;
	} else {
		assert(0);
	}

	return result;
}

int beIsing_get_mininumEnergy_and(qubo_var_type type)
{
	int result = 0;

	if (type == QUBO_BIMODAL) {
		result = and_energy_Bimodal;
	} else if (type == QUBO_BOOL) {
		result = and_energy_Boolean;
	} else {
		assert(0);
	}

	return result;
}

int beIsing_get_mininumEnergy_not(qubo_var_type type)
{
	int result = 0;

	if (type == QUBO_BIMODAL) {
		result = not_energy_Bimodal;
	} else if (type == QUBO_BOOL) {
		result = not_energy_Boolean;
	} else {
		assert(0);
	}

	return result;
}

int beIsing_get_mininumEnergy_one(qubo_var_type type)
{
	int result = 0;

	if (type == QUBO_BIMODAL) {
		result = one_energy_Bimodal;
	} else if (type == QUBO_BOOL) {
		result = one_energy_Boolean;
	} else {
		assert(0);
	}

	return result;
}


//=================================================================================================
// Utility functions:


static int beIsing_compute_qubo_recur(qubo_ptr q, const be_ptr f)
{
	if (f == NULL || be_is_checked(f)) return 0;

	int energy = 0;

	if (be_get_type(f) == ATOM) {

	} else if (be_get_type(f) == NOT) {
		be_ptr left  = be_get_left(f);
		int x = be_get_assigned_var(left);  // input
		int z = be_get_assigned_var(f);     // output
		energy += beIsing_add_NOT_primitive(q,x,z);
	} else {
		be_ptr left  = be_get_left(f);
		be_ptr right = be_get_right(f);

		energy += beIsing_compute_qubo_recur(q, left);
		energy += beIsing_compute_qubo_recur(q, right);

		int x = be_get_assigned_var(left);  // input
		int y = be_get_assigned_var(right); // input
		int z = be_get_assigned_var(f);     // output

		if (y < x) {
			int t = y;
			y = x;
			x = t;
		}		

		switch(be_get_type(f)) {
			case OR:
				energy += beIsing_add_OR_primitive(q,x,y,z);
				break;
			case AND:
				energy += beIsing_add_AND_primitive(q,x,y,z);
				break;
			default:
				fprintf(stderr, "invalid be node type\n");
				exit(1);
				break; 
		}
	}

	be_check(f);

	return energy;
}


static void beIsing_set_minimumEnergy(qubo_var_type type)
{
	if (type == QUBO_BIMODAL) {
#ifdef VERBOSE
		fprintf(stdout, "c %s%d /*To calculation energy, use the following comments indicated by the keyword %s and compute with bc.*/\n", bc_id, ++bc_count, bc_id);
		fprintf(stdout, "c %s%d %c = 0\n", bc_id, ++bc_count, bc_energy_symbol);
#endif

		or_energy_Bimodal       = beIsing_compute_minimumEnergy_binaryOP(1,1,-2,-2,-2,1, 0);
		and_energy_Bimodal      = beIsing_compute_minimumEnergy_binaryOP(-1,-1,2,-2,-2,1, 0);
		not_energy_Bimodal      = beIsing_compute_minimumEnergy_unaryOP(0,0,2, 0);
		identity_energy_Bimodal = beIsing_compute_minimumEnergy_unaryOP(0,0,-2, 0);
		one_energy_Bimodal      = beIsing_compute_minimumEnergy_constantOP(-2, 0);
	} else if (type == QUBO_BOOL) {
#ifdef VERBOSE
		fprintf(stdout, "c %s%d /*To calculation energy, use the following comments indicated by the keyword %s and compute with bc.*/\n", bc_id, ++bc_count, bc_id);
		fprintf(stdout, "c %s%d /*for i in {1..9}; do echo \"000110111\" | cut -c $i | sed -e \"s/\\(.\\)/s[$i]=\\1/g\"; done # bash script for setting the array s*/\n", bc_id, ++bc_count);
		fprintf(stdout, "c %s%d %c = 0\n", bc_id, ++bc_count, bc_energy_symbol);
#endif
	
		or_energy_Boolean       = beIsing_compute_minimumEnergy_binaryOP(4,4,4,-8,-8,4, 1);
		and_energy_Boolean      = beIsing_compute_minimumEnergy_binaryOP(0,0,12,-8,-8,4, 1);
		not_energy_Boolean      = beIsing_compute_minimumEnergy_unaryOP(-4,-4,8, 1);
		identity_energy_Boolean = beIsing_compute_minimumEnergy_unaryOP(4,4,-8, 1);
		one_energy_Boolean      = beIsing_compute_minimumEnergy_constantOP(-4, 1);
	} else {
		assert(0);
	}
}


static int beIsing_compute_minimumEnergy_binaryOP(int coeff_x, int coeff_y, int coeff_z, int coeff_x_z, int coeff_y_z, int coeff_x_y, int mode)
{
	const int len = 2;
	const int vars = 3;
	const int x = 0;
	const int y = 1;
	const int z = 2;
	assert(z+1 == vars);
 
	int s[vars][len];

	for (int w = 0; w<vars; w++) {
			s[w][0] = mode == 0? -1: 0;
			s[w][1] = 1;
	}

	int min = INT_MAX;
	for (int i = 0; i<len; i++) {
		for (int j = 0; j<len; j++) {
			for (int k= 0; k<len; k++) {
				int e = coeff_x*s[x][i] + coeff_y*s[y][j] + coeff_z*s[z][k]
				+ coeff_x_z*s[x][i]*s[z][k] + coeff_y_z*s[y][j]*s[z][k] + coeff_x_y*s[x][i]*s[y][j];
				if (e < min) {
					min = e;
				}
			}
		}
	}

	return min; // minimum energy of binary operation.
}


static int beIsing_compute_minimumEnergy_unaryOP(const int coeff_x, const int coeff_z, const int coeff_x_z, int mode)
{
	const int len = 2;
	const int vars = 3;
	const int x = 0;
	const int y = 1;
	const int z = 2;
	assert(z+1 == vars);
 
	int s[vars][len];

	for (int w = 0; w<vars; w++) {
			s[w][0] = mode == 0? -1: 0;
			s[w][1] = 1;
	}

	int min = INT_MAX;
	for (int i = 0; i<len; i++) {
		for (int k= 0; k<len; k++) {
			int e = coeff_x*s[x][i] + coeff_z*s[z][k]
				+ coeff_x_z*s[x][i]*s[z][k];
			if (e < min) {
				min = e;
			}
		}
	}

	return min; // minimum energy of unary operation.
}

static int beIsing_compute_minimumEnergy_constantOP(const int coeff_z, int mode)
{
	const int len = 2;
	const int vars = 3;
	const int x = 0;
	const int y = 1;
	const int z = 2;
	assert(z+1 == vars);
 
	int s[vars][len];

	for (int w = 0; w<vars; w++) {
			s[w][0] = mode == 0? -1: 0;
			s[w][1] = 1;
	}

	int min = INT_MAX;
	for (int k= 0; k<len; k++) {
		int e = coeff_z*s[z][k];
		if (e < min) {
			min = e;
		}
	}

	return min; // minimum energy of unary operation.
}

/* \brief Add the ising primitive for OR over two positive literals: z = x | y.
 * \param q coefficients for the terms of degree 1 or 2
 * \param x input variable
 * \param y input variable
 * \param z output variable
 * \note y must be larger than x.
 */
static int beIsing_add_OR_primitive(qubo_ptr q, const int x, const int y, const int z)
{
	assert(x < y);

	if (q->vtype == QUBO_BIMODAL) {
		qubo_add(x,x, 1,q);
		qubo_add(y,y, 1,q);
		qubo_add(z,z,-2,q);

		qubo_add(x,z,-2,q);
		qubo_add(y,z,-2,q);
		qubo_add(x,y, 1,q);

#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += s[%d]+s[%d]-2*s[%d]-2*s[%d]*s[%d]-2*s[%d]*s[%d]+s[%d]*s[%d]\t/*x%d = x%d or x%d*/\n", bc_id, ++bc_count, bc_energy_symbol, x, y, z, x,z, y,z, x,y, z,x,y);
#endif

	} else if (q->vtype == QUBO_BOOL) {
		qubo_add(x,x, 4,q);
		qubo_add(y,y, 4,q);
		qubo_add(z,z, 4,q);

		qubo_add(x,z,-8,q);
		qubo_add(y,z,-8,q);
		qubo_add(x,y, 4,q);

#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += 4*s[%d]+4*s[%d]+4*s[%d]-8*s[%d]*s[%d]-8*s[%d]*s[%d]+4*s[%d]*s[%d]\t/*x%d = x%d or x%d*/\n", bc_id, ++bc_count, bc_energy_symbol, x, y, z, x,z, y,z, x,y, z,x,y);
#endif

	} else {
		assert(0);
	}

	return or_energy_Bimodal;
}

/* \brief Add the ising primitive for AND over two positive literals: z = x & y.
 * \param q coefficients for the terms of degree 1 or 2
 * \param x input variable
 * \param y input variable
 * \param z output variable
 * \note y must be larger than x.
 */
static int beIsing_add_AND_primitive(qubo_ptr q, const int x, const int y, const int z)
{
	assert(x < y);

	if (q->vtype == QUBO_BIMODAL) {
		qubo_add(x,x,-1,q);
		qubo_add(y,y,-1,q);
		qubo_add(z,z, 2,q);

		qubo_add(x,z,-2,q);
		qubo_add(y,z,-2,q);
		qubo_add(x,y, 1,q);

#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += -s[%d]-s[%d]+2*s[%d]-2*s[%d]*s[%d]-2*s[%d]*s[%d]+s[%d]*s[%d]\t/*x[%d] = x%d and x%d*/\n", bc_id, ++bc_count, bc_energy_symbol, x, y, z, x,z, y,z, x,y, z,x,y);
#endif
	} else if (q->vtype == QUBO_BOOL) {
		qubo_add(x,x, 0,q);
		qubo_add(y,y, 0,q);
		qubo_add(z,z,12,q);

		qubo_add(x,z,-8,q);
		qubo_add(y,z,-8,q);
		qubo_add(x,y, 4,q);

#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += 12*s[%d]-8*s[%d]*s[%d]-8*s[%d]*s[%d]+4*s[%d]*s[%d]\t/*x%d = x%d and x%d*/\n", bc_id, ++bc_count, bc_energy_symbol, z, x,z, y,z, x,y, z,x,y);
#endif
	} else {
		assert(0);
	}

	return and_energy_Bimodal;
}

/* \brief Add the ising primitive for NOT: z = ~x.
 * \param q coefficients for the terms of degree 1 or 2
 * \param x input variable
 * \param z output variable
 */
static int beIsing_add_NOT_primitive(qubo_ptr q, const int x, const int z)
{
	if (q->vtype == QUBO_BIMODAL) {
		qubo_add(x,z, 2,q);
#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += 2*s[%d]*s[%d]\t/*x(%d) = not x%d*/\n", bc_id, ++bc_count, bc_energy_symbol, x,z, z,x);
#endif
	} else if (q->vtype == QUBO_BOOL) {
		qubo_add(x,x,-4,q);
		qubo_add(z,z,-4,q);
		qubo_add(x,z, 8,q);
#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += -4*s[%d]-4*s[%d]+8*s[%d]*s[%d]\t/*x%d = not x%d*/\n", bc_id, ++bc_count, bc_energy_symbol, x, z, x,z, z,x);
#endif
	} else {
		assert(0);
	}

	return not_energy_Bimodal;
}

/* \brief Add the ising primitive for identity: z = x.
 * \param q coefficients for the terms of degree 1 or 2
 * \param x input variable
 * \param z output variable
 */
static int beIsing_add_identity_primitive(qubo_ptr q, const int x, const int z)
{
	if (q->vtype == QUBO_BIMODAL) {
		qubo_add(x,z,-2,q);
#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += -2*s[%d]*s[%d]\t/*x%d = x%d*/\n", bc_id, ++bc_count, bc_energy_symbol, x,z, z,x);
#endif
	} else if (q->vtype == QUBO_BOOL) {
		qubo_add(x,x, 4,q);
		qubo_add(z,z, 4,q);
		qubo_add(x,z,-8,q);
#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += 4*s[%d]+4*s[%d]-8*s[%d]*s[%d]\t/*x%d = x%d*/\n", bc_id, ++bc_count, bc_energy_symbol, x, z, x,z, z,x);
#endif
	} else {
		assert(0);
	}

	return identity_energy_Bimodal;
}

/* \brief Add the ising primitive for constant 1: z = 1.
 * \param q coefficients for the terms of degree 1 or 2
 * \param z output variable
 */
static int beIsing_add_one_primitive(qubo_ptr q, const int z)
{
	if (q->vtype == QUBO_BIMODAL) {
		qubo_add(z,z,-2,q);
#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += -2*s[%d]\t/*x%d = 1*/\n", bc_id, ++bc_count, bc_energy_symbol, z, z);
#endif
	} else if (q->vtype == QUBO_BOOL) {
		qubo_add(z,z,-4,q);
#ifdef VERBOSE
		fprintf(stdout, "c %s%d %c += -4*s[%d]\t/*x%d = 1*/\n", bc_id, ++bc_count, bc_energy_symbol, z, z);
#endif
	} else {
		assert(0);
	}

	return one_energy_Bimodal;
}


