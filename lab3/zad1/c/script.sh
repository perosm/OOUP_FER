#! /bin/bash
gcc main.c myfactory.c -ldl # ldl je za libdl biblioteku
gcc -shared -fPIC tiger.c -o tiger.so # 
gcc -shared -fPIC parrot.c -o parrot.so
./a.out 0 tiger mirko parrot modrobradi