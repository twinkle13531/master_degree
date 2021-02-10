#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<stdbool.h>
#include<assert.h>

#include "be_dot.h"

#define DEFAULT_GRAPH_NAME "be_structure"

static void beDot_print_recur(FILE* out, be_ptr g);


void beDot_print(FILE* out, const char *graph_name, be_ptr g)
{
	fprintf(out, "digraph %s {\n", 
		graph_name == NULL? DEFAULT_GRAPH_NAME: graph_name);

	assert(!be_is_checked(g));	
	beDot_print_recur(out, g);
	be_uncheck_recur(g);

	fprintf(out, "}\n");
}

static void beDot_print_recur(FILE* out, be_ptr g)
{
	if (g == NULL || be_is_checked(g)) return;

	if (be_get_type(g) == ATOM) {
		int z = be_get_assigned_var(g);     // output
		fprintf(out, "%d;\n", z);

	} else if (be_get_type(g) == NOT) {
		be_ptr left  = be_get_left(g);
		int x = be_get_assigned_var(left);  // input
		int z = be_get_assigned_var(g);     // output

		fprintf(out, "%d [label = \"NOT(%d)\"];\n", z,z);
		fprintf(out, "%d -> %d;\n", x, z);

 	} else {
		be_ptr left  = be_get_left(g);
		be_ptr right = be_get_right(g);

		beDot_print_recur(out, left);
		beDot_print_recur(out, right);

		int x = be_get_assigned_var(left);  // input
		int y = be_get_assigned_var(right); // input
		int z = be_get_assigned_var(g);     // output

		switch(be_get_type(g)) {
			case OR:
				fprintf(out, "%d [label = \"OR(%d)\"];\n", z,z);
				break;
			case AND:
				fprintf(out, "%d [label = \"AND(%d)\"];\n", z,z);
				break;
			default:
				fprintf(stderr, "invalid be node type\n");
				exit(1);
				break; 
		}

		fprintf(out, "%d -> %d;\n", x, z);
		fprintf(out, "%d -> %d;\n", y, z);

	}

	be_check(g);

}
