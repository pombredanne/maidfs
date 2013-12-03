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

cmd_du = "/usr/bin/du '{}' | awk '{{print $1}}'"
cmd_file = "/usr/bin/file -Ib '{}'"

traces = []
for f in open(sys.argv[1]).readlines():
    syscall, path, count = f.split('\t')

    if not os.path.exists(path) or not os.access(path, os.R_OK):
        continue

    child = subprocess.Popen(cmd_du.format(path),
            shell=True, stdout=subprocess.PIPE)
    num_bytes = child.stdout.readline().rstrip()

    child = subprocess.Popen(cmd_file.format(path),
            shell=True, stdout=subprocess.PIPE)
    mimetype = child.stdout.readline().rstrip()

    trace = {
        'syscall': syscall,
        'path': path,
        'access_count': int(count),
        'size_bytes': int(num_bytes),
        'mimetype': mimetype
    }
    traces.append(trace)

print(json.dumps(traces))
