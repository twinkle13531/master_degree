#ifndef be_qubo_h
#define be_qubo_h

#include "be.h"
#include "qubo.h"

extern int beIsing_compute_qubo(qubo_ptr q, const be_ptr f);

extern int beIsing_get_mininumEnergy_or(qubo_var_type type);
extern int beIsing_get_mininumEnergy_and(qubo_var_type type);
extern int beIsing_get_mininumEnergy_not(qubo_var_type type);
extern int beIsing_get_mininumEnergy_one(qubo_var_type type);



#endif
