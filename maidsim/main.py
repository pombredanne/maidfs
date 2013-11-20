#!/usr/bin/python2


from compressionalgorithm import *
from diskarray import DiskArray
from diskmodel import *
from processormodel import *
from selectionalgorithm import *
from simulation import Simulation
from trace import Trace

import traceback

def main():
    '''
    Main function: parses command line arguments, generates several objects,
    and passes them all to the simulation.  Then runs the simulation.
    '''

    # TODO: parse command line arguments
    
    # TODO: these should be determined by command line arguments
    trace_file_name = "./trace"
    trace = Trace(trace_file_name)

    compression_alg = fake_alg
    selection_alg = NoCompressionSelectionAlgorithm()
    processor_model = xeonE52658v2

    num_cache_disks = 0
    cache_disk_model = siliconDriveA100ssd
    num_passive_disks = 100
    passive_disk_model = savvio10k6hd
    spin_down_timeout = 512    # seconds
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
except:
    traceback.print_exc()
    
