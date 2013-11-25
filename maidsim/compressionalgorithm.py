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
gzip_alg = CompressionAlgorithm(19850796.84,
        [0.343789349, 0.895010754, 0.948683215, 0.99946001, 0.977854164],
        127529527.2)

bzip2_alg = CompressionAlgorithm(5471412.616,
        [0.305588766, 66.46213967, 0.950647907, 0.99044826, 0.974886277], # 66.46 seems wrong...
        15488093.15)

_7z_alg = CompressionAlgorithm(3909888.524,
        [0.302648571, 100.8312446, 2.094601952, 3.641893277, 3.840438132], # 100.83 also seems wrong
        13380703.55)
