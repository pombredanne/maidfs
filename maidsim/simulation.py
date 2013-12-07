from event import EventType
from processor import CompressionResult
from processor import Processor


class SimulationResults:
    '''
    Utility class to hold the results from a run of the simulation
    '''

    # Performance metrics
    total_read_time = None
    read_count = None
    total_write_time = None
    write_count = None

    # Energy metrics
    processor_energy_usage = None
    disk_energy_usage = None


class Simulation:
    '''
    Master file that runs through a file system trace and simulates executing
    the trace on a MAID array while selectively applying compression according
    to a provided algorithm.
    '''


    trace = None
    compression_alg = None
    selection_alg = None
    processor = None
    disk_array = None
    previous_time = None
    total_read_time = None
    read_count = None
    total_write_time = None
    write_count = None


    def __init__(self, trace, compression_alg, selection_alg, 
                 processor_model, disk_array):
        self.trace = trace
        self.compression_alg = compression_alg
        self.selection_alg = selection_alg
        self.processor = Processor(processor_model)
        self.disk_array = disk_array
        self.previous_time = 0
        self.total_read_time = 0
        self.read_count = 0
        self.total_write_time = 0
        self.write_count = 0


    def read(self, do_compress, file_info):
        # Read a file from the disk array
        read_time = self.disk_array.read(file_info)
        if do_compress:
            read_time += \
                self.processor.decompress(file_info,
                                          self.compression_alg)
        return read_time


    def write(self, do_compress, file_info):
        # Write a file to the disk array
        compression_result = CompressionResult()
        if do_compress:
            compression_result = self.processor.compress(
                file_info, compression_alg)
        write_time = compression_result.execution_time
        write_time += self.disk_array.write(
            file_info, compression_result.compressed_size)
        return write_time


    def prepare_array(self):
        # This procedure ensures that any file that will be read during the
        # simulation already exists in the array
        while self.trace.more_events():

            # Get the next event
            event = self.trace.next_event()

            # If this file will be read during the simulation, write it to
            # the array
            if event.access_type is EventType.READ:
                do_compress = self.selection_alg.should_compress(event.file_info)
                self.write(do_compress, event.file_info)
            

    def execute_trace(self):

        while self.trace.more_events():

            # Get the next event
            event = self.trace.next_event()

            # Make sure time is not going backwards
            if event.time < self.previous_time:
                raise ValueError("Time is going backwards: current time = " +
                                 str(event.time) +
                                 ", previous time = " +
                                 str(self.previous_time))
            event.previous_time = event.time

            # Update the time in the rest of the simulation
            self.processor.update_time(event.time)
            self.disk_array.update_time(event.time)

            # Determine if this file should be compressed
            do_compress = self.selection_alg.should_compress(event.file_info)

            # Compress and write or read and decompress the file
            if event.access_type is EventType.READ:
                read_time = self.read(do_compress, event.file_info)
                self.total_read_time += read_time
                self.read_count += 1
            else:
                write_time = self.write(do_compress, event.file_info)
                self.total_write_time += write_time
                self.write_count += 1


    def run(self):
        # Prepare the disk array
        self.prepare_array()

        # Reset the trace and the energy usage for the array and processor
        self.trace.reset()
        self.processor.reset_energy_usage()
        self.disk_array.reset_energy_usage()

        # Simulate the provided trace
        print "Starting trace execution"
        self.execute_trace()
        print "Trace execution complete"

        # Gather and report results
        results = SimulationResults()
        results.total_read_time = self.total_read_time
        results.read_count = self.read_count
        results.total_write_time = self.total_write_time
        results.write_count = self.write_count
        results.processor_energy_usage = self.processor.get_energy_usage()
        results.disk_energy_usage = self.disk_array.get_energy_usage()
        return results        
