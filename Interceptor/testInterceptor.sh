clang -Wl,-rpath=$(dirname $(clang --print-file-name=libclang_rt.asan-aarch64.so)) -fsanitize=address  -static-libsan -fPIC -c Interceptor.c -o intercept.a 
clang -Wl -fsanitize=address intercept.a -o testIntercept.elf ../testPrograms/basicMultithread.c -lpthread
./testIntercept.elf
#LD_PRELOAD=./intercept.so ./testIntercept.elf