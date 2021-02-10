#ifndef xor_h
#define xor_h

#include <stdio.h>
#include "vec.h"

extern vecp* xor_create(void);
extern void xor_parse(FILE* in, vecp* f);
extern void xor_destroy(vecp* f);
extern int xor_get_maxvar(vecp* f);

#endif
