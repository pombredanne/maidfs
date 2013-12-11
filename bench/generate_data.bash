#!/bin/bash

# Generate 240MB text file
cp /usr/share/dict/words ./240MB.txt
for i in `seq 1 100`; do
    cat /usr/share/dict/words >> ./240MB.txt
done

# Generate 240MB incompressible binary file
dd if=/dev/urandom of=240MB.bin bs=1024 count=245904
