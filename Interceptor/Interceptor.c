#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

extern int __interceptor_pthread_create(pthread_t *restrict thread,
                          const pthread_attr_t *restrict attr,
                          void *(*start_routine)(void *),
                          void *restrict arg);
extern int pthread_create(pthread_t *restrict thread,
                          const pthread_attr_t *restrict attr,
                          void *(*start_routine)(void *),
                          void *restrict arg) {
  printf("pthread_create called \n");
  return __interceptor_pthread_create(thread, attr, start_routine, arg);
}



// void pthread_join() {
//   printf("pthread_join called \n");
// }
