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
    ${PYTHON} main.py -f $tracefilepath -n            -o results/trace.txt

    echo gzip tests..
    # gzip tests (compress text, compress text and images, compress all)
    ${PYTHON} main.py -f $tracefilepath -c g -r 0.4   -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g -r 0.993 -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g -a       -o results/trace.txt

    echo bzip tests..
    # bzip tests (compress text, compress text and images, compress all)
    ${PYTHON} main.py -f $tracefilepath -c b -r 0.4   -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c b -r 1.0   -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c b -a       -o results/trace.txt

    echo 7zip tests..
    # 7zip tests (compress text, compress text and images, compress all)
    ${PYTHON} main.py -f $tracefilepath -c 7 -r 0.4   -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c 7 -r 1.0   -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c 7 -a       -o results/trace.txt

    echo fast gzip tests..
    # Faster algorithm tests (based on gzip; compress only text)
    ${PYTHON} main.py -f $tracefilepath -c f1 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f2 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f3 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f4 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f5 -r 0.4  -o results/trace.txt

    echo better gzip tests..
    # Better algorithm tests (based on gzip; compress only text)
    ${PYTHON} main.py -f $tracefilepath -c g1 -r 0.27 -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g2 -r 0.2  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g3 -r 0.14 -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g4 -r 0.1  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g5 -r 0.08 -o results/trace.txt

    echo fast gzip all tests..
    # Faster algorithm tests (based on gzip; compress everything)
    ${PYTHON} main.py -f $tracefilepath -c f1 -a      -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f2 -a      -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f3 -a      -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f4 -a      -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f5 -a      -o results/trace.txt

    echo better gzip all tests..
    # Better algorithm tests (based on gzip; compress everything)
    ${PYTHON} main.py -f $tracefilepath -c g1 -a      -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g2 -a      -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g3 -a      -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g4 -a      -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c g5 -a      -o results/trace.txt

    echo
done
