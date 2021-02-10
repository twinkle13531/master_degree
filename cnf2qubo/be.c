#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<stdbool.h>
#include<assert.h>

#include "be.h"

//=================================================================================================
// Static function prototypes:

static void be_assign_vars_recur(be_ptr be, int* nextvar_ptr);
static void be_compute_assignment_recur_01_version(int* assign, const be_ptr g, const int size);
static void be_collect_inputs_recur(const be_ptr g, veci* vars);

//=================================================================================================
// Unique table definition:

// table entry
struct entry_tag {
	be_ptr data;
	struct entry_tag* next;
};

typedef struct entry_tag entry;
typedef entry* entry_ptr;

static entry_ptr* unique_table = NULL;
static int table_size = 6700417;
 

//=================================================================================================
// Major functions:

/* \brief Creates and initializes be environment.
 * \note Execute this once before using be package.
 * \see be_quit
 */
void be_init(void)
{
	if (unique_table != NULL) {
		fprintf(stderr, "unique table exists\n");
		exit(1);
	}

	unique_table = (entry_ptr*)malloc(sizeof(entry_ptr)*table_size);
	if (unique_table == NULL) {
		fprintf(stderr, "memory allocation failed\n");
		exit(1);
	}

	for (int i = 0; i < table_size; i++) {
		unique_table[i] = NULL;
	}

}

/* \brief Destroys be environment.
 * \note Not only buckets of the unique table but also all the contained Bes are deleted.
 * \see be_init
 */
void be_quit(void)
{
	for (int i = 0; i < table_size; i++) {
			entry_ptr p = unique_table[i];
			while(p != NULL) {
				entry_ptr tmp = p->next;
				be_check_valid(p->data);
				free(p->data);
				free(p);
				p = tmp;
			}
			unique_table[i] = NULL;
	}	
	unique_table = NULL;
}

/* \brief Finds be of a given type and having left child and right child.
 * \param type Type of Be
 * \param left The left child of this be node, possibly NULL.
 * \param right The right child of this be node, possibly NULL.
 * \return If such a be already exists, return it; otherwise, create a new be with those fields and return it.
 * \note All newly created be nodes have 0 in the iaux field and false in the checked field.
 */
be_ptr be_find_node(const BeType type, const be_ptr left, const be_ptr right)
{
	uintptr_t key = (uintptr_t)type;
	if (left != NULL) {
		key *= (uintptr_t)left;
	}
	if (right != NULL) {
		key *= (uintptr_t)right;
	}

	entry_ptr p = unique_table[key%table_size];
	while(p != NULL) {
		if ( type  == p->data->type
			&& left  == p->data->left
			&& right == p->data->right) {
			return p->data;
		}
		p = p->next;
	}

	be_ptr data  = (be_ptr)malloc(sizeof(be));
	data->type  = type;
	data->left  = left;
	data->right = right;
	data->iaux  = 0;
	data->checked = false;

	entry_ptr new = (entry_ptr)malloc(sizeof(entry));
	if (new == NULL) {
		fprintf(stderr, "memory allocation failed\n");
		exit(1);
	}

	new->data = data;
	new->next = unique_table[key%table_size];
	unique_table[key%table_size] = new;

	be_check_valid(data);
	return data;
}

/* \brief Unchecks all the nodes below a given be node. 
 * \param f be
 * \note When all the nodes of be is traversed, it is efficient to use their checked field so that once a node is visited, its checked field is set true. It is important that as soon as Be traversal finishes, makes all the checked field false by executing this function.
 */
void be_uncheck_recur(be_ptr f)
{
	if (f == NULL || f->checked == false) return ;
	if (f->type == ATOM) {
		f->checked = false;
		return ;
	}

	be_uncheck_recur(f->left);
	be_uncheck_recur(f->right);
	f->checked = false;
}

/* \brief Checks if a given be is valid.
 * \param f be
 */
void be_check_valid(const be_ptr f)
{
	if (f == NULL) {
		fprintf(stderr, "invalid be\n");
		exit(1);
	}
}

/* \brief decide if a given be node is checked.
 * \param f be
 * \return true if it is checked; false otherwise.
 */
bool be_is_checked(const be_ptr f)
{
	be_check_valid(f);

	return f->checked;
}

/* \brief check this be node.
 * \param f be
 */
void be_check(const be_ptr f)
{
	be_check_valid(f);
	
	f->checked = true;
}

/* \brief Gets the type of a given be node.
 * \param f be
 * \return the type of a be node
 */
BeType be_get_type(const be_ptr f)
{
	be_check_valid(f);

	return f->type;
}

/* \brief Gets the left child node of a given be node.
 * \param f be
 * \return the left child be node.
 * \see be_get_right
 */
be_ptr be_get_left(const be_ptr f)
{
	be_check_valid(f);

	return f->left;
}

/* \brief Gets the right child node of a given be node.
 * \param f be
 * \return the right child be node.
 * \see be_get_left
 */
be_ptr be_get_right(const be_ptr f)
{
	be_check_valid(f);

	return f->right;
}

