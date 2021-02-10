#ifndef cnf_h
#define cnf_h

#include <stdio.h>
#include "vec.h"

// Type definitions
typedef vecp cnf;
typedef vecp* cnf_ptr;

typedef veci clause;
typedef veci* clause_ptr;

// DIMACS  CNF parser
extern void parse_DIMACS(FILE * in, cnf_ptr f);

// Cnf functions
extern cnf_ptr cnf_create(void);
extern void cnf_destroy(cnf_ptr f);
extern void cnf_clear(cnf_ptr f);
extern int cnf_get_maxvar(const cnf_ptr f);
extern int cnf_get_size(const cnf_ptr f);
extern clause_ptr cnf_get(const cnf_ptr f, const int pos);
extern int cnf_push(cnf_ptr f, const clause_ptr cls);
extern clause_ptr cnf_replace(cnf_ptr f, const int pos, const clause_ptr cls);

extern void cnf_check_valid(const cnf_ptr f);

// Clause functions
extern clause_ptr clause_create(void);
extern void clause_destroy(clause_ptr cls);
extern void clause_clear(clause_ptr cls);
extern int clause_get_size(const clause_ptr cls);
extern int clause_get(const clause_ptr cls, const int pos);
extern int clause_push(clause_ptr cls, const int lit);
extern void clause_replace(clause_ptr cls, const int pos, const int lit);

extern void clause_check_valid(const clause_ptr cls);
#endif
