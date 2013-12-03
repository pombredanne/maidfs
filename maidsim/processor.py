

from compressionalgorithm import CompressionAlgorithm
from processormodel import ProcessorModel


class CompressionResult:
    '''
    Holds the results of a compression operation.  Only used as a return type.
    '''

    execution_time = 0
    compressed_size = 0


class Processor:
    '''
    Simulates a processor and calculates the energy usage of that processor
    during idle mode and for compression and decompression operations.
    '''


    model = None
    energy_used = None
    current_time = None


    def __init__(self, processor_model):
        self.model = processor_model
        self.energy_used = 0
        self.current_time = 0


    def update_time(self, time):
        # Updates the current time for the processor and calculates idle
        # energy usage since the last event
        time_since_last_update = time - self.current_time
        self.current_time = time
        self.energy_used += time_since_last_update * self.model.idle_power


    def compress(self, file_info, compression_alg):
        # Calculate time and energy required to compress the file.  Also
        # calculate the size of the compressed file.
        # Note that we're currently ignoring processor speed and assuming that
        # the processor runs at the same speed as the processor that was used
        # when testing compression speed.
        results = CompressionResult()
        results.execution_time = file_info.size / \
                                 compression_alg.compression_speed
        results.compressed_size = file_info.size * \
                                  compression_alg.compression_ratio[
                                      file_info.file_type]
        self.energy_used += results.execution_time * self.model.active_power
        return results


    def decompress(self, file_info, compression_alg):
        # Calculate time and energy required to decompress the file.
        # Note that we're currently ignoring processor speed and assuming that
        # the processor runs at the same speed as the processor that was used
        # when testing compression speed.
        execution_time = file_info.size / compression_alg.decompression_speed
        self.energy_used += execution_time * self.model.active_power
        return execution_time


    def get_energy_usage(self):
        return self.energy_used
