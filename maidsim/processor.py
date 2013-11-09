

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


    def __init__(self, processor_model):
        self.model = processor_model


    def update_time(self, new_time):
        # Updates the current time for the processor
        # TODO: calculate idle energy usage since last event
        pass


    def compress(self, file_info, compression_alg):
        # TODO: calculate time and energy usage to compress the file
        # TODO: calculate the new size of the file
        # TODO: return a CompressonResult with the new size if the file and the
        # time required for compression
        return None


    def decompress(self, file_info, compression_alg):
        # TODO: calculate time and energy usage to decompress the file
        pass


    def get_energy_usage(self):
        # TODO: return the energy usage by the processor since it was created
        return None    
