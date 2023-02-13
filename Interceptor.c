#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

extern int initialized;


int wrap_pthread_create(pthread_t *restrict thread,
                          const pthread_attr_t *restrict attr,
                          void *(*start_routine)(void *),
                          void *restrict arg) {
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