class CompressionAlgorithm:
    '''
    Describes a compression algorithm.  This file should only have public data
    members.
    '''

    name = None
    compression_speed = None
    compression_ratio = None    # This should be a list with compression
                                # ratios for each file type.
    decompression_speed = None


    def __init__(self, name, compression_speed, compression_ratio,
                 decompression_speed):
        self.name = name
        self.compression_speed = compression_speed
        self.compression_ratio = compression_ratio
        self.decompression_speed = decompression_speed


# based on preliminary results
# NOTE: speed is in terms of bytes/sec
gzip_alg = CompressionAlgorithm("gzip",
        [10423524.87, 30876888.42, 23397576.69, 24574384.64, 26892402.2],
        [0.377656117, 0.999549344, 0.992642428, 0.990812813, 0.977854524],
        [53887065.59, 95981239.82, 36033727.06, 92784830.08, 50620584.68])

bzip2_alg = CompressionAlgorithm("bzip2",
        [11583800.63, 5699762.777, 6041600.459, 6046515.213, 6173692.79],
        [0.305588766, 1.003703696, 0.98621879, 0.99044826, 0.974886517],
        [26032296.68, 16504040.73, 16088366.28, 15812971.74, 16010754.06])

sevenz_alg = CompressionAlgorithm("7z",
        [1327382.121, 7756920.55, 7593345.778, 7532636.129, 7539192.727],
        [0.302648571, 1.009040826, 0.99245957, 0.990712745, 0.975147138],
        [51361797.37, 16019330.43, 16425116.54, 16635157.38, 16863513.64])
