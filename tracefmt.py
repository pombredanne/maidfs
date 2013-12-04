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
cache = {}
for f in open(sys.argv[1]).readlines():
    try:
        syscall, path, timestamp = f.split('\t')

        if not os.path.exists(path) or not os.access(path, os.R_OK):
            continue

        if path not in cache:
            child = subprocess.Popen(cmd_du.format(path),
                    shell=True, stdout=subprocess.PIPE)
            num_bytes = child.stdout.readline().rstrip()

            child = subprocess.Popen(cmd_file.format(path),
                    shell=True, stdout=subprocess.PIPE)
            mimetype = child.stdout.readline().rstrip()
            cache[path] = {
                'syscall': syscall,
                'path': path,
                'size_bytes': int(num_bytes),
                'mimetype': mimetype
            }

        trace = cache[path].copy()
        trace['timestamp'] = int(timestamp)
        traces.append(trace)
    except:
        pass

print(json.dumps(traces))
