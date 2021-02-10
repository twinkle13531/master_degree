/** \file     my_hash2.h
 *  \brief    A chained-hash table (without delete operation)
 *  \author   Takahisa Toda
 */
#ifndef MY_HASH2_H
#define MY_HASH2_H

#include <stdint.h>
#include <stdbool.h>

/*---------------------------------------------------------------------------*/
/* Type declarations                                                         */
/*---------------------------------------------------------------------------*/

/** \brief    Key-value pair */
struct ht2_entry {
  intptr_t         key[2];
  double         val;
  struct  ht2_entry  *nx;
};

/** \brief    Hash table (chaining)*/
typedef struct {
  uintmax_t         bucket_count;   //!< the number of buckets
  uintmax_t         entry_count;    //!< the number of hash table entries
  struct ht2_entry   **table;        //!< an array of buckets
} my_hash2;


/*---------------------------------------------------------------------------*/
/* Function prototypes                                                       */
/*---------------------------------------------------------------------------*/

extern my_hash2    *ht2_create      (uintmax_t n);
extern void       ht2_destroy      (my_hash2 *h);
extern void       ht2_set          (intptr_t k1, intptr_t k2, double v, my_hash2 *h);
extern bool       ht2_search       (intptr_t k1, intptr_t k2, double *pv, const my_hash2 *h);
extern void       ht2_enlarge      (my_hash2 *h);

extern void       ht2_clear        (my_hash2 *h);
extern void       ht2_remove       (intptr_t k1, intptr_t k2, my_hash2 *h);


/** \brief    Compute a load factor.
 *  \param    h     Pointer to a hash table
 *  \return   The computed load factor
 */
static inline double ht2_loadfactor(const my_hash2 *h)
{
  return (double)h->entry_count/h->bucket_count;
}

#endif /*MY_HASH2_H*/
