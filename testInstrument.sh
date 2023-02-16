clang testPrograms/basicMultiThread.c -o basicMultiThread
clang -dynamiclib -Wl MemoryInstrumentation.c -lQBDI -lQBDIPreload -o instrument.dylib
sudo DYLD_INSERT_LIBRARIES=./instrument.dylib ./basicMultiThread
