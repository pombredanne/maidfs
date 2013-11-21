import os, sys
import time
import psutil
import subprocess
import logging

COMP_FILE_NAME = '/tmp/compressed'
DECOMP_FILE_NAME = '/tmp/decompressed'

COMPRESSION_TYPES = (
    # command, suffix
    ('gzip', 'gz'),
    ('7z', '7z'),
)

# FIXME: This is for testing purposes only. Will replace with an environment
# value or something configurable.
FILES = (
    '/Users/sumin/Downloads/dump.sql',
    '/Users/sumin/Downloads/rfc4269.txt',
)

NULL_FILE = open(os.devnull, 'w')

logger = logging.getLogger('compression_exp')
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
logger.addHandler(handler) 
logger.setLevel(logging.INFO)


class Profiler:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.secs = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        self.secs = self.end - self.start


def get_file_size(file_name):
    stats = os.stat(file_name)
    return stats.st_size


def build_comp_cmd(comp_util, file_name, suffix):
    if comp_util == 'gzip':
        return [comp_util, '-c', file_name], \
            open('{}.{}'.format(COMP_FILE_NAME, suffix), 'w')

    elif comp_util == '7z':
        return [comp_util, 'a', '{}.{}'.format(COMP_FILE_NAME, suffix),
            file_name], NULL_FILE

    else:
        raise Exception('Unsupported compression type: {}'.format(comp_type))


def build_decomp_cmd(comp_util, file_name, suffix):
    if comp_util == 'gzip':
        return [comp_util, '-df', '{}.{}'.format(COMP_FILE_NAME, suffix)], \
            open('{}.{}'.format(DECOMP_FILE_NAME, suffix), 'w')

    elif comp_util == '7z':
        return [comp_util, 'x', '{}.{}'.format(COMP_FILE_NAME, suffix),
            '-o/tmp/', '-aoa'], NULL_FILE

    else:
        raise Exception('Unsupported compression type: {}'.format(comp_type))


def time_cmd(cmd=[], fout=NULL_FILE):
    """Measures time time (in seconds) that a given command takes to run."""

    with Profiler() as profiler:
        subprocess.check_call(cmd, stdout=fout)

    return profiler.secs


def cleanup():
    os.unlink(COMP_FILE_NAME)
    os.unlink(DECOMP_FILE_NAME)


def measure(file_name, comp_type):
    comp_util, suffix = comp_type

    logger.info('Compressing {} with {}'.format(file_name, comp_type))

    uncomp_file_size = get_file_size(file_name)

    comp_cmd, fout = build_comp_cmd(comp_util, file_name, suffix)
    comp_time = time_cmd(comp_cmd, fout)

    comp_file_size = get_file_size('{}.{}'.format(COMP_FILE_NAME, suffix))

    logger.info(' '.join(comp_cmd))
    logger.info('Decompressing {} with {}'.format(file_name, comp_type))

    decomp_cmd, fout = build_decomp_cmd(comp_util, file_name, suffix)

    decomp_time = time_cmd(decomp_cmd, fout)

    print uncomp_file_size, comp_time, comp_file_size, decomp_time


if __name__ == '__main__':

    for file_name in FILES:
        for comp_type in COMPRESSION_TYPES:
            measure(file_name, comp_type)
