#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include "dr_api.h"
#include "drmgr.h"
#include "drreg.h"
#include "drutil.h"
#include "drx.h"

#include "include/types.h"
#include "include/memtrace.h"

// todo => shrink to 8 bytes. Should be possible if memory address access/accessing only store 
// bytes of the virtual address that define the memory locations relative to the process pages)
// reference: https://developer.arm.com/documentation/den0024/a/The-Memory-Management-Unit/Translating-a-Virtual-Address-to-a-Physical-Address
// abstract: only the last 28 bits of an virtual address encode the actual loation(or index) of the address, the rest is context
typedef struct MemoryAccess {
   usize address_accessed;
   u64 size;
   u32 thread_id;
} MemoryAccess;

typedef struct LockAccess {
   usize lock_address;
   u32 thread_id;
} LockAccess;

const u64 linear_set_size_increment = 10000;

MemoryAccess *mem_read_set;
u64 mem_read_set_capacity = linear_set_size_increment;
u64 mem_read_set_len = 0;

MemoryAccess *mem_write_set;
u64 mem_write_set_capacity = linear_set_size_increment;
u64 mem_write_set_len = 0;

LockAccess *lock_unlock_set;
u64 lock_unlock_set_capacity = linear_set_size_increment;
u64 lock_unlock_set_len = 0;

LockAccess *lock_lock_set;
u64 lock_lock_set_capacity = linear_set_size_increment;
u64 lock_lock_set_len = 0;


void memtrace_init() { 
    mem_read_set = (MemoryAccess*)malloc(sizeof(MemoryAccess)*mem_read_set_capacity);
    if (mem_read_set == NULL) {
        printf("set allocation error \n");
    }
    mem_write_set = (MemoryAccess*)malloc(sizeof(MemoryAccess)*mem_write_set_capacity);
    if (mem_write_set == NULL) {
        printf("set allocation error \n");
    }

    lock_lock_set = (LockAccess*)malloc(sizeof(LockAccess)*lock_unlock_set_capacity);
    if (lock_lock_set == NULL) {
        printf("set allocation error \n");
    }
    lock_unlock_set = (LockAccess*)malloc(sizeof(LockAccess)*lock_lock_set_capacity);
    if (lock_unlock_set == NULL) {
        printf("set allocation error \n");
    }
}

void *increase_set_capacity(void *set, u64 *set_capacity) {
    *set_capacity += linear_set_size_increment;
    void *ret = realloc(set, *set_capacity);
    if (ret == NULL) {
        printf("set allocation error \n");
    }
    return ret;
}

// this is an event like fn that is envoked on every memory access (called by DynamRIO)
void memtrace(void *drcontext) {
    per_thread_t *data;
    mem_ref_t *mem_ref, *buf_ptr;

    data = drmgr_get_tls_field(drcontext, tls_idx);
    buf_ptr = BUF_PTR(data->seg_base);
    
    /* We use libc's fprintf as it is buffered and much faster than dr_fprintf
     * for repeated printing that dominates performance, as the printing does here.
     */
    for (mem_ref = (mem_ref_t *)data->buf_base; mem_ref < buf_ptr; mem_ref++) {
        if (mem_ref->type < REF_TYPE_WRITE) {
            if (mem_ref->type == REF_TYPE_WRITE) {
                // mem write
                if (mem_write_set_len >= mem_write_set_capacity) mem_write_set = increase_set_capacity(mem_write_set, &mem_write_set_capacity);
                mem_write_set[mem_write_set_len].address_accessed = mem_ref->addr;
                mem_write_set[mem_write_set_len].size = mem_ref->size;
                mem_write_set_len += 1;
            } else {
                // mem read
                if (mem_read_set_len >= mem_read_set_capacity) mem_read_set = increase_set_capacity(mem_read_set, &mem_read_set_capacity);
                mem_read_set[mem_read_set_len].address_accessed = mem_ref->addr;
                mem_read_set[mem_read_set_len].size = mem_ref->size;
                mem_read_set_len += 1;
            }
        }
        /* We use PIFX to avoid leading zeroes and shrink the resulting file. */
        fprintf(data->logf, "" PIFX ": %2d, %s\n", (ptr_uint_t)mem_ref->addr,
                mem_ref->size,
                (mem_ref->type > REF_TYPE_WRITE)
                    ? decode_opcode_name(mem_ref->type) /* opcode for instr */
                    : (mem_ref->type == REF_TYPE_WRITE ? "w" : "r"));
        data->num_refs++;
    }
    BUF_PTR(data->seg_base) = data->buf_base;
}