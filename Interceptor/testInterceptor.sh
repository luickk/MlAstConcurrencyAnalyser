clang -fsanitize=address -shared -fpic Interceptor.c -o intercept.so 
export LD_LIBRARY_PATH=/usr/lib/llvm-10/lib/clang/10.0.0/lib/linux
clang -Wl,-rpath=./ -fsanitize=address -shared-libsan intercept.so -o testIntercept.elf ../testPrograms/basicMultithread.c -lpthread
./testIntercept.elf