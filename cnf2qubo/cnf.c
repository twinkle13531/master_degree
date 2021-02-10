#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<assert.h>

#include "cnf.h"

static char* readFile(FILE *  in);
static void readClause(char** in, clause_ptr lits);
static void parse_DIMACS_main(char* in, cnf_ptr f);
static inline int parseInt(char** in);
static inline void skipLine(char** in);
static inline void skipWhitespace(char** in);

static void cnf_check_out_of_bound(const cnf_ptr f, const int pos);
static void clause_check_out_of_bound(const clause_ptr cls, const int pos);

//=================================================================================================
// Helpers:


// Reads an input stream to end-of-file and returns the result as a 'char*' terminated by '\0'
// (dynamic allocation in case 'in' is standard input).
//
static char* readFile(FILE *  in)
{
    char*   data = malloc(65536);
    int     cap  = 65536;
    int     size = 0;

    while (!feof(in)){
        if (size == cap){
            cap *= 2;
            data = realloc(data, cap); }
        size += fread(&data[size], 1, 65536, in);
    }
    data = realloc(data, size+1);
    data[size] = '\0';

    return data;
}

//static inline double cpuTime(void) {
//    struct rusage ru;
//    getrusage(RUSAGE_SELF, &ru);
//    return (double)ru.ru_utime.tv_sec + (double)ru.ru_utime.tv_usec / 1000000; }


//=================================================================================================
// DIMACS Parser:

/* \brief Parses DIMACS CNF and set the internal data structure of cnf.
 * \param in input file
 * \param f  empty CNF
 */
void parse_DIMACS(FILE * in, cnf_ptr f) {
		cnf_check_valid(f);
    char* text = readFile(in);
    parse_DIMACS_main(text, f);
    free(text);
}

static inline void skipWhitespace(char** in) {
    while ((**in >= 9 && **in <= 13) || **in == 32)
        (*in)++; }

static inline void skipLine(char** in) {
    for (;;){
        if (**in == 0) return;
        if (**in == '\n') { (*in)++; return; }
        (*in)++; } }

static inline int parseInt(char** in) {
    int     val = 0;
    int    _neg = 0;
    skipWhitespace(in);
    if      (**in == '-') _neg = 1, (*in)++;
    else if (**in == '+') (*in)++;
    if (**in < '0' || **in > '9') fprintf(stderr, "PARSE ERROR! Unexpected char: %c\n", **in), exit(1);
    while (**in >= '0' && **in <= '9')
        val = val*10 + (**in - '0'),
        (*in)++;
    return _neg ? -val : val; }

static void readClause(char** in, clause_ptr cls) {
    int parsed_lit, var;
		clause_clear(cls);
    for (;;){
        parsed_lit = parseInt(in);
        if (parsed_lit == 0) break;
				clause_push(cls, parsed_lit);
    }
}

static void parse_DIMACS_main(char* in, cnf_ptr f) {

    for (;;){
        skipWhitespace(&in);
        if (*in == 0)
            break;
        else if (*in == 'c' || *in == 'p')
            skipLine(&in);
        else{
    				clause_ptr cls = clause_create();
            readClause(&in, cls);
						if (clause_get_size(cls) > 0) {
							cnf_push(f, cls);
						} else {
							clause_destroy(cls);
						}
        }
    }
}

//=================================================================================================
// Cnf Functions:

/* \brief Creates an empty CNF.
 * \see cnf_destroy, cnf_clear
 */
cnf_ptr cnf_create(void)
{
	cnf_ptr f = (cnf_ptr)malloc(sizeof(cnf));
	if (f == NULL) {
		fprintf(stderr, "memory allocation failed\n");
		exit(1);
	}

	vecp_new(f);

	return f;
}

/* \brief Destorys a given CNF: all clauses contained are also destroyed.
 * \param f cnf
 * \see cnf_clear, cnf_create
 */
void cnf_destroy(cnf_ptr f)
{
	cnf_check_valid(f);

	cnf_clear(f);

	vecp_delete(f);
	free(f);
}

/* \brief Clears a given CNF and makes it empty: CNF itself is not destroyed, but all claused contained are destoryed.
 * \param f cnf
 */
void cnf_clear(cnf_ptr f)
{
	cnf_check_valid(f);

	const int nof_clauses = cnf_get_size(f);

	for (int i = 0; i < nof_clauses; i++) {
		clause_ptr cls = cnf_get(f, i);
		clause_check_valid(cls);
		clause_destroy(cls);
	}

}

/* \brief Checks if a given cnf is valid.
 * \param f cnf
 */
void cnf_check_valid(const cnf_ptr f)
{
	if (f == NULL) {
		fprintf(stderr, "invalid cnf\n");
		exit(1);
	}
}

/* \brief Gets the maximum value of a variable.
 * \param f cnf
 * \return the maximum variable if CNF is nonempty; -1 otherwise.
 * \note Assume variables are non-negative integers.
 */
