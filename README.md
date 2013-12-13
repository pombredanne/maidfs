maidfs
======

```maidfs``` is a software simulation of processor and hard disk to gauge energy
use when various compression algorithms and compression ratios are used on workloads.

The software simulation supports GZip, BZip, LZO and [Snappy](https://code.google.com/p/snappy/) out of the box.

To run, first generate a trace file. This requires that the host system have a working
installation of DTrace (Mac OS X, FreeBSD, Solaris-derivatives, Linux via [dtrace4linux](https://github.com/dtrace4linux/linux).)
Next, convert the trace file to JSON format with the provided ```tracefmt.py``` tool.

```
# ./trace.d > trace.txt
$ python tracefmt.py trace.txt > trace.json
```

Optionally, JSON trace files can be formatted for easier reading:

```
$ python tracefmt.py trace.txt | python -mjson.tool > trace.json
```

Finally, the simulator can re-play the trace file with various command line arguments.
Run ```python main.py --help``` to see a full list of arguments.

We provide a batch run script that runs the simulator against all supported compression
algorithms and various compression ratios. This script can be run via:

```
$ ./tracer.bash
```

Results will appear in ```results/trace.txt``` as a CSV file.
