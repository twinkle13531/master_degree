#ifndef be_h
#define be_h

#include <stdbool.h>
#include <stdint.h>

#include "vec.h"

enum BeType_Tag {
	ATOM=1,
	OR,
	AND,
	NOT
};

// Type of be node
typedef enum BeType_Tag BeType;

// Boolean expression node
struct be_tag {
	// public:
	BeType type;
	struct be_tag*	left;
	struct be_tag*	right;

	// private:
	intptr_t	iaux;    // auxiliary field for integer value.
	bool  checked; // used for efficient be traversal.
};

typedef struct be_tag be;
typedef be* be_ptr;

// Major Be functions
extern void be_init(void);
extern void be_quit(void);
extern be_ptr be_find_node(const BeType type, const be_ptr left, const be_ptr right);
extern void be_uncheck_recur(be_ptr be);

extern void be_check_valid(const be_ptr f);

extern bool be_is_checked(const be_ptr f);
extern void be_check(const be_ptr f);
extern BeType be_get_type(const be_ptr f);
extern be_ptr be_get_left(const be_ptr f);
extern be_ptr be_get_right(const be_ptr f);

extern void be_collect_inputs(const be_ptr g, veci* vars);

extern void be_compute_assignment_01_version(int* assign, const be_ptr g, const int size);

// Optional Be functions
extern void be_assign_vars(be_ptr f, const int init_var);
extern int be_get_assigned_var(const be_ptr f);
extern void be_reset_assigned_var(be_ptr f);
extern bool be_is_var_assigned(const be_ptr f);

#endif
