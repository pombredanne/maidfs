class CompressionAlgorithm:
    '''
    Describes a compression algorithm.  This file should only have public data
    members.
    '''

# TODO: figure out units for speed (MB/sec?) and decide what speed means 
# exactly.  The compression speed and the processor speed will both need to be
# taken into account when determining compression/decompression time.

    compression_speed = None
    compression_ratio = None    # This should be a list with compression
                                # ratios for each file type.
    decompression_speed = None


    def __init__(self, compression_speed, compression_ratio,
                 decompression_speed):
        self.compression_speed = compression_speed
        self.compression_ratio = compression_ratio
        self.decompression_speed = decompression_speed


fake_alg = CompressionAlgorithm(1000, [0.2, 1.1, 1.0, 1.2, 1.2], 2000)
