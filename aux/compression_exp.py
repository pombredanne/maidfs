import os, sys
import time
import psutil
import subprocess
import logging

COMP_FILE_NAME = '/tmp/compressed'
DECOMP_FILE_NAME = '/tmp/decompressed/'

COMPRESSION_TYPES = (
    # command, suffix
    #('tar', 'tar.gz'),
    #('tar', 'tar.bz2'),
    ('7z', '7z'),
)

# FIXME: This is for testing purposes only. Will replace with an environment
# value or something configurable.
FILES = (
    '/Users/sumin/Documents/compression-test/text',
    '/Users/sumin/Documents/compression-test/binary',
    '/Users/sumin/Documents/compression-test/image',
    '/Users/sumin/Documents/compression-test/video',
    '/Users/sumin/Documents/compression-test/audio',
)

NULL_FILE = open(os.devnull, 'w')

logger = logging.getLogger('compression_exp')
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
logger.addHandler(handler) 
logger.setLevel(logging.DEBUG)


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
    if os.path.isfile(file_name):
        stats = os.stat(file_name)
        return stats.st_size

    elif os.path.isdir(file_name):
        logger.debug(file_name)
        # http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
        return sum([os.path.getsize(os.path.join(file_name, f))
            for f in os.listdir(file_name)
            if os.path.isfile(os.path.join(file_name, f))])

    else:
        raise Exception('Unsupported file type')


def build_comp_cmd(comp_util, file_name, suffix):
    if suffix == 'tar.gz':
        return [comp_util, '-zcf', '{}.{}'.format(COMP_FILE_NAME, suffix),
            file_name], NULL_FILE

    elif suffix == 'tar.bz2':
        return [comp_util, '-jcf', '{}.{}'.format(COMP_FILE_NAME, suffix),
            file_name], NULL_FILE

    elif suffix == '7z':
        return [comp_util, 'a', '{}.{}'.format(COMP_FILE_NAME, suffix),
            file_name], NULL_FILE

    else:
        raise Exception('Unsupported compression type: {}'.format(suffix))


def build_decomp_cmd(comp_util, file_name, suffix):
    if suffix == 'tar.gz':
        return [comp_util, '-zxf', '{}.{}'.format(COMP_FILE_NAME, suffix),
            '-C', DECOMP_FILE_NAME], NULL_FILE

    elif suffix == 'tar.bz2':
        return [comp_util, '-jxf', '{}.{}'.format(COMP_FILE_NAME, suffix),
            '-C', DECOMP_FILE_NAME], NULL_FILE

    elif suffix == '7z':
        return [comp_util, 'x', '{}.{}'.format(COMP_FILE_NAME, suffix),
            '-o/tmp/', '-aoa'], NULL_FILE

    else:
        raise Exception('Unsupported compression type: {}'.format(suffix))


def time_cmd(cmd=[], fout=NULL_FILE):
    """Measures time time (in seconds) that a given command takes to run."""

    with Profiler() as profiler:
        subprocess.check_call(cmd, stdout=fout)

    return profiler.secs


def cleanup(sffix):
    os.unlink('{}.{}'.format(COMP_FILE_NAME, suffix))
    os.unlink('{}.{}'.format(DECOMP_FILE_NAME, suffix))


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

    logger.info(', '.join(map(str, [uncomp_file_size, comp_time, comp_file_size, decomp_time])))

    cleanup(suffix)

    return uncomp_file_size, comp_time, comp_file_size, decomp_time


def print_as_csv(*args):
    uncomp_file_size, comp_time, comp_file_size, decomp_time = args

    print ','.join(map(str, [
        uncomp_file_size / comp_time, # compression speed
        comp_file_size / float(uncomp_file_size), # compression ratio
        uncomp_file_size / decomp_time, # decompression speed
    ]))


if __name__ == '__main__':

    for file_name in FILES:
        for comp_type in COMPRESSION_TYPES:
                print_as_csv(*measure(file_name, comp_type))
