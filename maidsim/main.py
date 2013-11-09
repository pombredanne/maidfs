#!/usr/bin/python2


from trace import Trace
from simulation import Simulation


# TODO: this should be a command line arg
TRACE_FILE_NAME = "./trace"


def main():
    '''
    Main function: parses command line arguments, generates several objects,
    and passes them all to the simulation.  Then runs the simulation.

    Objects generated and passed to the simulation:
    tr - trace of disk accesses
    compression_model - description of a compression algorithm
    processor_model - description of a processor
    disk_model - description of a hard disk
    '''

    # TODO: parse command line arguments
    # TODO: create objects
    # TODO: may need multiple disk models (solid state vs hard disk)
    
    trace = Trace(TRACE_FILE_NAME)
    
    sim = Simulation(trace)
    sim.run()


main()
