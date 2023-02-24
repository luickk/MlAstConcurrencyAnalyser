#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <pthread.h>
#include "dr_api.h"
#include "drmgr.h"
#include "drreg.h"
#include "drutil.h"
#include "drx.h"

#include "include/memtrace.h"

#define MAX_THREADS 100
const u64 linear_set_size_increment = 1000000;

// todo => shrink to 8 bytes. Should be possible if memory address access/accessing only store 
// bytes of the virtual address that define the memory locations relative to the process pages)
// reference: https://developer.arm.com/documentation/den0024/a/The-Memory-Management-Unit/Translating-a-Virtual-Address-to-a-Physical-Address
// abstract: only the last 28 bits of an virtual address encode the actual loation(or index) of the address, the rest is context
typedef struct MemoryAccess {
   usize address_accessed;
   u16 opcode;
   u64 size;
   u32 thread_id;
} MemoryAccess;

typedef struct LockAccess {
   usize lock_address;
   u32 thread_id;
} LockAccess;

typedef struct ThreadState {
    u64 idx;
    MemoryAccess *mem_read_set;
    u64 mem_read_set_capacity;
    u64 mem_read_set_len;

    MemoryAccess *mem_write_set;
    u64 mem_write_set_capacity;
    u64 mem_write_set_len;

    LockAccess *lock_unlock_set;
    u64 lock_unlock_set_capacity;
    u64 lock_unlock_set_len;

    LockAccess *lock_lock_set;
    u64 lock_lock_set_capacity;
    u64 lock_lock_set_len;
} ThreadState;
ThreadState threads[MAX_THREADS] = {};
u64 n_threads = 0;

extern int initialized;


int wrap_pthread_create(pthread_t *restrict thread, const pthread_attr_t *restrict attr, void *(*start_routine)(void *), void *restrict arg) {
  if (initialized)
    printf("pthread_create called \n");
  return pthread_create(thread, attr, start_routine, arg);
}


int wrap_pthread_join(pthread_t thread, void **retval) {
  if (initialized)
    printf("pthread_join called \n");
  return pthread_join(thread, retval);
}

void *wrap_malloc(size_t size) {
  if (initialized)
    printf("malloc size %zu called \n", size);
  void *ret = malloc(size);
  return ret;
}

void wrap_free(void *ptr) {
  if (initialized)
    printf("free on %p called \n", ptr);
  free(ptr);
}


__attribute__((used, section("__DATA, __interpose")))
static void *const interpose[] = {(void *)wrap_pthread_create, (void *)pthread_create, (void *)wrap_pthread_join, (void *)pthread_join, (void *)malloc, (void *)wrap_malloc, (void *)free, (void *)wrap_free };

i64 findThreadByTlsIdx(u64 idx) {
    u64 i;
    for (i = 0; i <= n_threads; i++) {
        if (threads[i].idx == idx) {
            return i;
        }
    }
    return -1;
}

void mem_analyse_exit() { 
    u64 j;
    for (j = 0; j < n_threads; j++) {
        u64 i;
        printf("mem_write_set_len: %ld \n", threads[j].mem_write_set_len);
        printf("mem_read_set_len: %ld \n", threads[j].mem_read_set_len);
        // for (i = 0; i < threads[j].mem_write_set_len; i++) {
        //     printf("[%d]tid write access to address: %ld, size: %ld, opcode: %s \n", threads[j].mem_write_set[i].thread_id, threads[j].mem_write_set[i].address_accessed, threads[j].mem_write_set[i].size, (threads[j].mem_read_set[i].opcode > REF_TYPE_WRITE) ? decode_opcode_name(threads[j].mem_read_set[i].opcode) /* opcode for instr */ : (threads[j].mem_read_set[i].opcode == REF_TYPE_WRITE ? "w" : "r"));        
        // }
        // for (i = 0; i < threads[j].mem_read_set_len; i++) {
        //     printf("[%d]tid read access to address: %ld, size: %ld, opcode: %s \n", threads[j].mem_write_set[i].thread_id, threads[j].mem_read_set[i].address_accessed, threads[j].mem_read_set[i].size, (threads[j].mem_read_set[i].opcode > REF_TYPE_WRITE) ? decode_opcode_name(threads[j].mem_read_set[i].opcode) /* opcode for instr */ : (threads[j].mem_read_set[i].opcode == REF_TYPE_WRITE ? "w" : "r"));
        // }

        free(threads[j].mem_write_set);
        free(threads[j].mem_read_set);
        free(threads[j].lock_lock_set);
        free(threads[j].lock_unlock_set);
    }
}

u32 mem_analyse_init() { 
        return 1;
}

