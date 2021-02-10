/** \file     my_hash2.c
 *  \brief    A simple implementation of a chained-hash table (without delete operation)
 *  \author   Takahisa Toda
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "my_def.h"
#include "my_hash2.h"


#define DEFAULT_HASH_SIZE         (UINTMAX_C(1) << 24)  //!< The default number of buckets
#define HASH_ENLARGEMENT_WIDTH    (2)                   //!< the width of bitshift for enlargement
#define HASHCONST                 (31415926525)


/** \brief    Create a hash table.
 *  \param    n     The number of buckets to be created
 *  \return   Pointer to a hash table if successful; otherwise, NULL.
 *  \note     Set a default value to n if n == 0. 
 *  \see      ht2_destroy
 */
my_hash2 *ht2_create(uintmax_t n)
{
  n = (n == 0? DEFAULT_HASH_SIZE: n);

  my_hash2 *h = (my_hash2*) malloc(sizeof(my_hash2));
  ENSURE_TRUE_MSG(h != NULL,"memory allocation failed");

  h->bucket_count = n;
  h->entry_count  = 0;
  h->table        = (struct ht2_entry**) malloc(sizeof(struct ht2_entry*) * n);
  ENSURE_TRUE_MSG(h->table != NULL, "memory allocation failed");
  for(uintmax_t i = 0; i < n; i++) h->table[i] = NULL;

  return h;
}


/** \brief    Clear all entries of a hash table.
 *  \param    h     Pointer to a hash table
 *  \see      ht2_create
 */
void ht2_clear(my_hash2 *h)
{
  assert(h != NULL);
  const uintmax_t n = h->bucket_count;
  for(uintmax_t i = 0; i < n; i++) {
      for(struct ht2_entry *e = h->table[i]; e != NULL; ) {
        struct ht2_entry *t = e->nx;
        free(e);
        e = t;
      }
      h->table[i] = NULL;
  }
  
  h->entry_count  = 0;
}

/** \brief    Free memory area used by a hash table.
 *  \param    h     Pointer to a hash table
 *  \see      ht2_create
 */
void ht2_destroy(my_hash2 *h)
{
  assert(h != NULL);
  const uintmax_t n = h->bucket_count;
  for(uintmax_t i = 0; i < n; i++) {
      for(struct ht2_entry *e = h->table[i]; e != NULL; ) {
        struct ht2_entry *t = e->nx;
        free(e);
        e = t;
      }
  }
  free(h->table); h->table  = NULL;
  free(h);        h         = NULL;
}

/** \brief    Calculate a hash value.
 *  \param    k1     Key (of pointer size)
 *  \param    k2     Key (of pointer size)
 *  \param    n     The number of buckets
 *  \return   The calculated hash value
 */
static inline uintmax_t ht2_hash(intptr_t k1,  intptr_t k2, uintmax_t n)
{
  assert(n > 0);
  uintmax_t val1 = (uintmax_t)(HASHCONST * (k1 >> 3))%n;
  uintmax_t val2 = (uintmax_t)(HASHCONST * (k2 >> 3))%n;

  return (val1+val2)%n;
}

/** \brief    Register an entry if the associated key pair is not yet registered; otherwise, overwrite.
 *  \param    k1     Key (of pointer size)
 *  \param    k2     Key (of pointer size)
 *  \param    v     Value associated with key (of pointer size)
 *  \param    h     Pointer to a hash table
 *  \see      ht2_search
 */
