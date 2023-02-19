clang testPrograms/basicMultiThread.c -o basicMultiThread.elf -lpthread
mkdir build
rm build/libmyclient.so
cd build
cmake ../
make
cd ../
DynamoRIO/bin64/drrun -c build/libmyclient.so -- basicMultiThread.elf