u32 mem_analyse_new_thread_init() {
    printf("new thread inited \n");
    if (n_threads >= MAX_THREADS) return 0;
    threads[n_threads].idx = tls_idx;

    threads[n_threads].mem_read_set = (MemoryAccess*)malloc(sizeof(MemoryAccess) * linear_set_size_increment);
    threads[n_threads].mem_read_set_capacity = linear_set_size_increment;
    if (threads[n_threads].mem_read_set == NULL) {
        printf("set allocation error \n");
        return 0;    
    }
    threads[n_threads].mem_write_set = (MemoryAccess*)malloc(sizeof(MemoryAccess) * linear_set_size_increment);
    threads[n_threads].mem_write_set_capacity = linear_set_size_increment;
    if (threads[n_threads].mem_write_set == NULL) {
        printf("set allocation error \n");
        return 0;
    }

    threads[n_threads].lock_lock_set = (LockAccess*)malloc(sizeof(LockAccess) * linear_set_size_increment);
    threads[n_threads].lock_lock_set_capacity = linear_set_size_increment;
    if (threads[n_threads].lock_lock_set == NULL) {
        printf("set allocation error \n");
        return 0;
    }
    threads[n_threads].lock_unlock_set = (LockAccess*)malloc(sizeof(LockAccess) * linear_set_size_increment);
    threads[n_threads].lock_unlock_set_capacity = linear_set_size_increment;    
    if (threads[n_threads].lock_unlock_set == NULL) {
        printf("set allocation error \n");
        return 0;
    }

    n_threads += 1;
    return 1;
}

void mem_analyse_thread_exit() {
    printf("thread exit \n");
}

void *increase_set_capacity(void *set, u64 *set_capacity) {
    *set_capacity += linear_set_size_increment;
    printf("new set_capacity: %ld \n", *set_capacity);
    return realloc(set, *set_capacity);
}

// this is an event like fn that is envoked on every memory access (called by DynamRIO)
void memtrace(void *drcontext) {
    per_thread_t *data;
    mem_ref_t *mem_ref, *buf_ptr;

    data = drmgr_get_tls_field(drcontext, tls_idx);
    buf_ptr = BUF_PTR(data->seg_base);
    
    i64 t_index = findThreadByTlsIdx(tls_idx);
    if (t_index < 0) {
        printf("error finding tls_idx. %ld \n", t_index);
        return;    
    }
    ThreadState *curr_thread = &threads[t_index];
    for (mem_ref = (mem_ref_t *)data->buf_base; mem_ref < buf_ptr; mem_ref++) {
        if (mem_ref->type == 1 || mem_ref->type == 457 || mem_ref->type == 458 || mem_ref->type == 456 || mem_ref->type == 568) {
            // mem write
            if (curr_thread->mem_write_set_len >= curr_thread->mem_write_set_capacity) curr_thread->mem_write_set = increase_set_capacity(curr_thread->mem_write_set, &curr_thread->mem_write_set_capacity);
            if (curr_thread->mem_write_set == NULL) exit(1);
            curr_thread->mem_write_set[curr_thread->mem_write_set_len].address_accessed = (usize)mem_ref->addr;
            curr_thread->mem_write_set[curr_thread->mem_write_set_len].opcode = mem_ref->type;
            curr_thread->mem_write_set[curr_thread->mem_write_set_len].thread_id = tls_idx;
            curr_thread->mem_write_set[curr_thread->mem_write_set_len].size = mem_ref->size;
            curr_thread->mem_write_set_len += 1;
        } else if(mem_ref->type == 0 || mem_ref->type == 227 || mem_ref->type == 225 || mem_ref->type == 197 || mem_ref->type == 228 || mem_ref->type == 229 || mem_ref->type == 299 || mem_ref->type == 173) {
            // mem read
            if (curr_thread->mem_read_set_len >= curr_thread->mem_read_set_capacity) curr_thread->mem_read_set = increase_set_capacity(curr_thread->mem_read_set, &curr_thread->mem_read_set_capacity);
            if (curr_thread->mem_read_set == NULL) exit(1);
            curr_thread->mem_read_set[curr_thread->mem_read_set_len].address_accessed = (usize)mem_ref->addr;
            curr_thread->mem_read_set[curr_thread->mem_read_set_len].opcode = mem_ref->type;
            curr_thread->mem_read_set[curr_thread->mem_read_set_len].thread_id = tls_idx;
            curr_thread->mem_read_set[curr_thread->mem_read_set_len].size = mem_ref->size;
            curr_thread->mem_read_set_len += 1;
        }
        //  else {
        //     printf("missed %d \n", mem_ref->type);        
        // }
        // // /* We use PIFX to avoid leading zeroes and shrink the resulting file. */
        // fprintf(data->logf, "" PIFX ": %2d, %s (%d)\n", (ptr_uint_t)mem_ref->addr, mem_ref->size, (mem_ref->type > REF_TYPE_WRITE) ? decode_opcode_name(mem_ref->type) /* opcode for instr */ : (mem_ref->type == REF_TYPE_WRITE ? "w" : "r"), mem_ref->type);
        data->num_refs++;
    }
    BUF_PTR(data->seg_base) = data->buf_base;
}
