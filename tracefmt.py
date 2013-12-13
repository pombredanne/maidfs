"""Take the output of trace.d and annotate disk size (in bytes)
and mimetype of each file. This program will remove files that no longer
exist from the original trace and programs which cannot be accessed
due to permissions.

The output of this program will be a valid JSON structure that
can then be piped to a pretty-printer:

    $ python tracefmt.py trace.txt | python -mjson.tool > pretty.json
"""

import json
import os
import subprocess
import sys

traces = []

with open(sys.argv[1]) as f:
    cmd_file = "/usr/bin/file -Ib '{}'"
    cache = {}

    lines = (line.rstrip() for line in f)
    lines = (line for line in lines if line)

    for line in lines:
        syscall, path, timestamp, size = line.split('\t')

        if path not in cache:
            if not os.path.exists(path) or not os.access(path, os.R_OK):
                mimetype = 'application/octet-stream; charset=binary'
            else:
                child = subprocess.Popen(cmd_file.format(path),
                        shell=True, stdout=subprocess.PIPE)
                mimetype = child.stdout.readline().rstrip()

            cache[path] = { 'path': path, 'mimetype': mimetype }

        trace = cache[path].copy()
        trace['syscall'] = syscall
        trace['size_bytes'] = int(size)
        trace['timestamp'] = int(timestamp)
        traces.append(trace)

print(json.dumps(traces))
