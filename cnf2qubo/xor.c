#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "xor.h"


static char* readFile(FILE *  in);
static void xor_parse_main(char* in, vecp* f);

vecp* xor_create(void)
{
        vecp* f = (vecp*)malloc(sizeof(vecp));
        if (f == NULL) {
                fprintf(stderr, "memory allocation failed\n");
                exit(1);
        }

        vecp_new(f);

        return f;
}

void xor_parse(FILE* in, vecp* f)
{
    char* text = readFile(in);
    xor_parse_main(text, f);
    free(text);
}

void xor_clear(vecp* f)
{
        for (int i = 0; i < vecp_size(f); i++) {
		veci* v = vecp_begin(f)[i]; 
                veci_delete(v);
		free(v);
		vecp_begin(f)[i] = NULL;
        }
	vecp_resize(f, 0);
}



void xor_destroy(vecp* f)
{
        xor_clear(f);
        vecp_delete(f);
        free(f);
}


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

static inline void skipWhitespace(char** in) {
    while ((**in >= 9 && **in <= 13) || **in == 32)
        (*in)++; }

static inline void skipLine(char** in) {
    for (;;){
        if (**in == 0) return;
        if (**in == '\n') { (*in)++; return; }
        (*in)++; } }

// If the returned value is positive, it means a variable index.
// If the returned value is -1 or -2, it means the constant 1 or 0, respectively. 
static inline int parseInt(char** in) {
    int     val = 0;

    skipWhitespace(in);
    if      (**in == 't' || **in == 'T') {
      (*in)++;
      assert((**in >= 9 && **in <= 13) || **in == 32);
      return  -1;
    }
    
    if      (**in == 'f' || **in == 'F') {
      (*in)++;
      assert((**in >= 9 && **in <= 13) || **in == 32);
      return  -2;
    }

    assert(**in != '-');

    if (**in == '+') (*in)++;
    if (**in < '0' || **in > '9') fprintf(stderr, "PARSE ERROR! Unexpected char: %c\n", **in), exit(1);
    while (**in >= '0' && **in <= '9')
        val = val*10 + (**in - '0'),
        (*in)++;
    return val; }

static void readLine(char** in, veci* v) {
    int parsed_lit, parity;
    assert(veci_size(v) == 0);
    parity = 0;
    for (;;){
        parsed_lit = parseInt(in);
        if (parsed_lit == 0) break;

	if (parsed_lit == -1) parity = (parity+1)%2;
        if (parsed_lit > 0) veci_push(v, parsed_lit);
    }

    if (parity == 1) {
	veci_push(v, -2); // even parity
    } else {
	veci_push(v, -1); // odd parity
    }
}

static void xor_parse_main(char* in, vecp* f) {

    for (;;){
        skipWhitespace(&in);
        if (*in == 0)
            break;
        else if (*in == 'c' || *in == 'p')
            skipLine(&in);
        else{
		veci* v = (veci*)malloc(sizeof(veci));
		assert(v != NULL);
		veci_new(v);
		readLine(&in, v);
		if (veci_size(v) > 0) {
			vecp_push(f, v);
		} else {
			free(v);
			v = NULL;
		}
        }
    }
}

int xor_get_maxvar(vecp* f)
{
	int max = 0;

	for (int i = 0; i < vecp_size(f); i++) {
		veci* v = vecp_begin(f)[i];
		for (int j = 0; j < veci_size(v); j++) {
			int val = veci_begin(v)[j];
			if (val > 0) {
				if (max < val) {
					max = val;
				}
			} else {
				assert(val == -1 || val == -2); // parity
			}
		}
	}

	return max;
}