int cnf_get_maxvar(const cnf_ptr f)
{
	cnf_check_valid(f);

	int max = -1;

	const int nof_clauses = cnf_get_size(f);

	for (int i = 0; i < nof_clauses; i++) {
		clause_ptr cls = cnf_get(f,i);
		clause_check_valid(cls);

		const int nof_literals = clause_get_size(cls);

		for (int j = 0; j < nof_literals; j++) {
			int literal = clause_get(cls, j);
			int var = abs(literal);

			max = max < var? var: max;
		}
	}

	return max;
}

/* \brief Gets the number of clauses
 * \param f cnf
 * \return the number of clauses
 */
int cnf_get_size(const cnf_ptr f)
{
	cnf_check_valid(f);

	return vecp_size(f);	
}

/* \brief Gets the clause of a given position.
 * \param f cnf
 * \param pos position of clause, which ranges from 0 to the number of clauses minus 1.
 * \return the clause of a given position.
 * \see cnf_push
 */
clause_ptr cnf_get(const cnf_ptr f, const int pos)
{
	cnf_check_valid(f);

	cnf_check_out_of_bound(f, pos);

	return (clause_ptr)vecp_begin(f)[pos];
}

/* \brief Pushes a given clause.
 * \param f cnf
 * \param cls clause
 * \return the position at which a clause is pushed.
 * \see cnf_get
 */
int cnf_push(cnf_ptr f, const clause_ptr cls)
{
	cnf_check_valid(f);
	clause_check_valid(cls);

	vecp_push(f, (void*)cls);

	return vecp_size(f)-1;
}

/* \brief Replaces the clause of a given position with a given clause.
 * \param f cnf
 * \param pos position
 * \param cls clause
 * \return the replaced clause.
 * \see cnf_push
 */
clause_ptr cnf_replace(cnf_ptr f, const int pos, const clause_ptr cls)
{
	cnf_check_valid(f);
	clause_check_valid(cls);

	cnf_check_out_of_bound(f, pos);

	clause_ptr old = vecp_begin(f)[pos];

	vecp_begin(f)[pos] = cls;

	return old;
}

/* \brief Checks if out of bound error occurs.
 * \param f cnf
 * \param pos position
 */
static void cnf_check_out_of_bound(const cnf_ptr f, const int pos)
{
	if (!(0 <= pos && pos < vecp_size(f))) {
		fprintf(stderr, "out of bound error\n");
		exit(1);
	}
}

//=================================================================================================
// Clause Functions:

/* \brief Creates empty clause.
 * \see clause_destory, clause_clear
 */
clause_ptr clause_create(void)
{
	clause_ptr cls = (clause_ptr)malloc(sizeof(clause));
	if (cls == NULL) {
		fprintf(stderr, "memory allocation failed\n");
		exit(1);
	}

	veci_new(cls);

	return cls;
}

/* \brief Destorys a clause.
 * \param cls clause
 * \see clause_create, clause_clear
 */
void clause_destroy(clause_ptr cls)
{
	clause_check_valid(cls);
	veci_delete(cls);	
	free(cls);
}

/* \brief Clears all literals and makes it empty.
 * \param cls clause
 * \see clause_destory
 */
void clause_clear(clause_ptr cls)
{
	clause_check_valid(cls);

	veci_resize(cls, 0);
}

/* \brief Gets the number of literals
 * \param cls clause
 * \return the number of literals
 */
int clause_get_size(const clause_ptr cls)
{
	clause_check_valid(cls);

	return veci_size(cls);
}

/* \brief Gets the literal of a given position.
 * \param cls clause
 * \param pos position, which ranges from 0 to the size of clause minus 1.
 * \return the literal of a given position.
 * \see clause_push
 */
int clause_get(const clause_ptr cls, const int pos)
{
	clause_check_valid(cls);

	clause_check_out_of_bound(cls, pos);

	return veci_begin(cls)[pos];
}

/* \brief Pushes a given literal.
 * \param cls clause
 * \param lit literal
 * \return the position at which the literal is pushed.
 * \see clause_get
 */
int clause_push(clause_ptr cls, const int lit)
{
	clause_check_valid(cls);

	veci_push(cls, lit);

	return veci_size(cls)-1;
}

/* \brief Replaces the literal at a given position with a given literal.
 * \param cls clause
 * \param pos position
 * \param lit literal
 */
void clause_replace(clause_ptr cls, const int pos, const int lit)
{
	clause_check_valid(cls);

	clause_check_out_of_bound(cls, pos);

	veci_begin(cls)[pos] = lit;
}

/* \brief Checks if a given clause is valid.
 * \param cls clause
 */
void clause_check_valid(const clause_ptr cls)
{
	if (cls == NULL) {
		fprintf(stderr, "invalid clause\n");
		exit(1);
	}
}

/* \brief Checks if out of bound error occurs.
 * \param cls clause
 * \param pos position
 */
static void clause_check_out_of_bound(const clause_ptr cls, const int pos)
{
	if (!(0 <= pos && pos < veci_size(cls))) {
		fprintf(stderr, "out of bound error\n");
		exit(1);
	}
}
