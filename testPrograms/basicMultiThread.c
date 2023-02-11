// from here: https://gist.github.com/vaclavbohac/956073
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


void *hello(void* par)
{
	int *ppar = (int *) par;
	int thrid = ppar[0];
	puts("Hello, from thread!");
	pthread_exit((void *) -thrid);
}


int main(void)
{
	int i, ret, numthreads = 2;
	void *thread_status[numthreads];
	int thread_param[numthreads][1];
	pthread_t thread[numthreads];

	// Set thread ids.
	for (i = 0; i < numthreads; i++) {
		thread_param[i][0] = i + 1;
	}

	puts("Hello, from main!");

	// Create threads.
	for (i = 0; i < numthreads; i++) {
		ret = pthread_create(&thread[i], NULL, hello, thread_param[i]);
		if (ret) {
			perror("Error while creating thread");
		}
	}

	// Wait for all threads.
	for (i = 0; i < numthreads; i++) {
		pthread_join(thread[i], &thread_status[i]);
	}

	return EXIT_SUCCESS;
}