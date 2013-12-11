#!/usr/bin/python2

from __future__ import division

from compressionalgorithm import *
from diskarray import DiskArray
from diskmodel import *
from processormodel import *
from selectionalgorithm import *
from simulation import Simulation
from trace import Trace

import argparse
import os
import traceback

import pdb

def main():
    '''
    Main function: parses command line arguments, generates several objects,
    and passes them all to the simulation.  Then runs the simulation and writes
    the results to an output file.
    '''


    # Set some defaults in case command line arguments are not supplied
    DEFAULT_TRACE_FILE_NAME = "./trace"
    DEFAULT_SPIN_DOWN_TIMEOUT = float("inf") # seconds
    DEFAULT_COMPRESSION_THRESHOLD = 0.3 # compression ratio
    DEFAULT_COMPRESSION_ALG = "g"
    DEFAULT_OUTPUT_FILE_NAME = "output.csv"

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
                        help="compression algorithm to use in the simulation (g = gzip, b = bzip2, 7 = 7z, l, = lzop, s = snappy, fx = gzip x times faster, gx = gzip with x times better compression)",
                        default=DEFAULT_COMPRESSION_ALG,
                        choices=["g", "b", "7", "l", "s", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20", "g1", "g2", "g3", "g4", "g5"])

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

    parser.add_argument("-o", "--output",
                        help="output file name (results will be appended to this file)",
                        default=DEFAULT_OUTPUT_FILE_NAME,
                        metavar="OUTPUT_FILE")

    # Parse the command line arguments
    args = parser.parse_args()

    trace_file_name = args.trace
    spin_down_timeout = args.timeout
    output_file_name = args.output

    if args.compression_alg == "g":
        compression_alg = gzip_alg
    elif args.compression_alg == "b":
        compression_alg = bzip2_alg
    elif args.compression_alg == "7":
        compression_alg = sevenz_alg
    elif args.compression_alg == "s":
        compression_alg = snappy_alg
    elif args.compression_alg == "f1":
        compression_alg = faster1_alg
    elif args.compression_alg == "f2":
        compression_alg = faster2_alg
    elif args.compression_alg == "f3":
        compression_alg = faster3_alg
    elif args.compression_alg == "f4":
        compression_alg = faster4_alg
    elif args.compression_alg == "f5":
        compression_alg = faster5_alg
    elif args.compression_alg == "f6":
        compression_alg = faster6_alg
    elif args.compression_alg == "f7":
        compression_alg = faster7_alg
    elif args.compression_alg == "f8":
        compression_alg = faster8_alg
    elif args.compression_alg == "f9":
        compression_alg = faster9_alg
    elif args.compression_alg == "f10":
        compression_alg = faster10_alg
    elif args.compression_alg == "f11":
        compression_alg = faster11_alg
    elif args.compression_alg == "f12":
        compression_alg = faster12_alg
    elif args.compression_alg == "f13":
        compression_alg = faster13_alg
    elif args.compression_alg == "f14":
        compression_alg = faster14_alg
    elif args.compression_alg == "f15":
        compression_alg = faster15_alg
    elif args.compression_alg == "f16":
        compression_alg = faster16_alg
    elif args.compression_alg == "f17":
        compression_alg = faster17_alg
    elif args.compression_alg == "f18":
        compression_alg = faster18_alg
    elif args.compression_alg == "f19":
        compression_alg = faster19_alg
    elif args.compression_alg == "f20":
        compression_alg = faster20_alg
    elif args.compression_alg == "g1":
        compression_alg = greater1_alg
    elif args.compression_alg == "g2":
        compression_alg = greater2_alg
    elif args.compression_alg == "g3":
        compression_alg = greater3_alg
    elif args.compression_alg == "g4":
        compression_alg = greater4_alg
    elif args.compression_alg == "g5":
        compression_alg = greater5_alg
        
    if args.none:
        selection_alg = NoCompressionSelectionAlgorithm()
        compression_threshold = 0
    elif args.all:
        selection_alg = CompressEverythingSelectionAlgorithm()
        compression_threshold = float("inf")
    else:
        compression_threshold = args.compression_ratio
        selection_alg = ThresholdCompressionAlgorithm(
            compression_threshold,
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

    results = sim.run()

    # Write the parameters and results to the output file.  The file is written
    # in CSV format, which is easy to parse and can be read by many spreadsheet
    # applications.

    # Do some calculations up front
    average_read_time = 0
    if results.read_count > 0:
        average_read_time = results.total_read_time / results.read_count

    average_write_time = 0
    if results.write_count > 0:
        average_write_time = results.total_write_time / results.write_count

    total_energy_usage = results.processor_energy_usage + \
                         results.disk_energy_usage
    
    # Open (or create) the file for appending.
    # Technically there is a bug here because the file might spontaneously
    # spring into existence between the time it is checked and the time it is
    # opened, but there's no need to worry about that for non-production code.
    file_exists = os.path.exists(output_file_name)
    output_file = open(output_file_name, 'a')

    # Write out the header, if needed
    if not file_exists:
        output_file.write("trace_file_name,compression_algorithm,"
                          "compression_threshold,spin_down_timeout,"
                          "total_read_time,read_count,avg_read_time,"
                          "total_write_time,write_count,avg_write_time,"
                          "processor_energy_used,disk_energy_used,"
                          "total_energy_used,total_capacity_used,"
                          "parse_error_occurred\n")

    # Write out the input parameters
    output_file.write(trace_file_name)
    output_file.write(",")
    output_file.write(compression_alg.name)
    output_file.write(",")
    output_file.write(str(compression_threshold))
    output_file.write(",")
    output_file.write(str(spin_down_timeout))
    output_file.write(",")

    # Write out the results
    output_file.write(str(results.total_read_time))
    output_file.write(",")
    output_file.write(str(results.read_count))
    output_file.write(",")
    output_file.write(str(average_read_time))
    output_file.write(",")
    output_file.write(str(results.total_write_time))
    output_file.write(",")
    output_file.write(str(results.write_count))
    output_file.write(",")
    output_file.write(str(average_write_time))
    output_file.write(",")
    output_file.write(str(results.processor_energy_usage))
    output_file.write(",")
    output_file.write(str(results.disk_energy_usage))
    output_file.write(",")
    output_file.write(str(total_energy_usage))
    output_file.write(",")
    output_file.write(str(results.total_capacity_usage))
    output_file.write(",")
    output_file.write(str(results.parse_error_occurred))
    output_file.write("\n")

    # TODO: it might be nice to provide finer grained metrics: for example,
    # energy used by reads vs write vs idle and separate out procesor time
    # from disk time for reads and writes.

    # Clean up
    output_file.close()


try:
    main()
except SystemExit:
    pass
except:
    traceback.print_exc()
    
