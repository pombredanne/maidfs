#!/bin/bash

if which pypy >/dev/null; then
    PYTHON=pypy
else
    PYTHON=python
fi

mkdir -p results

for tracefilepath in ../*.json
do
    tracefile=`basename $tracefilepath`
    echo running tests for $tracefile

    echo no compression..
    # No compression
    ${PYTHON} main.py -f $tracefilepath -n            -o results/${tracefile}_nocomp.txt

    echo gzip tests..
    # gzip tests (compress text, compress text and images, compress all)
    ${PYTHON} main.py -f $tracefilepath -c g -r 0.4   -o results/${tracefile}_gzip_text.txt
    ${PYTHON} main.py -f $tracefilepath -c g -r 0.993 -o results/${tracefile}_gzip_text_and_images.txt
    ${PYTHON} main.py -f $tracefilepath -c g -a       -o results/${tracefile}_gzip_all.txt

    echo bzip tests..
    # bzip tests (compress text, compress text and images, compress all)
    ${PYTHON} main.py -f $tracefilepath -c b -r 0.4   -o results/${tracefile}_bzip_text.txt
    ${PYTHON} main.py -f $tracefilepath -c b -r 1.0   -o results/${tracefile}_bzip_text_and_images.txt
    ${PYTHON} main.py -f $tracefilepath -c b -a       -o results/${tracefile}_bzip_all.txt

    echo 7zip tests..
    # 7zip tests (compress text, compress text and images, compress all)
    ${PYTHON} main.py -f $tracefilepath -c 7 -r 0.4   -o results/${tracefile}_7zip_text.txt
    ${PYTHON} main.py -f $tracefilepath -c 7 -r 1.0   -o results/${tracefile}_7zip_text_and_images.txt
    ${PYTHON} main.py -f $tracefilepath -c 7 -a       -o results/${tracefile}_7zip_all.txt

    echo fast gzip tests..
    # Faster algorithm tests (based on gzip; compress only text)
    ${PYTHON} main.py -f $tracefilepath -c f1 -r 0.4  -o results/${tracefile}_f1_text.txt
    ${PYTHON} main.py -f $tracefilepath -c f2 -r 0.4  -o results/${tracefile}_f2_text.txt
    ${PYTHON} main.py -f $tracefilepath -c f3 -r 0.4  -o results/${tracefile}_f3_text.txt
    ${PYTHON} main.py -f $tracefilepath -c f4 -r 0.4  -o results/${tracefile}_f4_text.txt
    ${PYTHON} main.py -f $tracefilepath -c f5 -r 0.4  -o results/${tracefile}_f5_text.txt

    echo better gzip tests..
    # Better algorithm tests (based on gzip; compress only text)
    ${PYTHON} main.py -f $tracefilepath -c g1 -r 0.27 -o results/${tracefile}_g1_r27.txt
    ${PYTHON} main.py -f $tracefilepath -c g2 -r 0.2  -o results/${tracefile}_g2_r20.txt
    ${PYTHON} main.py -f $tracefilepath -c g3 -r 0.14 -o results/${tracefile}_g3_r14.txt
    ${PYTHON} main.py -f $tracefilepath -c g4 -r 0.1  -o results/${tracefile}_g4_r10.txt
    ${PYTHON} main.py -f $tracefilepath -c g5 -r 0.08 -o results/${tracefile}_g5_r08.txt

    echo fast gzip all tests..
    # Faster algorithm tests (based on gzip; compress everything)
    ${PYTHON} main.py -f $tracefilepath -c f1 -a      -o results/${tracefile}_f1_all.txt
    ${PYTHON} main.py -f $tracefilepath -c f2 -a      -o results/${tracefile}_f2_all.txt
    ${PYTHON} main.py -f $tracefilepath -c f3 -a      -o results/${tracefile}_f3_all.txt
    ${PYTHON} main.py -f $tracefilepath -c f4 -a      -o results/${tracefile}_f4_all.txt
    ${PYTHON} main.py -f $tracefilepath -c f5 -a      -o results/${tracefile}_f5_all.txt

    echo better gzip all tests..
    # Better algorithm tests (based on gzip; compress everything)
    ${PYTHON} main.py -f $tracefilepath -c g1 -a      -o results/${tracefile}_g1_all.txt
    ${PYTHON} main.py -f $tracefilepath -c g2 -a      -o results/${tracefile}_g2_all.txt
    ${PYTHON} main.py -f $tracefilepath -c g3 -a      -o results/${tracefile}_g3_all.txt
    ${PYTHON} main.py -f $tracefilepath -c g4 -a      -o results/${tracefile}_g4_all.txt
    ${PYTHON} main.py -f $tracefilepath -c g5 -a      -o results/${tracefile}_g5_all.txt
    
    echo
done