// This function computes from the assignment for the CNF variables the assignment for the other variables,
// where the value assigned to each variable is 1 for true and 0 for false.
void be_compute_assignment_01_version(int* assign, const be_ptr g, const int size)
{

	assert(!be_is_checked(g));	
	be_compute_assignment_recur_01_version(assign, g, size);
	be_uncheck_recur(g);

	return ;
}


static void be_compute_assignment_recur_01_version(int* assign, const be_ptr g, const int size)
{
	if (g == NULL || be_is_checked(g)) return ;

	if (be_get_type(g) == ATOM) {
		int x = be_get_assigned_var(g);
		assert(0 < x && x <= size);
		assert(assign[x] == 0 || assign[x] == 1); // must be assigned

	} else if (be_get_type(g) == NOT) {
		be_ptr left  = be_get_left(g);
		int x = be_get_assigned_var(left);  // input
		int z = be_get_assigned_var(g);     // output

		assert(0 < x && x <= size);
		assert(0 < z && z <= size);
		assert(assign[x] == 0 || assign[x] == 1); // must be assigned

		assign[z] = 1 - assign[x];
	} else {
		be_ptr left  = be_get_left(g);
		be_ptr right = be_get_right(g);

		be_compute_assignment_recur_01_version(assign, left, size);
		be_compute_assignment_recur_01_version(assign, right, size);

		int x = be_get_assigned_var(left);  // input
		int y = be_get_assigned_var(right); // input
		int z = be_get_assigned_var(g);     // output

		if (y < x) {
			int t = y;
			y = x;
			x = t;
		}

		assert(0 < x && x <= size);
		assert(0 < y && y <= size);
		assert(0 < z && z <= size);
		assert(assign[x] == 0 || assign[x] == 1); // must be assigned
		assert(assign[y] == 0 || assign[y] == 1); // must be assigned

		switch(be_get_type(g)) {
			case OR:
				assign[z] = 1 - (1 - assign[x]) * (1 - assign[y]);
				break;
			case AND:
				assign[z] = assign[x] * assign[y];
				break;
			default:
				fprintf(stderr, "invalid be node type\n");
				exit(1);
				break; 
		}
	}

	be_check(g);

	return ;
}

void be_collect_inputs(const be_ptr g, veci* vars)
{
	assert(!be_is_checked(g));	
	be_collect_inputs_recur(g, vars);
	be_uncheck_recur(g);
}

static void be_collect_inputs_recur(const be_ptr g, veci* vars)
{
	if (g == NULL || be_is_checked(g)) return;

	if (be_get_type(g) == ATOM) {
		assert(be_is_var_assigned(g));
		veci_push(vars, be_get_assigned_var(g));

	} else {
		be_collect_inputs_recur(be_get_left(g), vars);
		be_collect_inputs_recur(be_get_right(g), vars);

	}

	be_check(g);
}


//=================================================================================================
// Optional functions:

/* \brief Assigns all the internal be nodes below a given be with variables.
 * \param f be
 * \param init_var new variables are taken from init_var and larger variables in incremental fashion.
 * \see be_assign_vars_recur
 * \note init_var must be a positive integer.
 */
void be_assign_vars(be_ptr f, const int init_var)
{
	be_check_valid(f);

	assert(f->checked == false);

	if (!(init_var > 0)) {
		fprintf(stderr, "Variables must be assigned value larger than 0\n");
		exit(1);
	}

	int nextvar = init_var; // the next variable available
	be_assign_vars_recur(f, &nextvar);
	be_uncheck_recur(f);
}

static void be_assign_vars_recur(be_ptr f, int* nextvar_ptr)
{
	if (f == NULL) 		return;	
	if (f->checked == true) return;

	switch (f->type) {
		case ATOM:
			f->iaux = (intptr_t)f->left;
			break;
		case NOT:
		case OR:
		case AND:
			be_assign_vars_recur(f->left, nextvar_ptr);
			be_assign_vars_recur(f->right, nextvar_ptr);
			f->iaux = ((*nextvar_ptr)++);
			break;
		default:
			fprintf(stderr,  "invalid be node type\n");
			exit(1);
			break;
	}

	f->checked = true;
}

/* \brief Gets the variable assigned to a given be node.
 * \param f be
 * \return the assigned variable.
 */
int be_get_assigned_var(const be_ptr f)
{
	be_check_valid(f);

	if (!(f->iaux > 0)) {
		fprintf(stderr, "Variable is not yet assigned, or an invalid value is assinged\n");
		exit(1);
	}

	return (int)f->iaux;
}

/* \brief Resets the currently assigned value, which means this node is made to be not assigned value.
 * \param f be
 */
void be_reset_assigned_var(be_ptr f)
{
	be_check_valid(f);
	f->iaux	= 0;
}

/* \brief decide if a given be node is assigned value.
 * \param f be
 * \return true if assigned; false otherwise.
 */
bool be_is_var_assigned(const be_ptr f)
{
	be_check_valid(f);
	return (bool)f->iaux > 0;
}
