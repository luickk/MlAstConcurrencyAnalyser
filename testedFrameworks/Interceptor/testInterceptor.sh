clang -dynamiclib -Wl,-U,_initialized Interceptor.c -o testPrograms/intercept.dylib  # or use -Wl,-undefined,dynamic_lookup
clang testPrograms/basicMultithread.c testPrograms/intercept.dylib -o testPrograms/testIntercept
./testPrograms/testIntercept