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

# based on preliminary results
# NOTE: speed is in terms of bytes/sec
gzip_alg = CompressionAlgorithm(23232955.36,
        [0.377656117, 0.999549344, 0.992642428, 0.990812813, 0.977854524],
        65861489.45)

bzip2_alg = CompressionAlgorithm(7109074.375,
        [0.305588766, 1.003703696, 0.98621879, 0.99044826, 0.974886517],
        18089685.9)

_7z_alg = CompressionAlgorithm(4230593.932,
        [0.762788752, 1.95437884, 2.020264387, 3.547802383, 3.766411654],
        7181550.832)
