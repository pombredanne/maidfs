

from diskarray import DiskArray
from compressionalgorithm import CompressionAlgorithm
from event import Event
from event import EventType
from processor import CompressionResult
from processor import Processor
from processormodel import ProcessorModel
from selectionalgorithm import SelectionAlgorithm
from trace import Trace


class Simulation:
    '''
    Master file that runs through a file system trace and simulates executing
    the trace on a MAID array while selectively applying compression according
    to a provided algorithm.
    '''


    trace = None

    # TODO: if someone can think of a better name than selection_alg, please use it
    selection_alg = None

    compression_alg = None
    processor = None
    disk_array = None


    def __init__(self, trace):
        self.trace = trace
        # TODO: perform other initialization


    def execute_trace(self):

        while self.trace.more_events():

            # Get the next event
            event = self.trace.next_event()

            # Update the time in the rest of the simulation
            self.processor.update_time(event.time)
            self.disk_array.update_time(event.time)

            # Determine if this file should be compressed
            do_compress = self.selection_alg.should_compress(event.file)

            # Compress and write or read and decompress the file
            # TODO: need to keep track of performance results for all reads and
            # writes
            read_time = 0
            write_time = 0
            if event.access_type is EventType.READ:
                read_time += self.disk_array.read(event.file)
                if do_compress:
                    read_time += \
                        self.processor.decompress(event.file, compression_alg)
            else:
                size = event.file.size
                compression_result = CompressionResult()
                if do_compress:
                    compression_result = self.processor.compress(
                        event.file, compression_alg)
                write_time += compression_result.execution_time
                write_time += self.disk_array.write(
                    event.file, compression_result.compressed_size)

        # Clean up
        self.trace.close()


    def run(self):
        # TODO: set up objects (if that's not already done in __init__)

        # Simulate the provided trace
        print "Starting trace execution"
        self.execute_trace()
        print "Trace execution complete"

        # TODO: gather and report results