void ht2_set(intptr_t k1, intptr_t k2, double v, my_hash2 *h)
{
  assert(h != NULL);
  const uintmax_t i = ht2_hash(k1, k2, h->bucket_count);
  for(struct ht2_entry *e = h->table[i]; e != NULL; e = e->nx) {
    if(e->key[0] == k1 && e->key[1] == k2) {
      e->val = v; // just overwrite. (Do not count up entry_count!)
      return;
    }
  }

  assert(h != NULL);
  struct ht2_entry *e = (struct ht2_entry*)malloc(sizeof(struct ht2_entry));
  ENSURE_TRUE_MSG(e != NULL, "memory allocation failed");
  e->key[0] = k1;
  e->key[1] = k2;
  e->val = v;

  const uintmax_t j = ht2_hash(k1, k2, h->bucket_count);
  e->nx             = h->table[j];
  h->table[j]       = e;

  h->entry_count++;
}


/** \brief    Remove all occurences of the entry with keys (k1,k2).
 *  \param    k1     Key (of pointer size)
 *  \param    k2     Key (of pointer size)
 *  \param    h     Pointer to a hash table
 *  \see      ht2_search
 */
void ht2_remove(intptr_t k1, intptr_t k2, my_hash2 *h)
{
  assert(h != NULL);
  const uintmax_t i = ht2_hash(k1, k2, h->bucket_count);
  struct ht2_entry *prev = NULL;
  for(struct ht2_entry *e = h->table[i]; e != NULL;) {
    if(e->key[0] == k1 && e->key[1] == k2) {
      if (prev != NULL) {
        prev->nx = e->nx;
      } else {
	h->table[i] = e->nx;
      }
      struct ht2_entry *tmp = e->nx;
      free(e);
      h->entry_count--;
      e = tmp;
    } else {
      prev = e;
      e = e->nx;
    }
  }


}

/** \brief    Find a hash entry. If found, copy the associated value to the location pointed to by pv.
 *  \param    k1     key (of pointer size)
 *  \param    k2     key (of pointer size)
 *  \param    pv    Pointer to a variable, in which the associated value (of pointer size) is copied.
 *  \param    h     Pointer to a hash table
 *  \return   true if found; otherwise, false.
 *  \see      ht2_set
 *  \note
 *  - Value will not be copied if pd == NULL.
 */
bool ht2_search(intptr_t k1, intptr_t k2, double *pv, const my_hash2 *h)
{
  assert(h != NULL);
  const uintmax_t i = ht2_hash(k1, k2, h->bucket_count);
  for(struct ht2_entry *e = h->table[i]; e != NULL; e = e->nx) {
    if(e->key[0] == k1 && e->key[1] == k2) {
      if(pv != NULL) *pv = e->val;
      return true;
    }
  }
  return false;
}


/** \brief   Enlarge a hash table.
 *  \param   h     Pointer to a hash table
 *  \see     ht2_create, ht2_destroy
 */
void ht2_enlarge(my_hash2 *h)
{
  const uintmax_t oldcnt = h->bucket_count;
  ENSURE_TRUE_MSG(oldcnt < (UINTMAX_MAX >> HASH_ENLARGEMENT_WIDTH), "bucket count overflow");
  const uintmax_t newcnt = oldcnt << HASH_ENLARGEMENT_WIDTH;
#ifdef HT_LOG
  printf("hashtable_resizing\t%ju\t%ju\n", oldcnt, newcnt);
#endif /*HT_LOG*/
  struct ht2_entry **oldtable = h->table;
  struct ht2_entry **newtable = (struct ht2_entry**) malloc(sizeof(struct ht2_entry*) * newcnt);
  ENSURE_TRUE_MSG(newtable != NULL, "memory allocation failed");
  for(uintmax_t i = 0; i < newcnt; i++) newtable[i] = NULL;
  for(uintmax_t i = 0; i < oldcnt; i++) {
    for(struct ht2_entry *e = oldtable[i]; e != NULL;) {
      struct ht2_entry *t  = e->nx;
      const uintmax_t j   = ht2_hash(e->key[0], e->key[1], newcnt);
      e->nx       = newtable[j];
      newtable[j] = e;      
      e           = t;
    }
  }
  free(oldtable); oldtable = NULL;
  h->bucket_count = newcnt;
  h->table        = newtable;
}
