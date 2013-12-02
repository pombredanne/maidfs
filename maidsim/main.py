#!/usr/bin/python2


from compressionalgorithm import *
from diskarray import DiskArray
from diskmodel import *
from processormodel import *
from selectionalgorithm import *
from simulation import Simulation
from trace import Trace

import argparse
import traceback

import pdb

def main():
    '''
    Main function: parses command line arguments, generates several objects,
    and passes them all to the simulation.  Then runs the simulation.
    '''


    # Set some defaults in case command line arguments are not supplied
    DEFAULT_TRACE_FILE_NAME = "./trace"
    DEFAULT_SPIN_DOWN_TIMEOUT = 512 # seconds
    DEFAULT_COMPRESSION_THRESHOLD = 0.3 # compression ratio
    DEFAULT_COMPRESSION_ALG = "g"

    # Generate a parser for the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--trace",
                        help="file name of trace file to execute",
                        default=DEFAULT_TRACE_FILE_NAME,
                        metavar="TRACE_FILE")
    parser.add_argument("-t", "--timeout",
                        help="spin down timeout for disks",
                        default=DEFAULT_SPIN_DOWN_TIMEOUT,
                        metavar="SPIN_DOWN_TIMEOUT")
    parser.add_argument("-c", "--compression_alg",
                        help="compression algorithm to use in the simulation (g = gzip, b = bzip2, 7 = 7z)",
                        default=DEFAULT_COMPRESSION_ALG,
                        choices=["g", "b", "7"])

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--none",
                       action="store_true",
                       help="do not compress any files")
    group.add_argument("-a", "--all",
                       action="store_true",
                       help="compress all files")
    group.add_argument("-r", "--compression_ratio",
                       help="compression ratio below which files will be compressed",
                       default=DEFAULT_COMPRESSION_THRESHOLD,
                       type=float,
                       metavar="COMPRESSION_RATIO")

    # Parse the command line arguments
    args = parser.parse_args()

    trace_file_name = args.trace
    spin_down_timeout = args.timeout

    if args.compression_alg == "g":
        compression_alg = gzip_alg
    elif algs.compression_alg == "b":
        compression_alg = bzip_alg
    else:
        compression_alg = _7z_alg
        
    if args.none:
        selection_alg = NoCompressionSelectionAlgorithm()
    elif args.all:
        selection_alg = CompressEverythingSelectionAlgorithm()
    else:
        selection_alg = ThresholdCompressionAlgorithm(
            args.compression_ratio,
            compression_alg)

    # The following parameters are hard coded
    processor_model = xeonE52658v2
    num_cache_disks = 0
    cache_disk_model = siliconDriveA100ssd
    num_passive_disks = 100
    passive_disk_model = savvio10k6hd

    trace = Trace(trace_file_name)
    disk_array = DiskArray(num_cache_disks, cache_disk_model,
                           num_passive_disks, passive_disk_model,
                           spin_down_timeout)
    sim = Simulation(trace,
                     compression_alg,
                     selection_alg,
                     processor_model,
                     disk_array)

    sim.run()


try:
    main()
except SystemExit:
    pass
except:
    traceback.print_exc()
    
