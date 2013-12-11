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
    ${PYTHON} main.py -f $tracefilepath -c f1  -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f2  -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f3  -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f4  -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f5  -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f6  -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f7  -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f8  -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f9  -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f10 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f11 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f12 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f13 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f14 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f15 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f16 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f17 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f18 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f19 -r 0.4  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f20 -r 0.4  -o results/trace.txt

    echo fast gzip all tests..
    # Faster algorithm tests (based on gzip; compress everything)
    ${PYTHON} main.py -f $tracefilepath -c f1  -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f2  -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f3  -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f4  -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f5  -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f6  -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f7  -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f8  -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f9  -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f10 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f11 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f12 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f13 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f14 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f15 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f16 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f17 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f18 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f19 -a  -o results/trace.txt
    ${PYTHON} main.py -f $tracefilepath -c f20 -a  -o results/trace.txt

    echo
done
