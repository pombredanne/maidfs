from __future__ import division


class CompressionAlgorithm:
    '''
    Describes a compression algorithm.  This file should only have public data
    members.
    '''

    name = None

    # These should be lists with entries for each file type
    compression_speed = None
    compression_ratio = None
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
    [12130414.17, 27038267.75, 26383798.41, 25033441.33, 24634783.92],
    [0.377656117, 0.999549344, 0.992642428, 0.990812813, 0.977854524],
    [106132060.9, 122839000.8, 125659929.4, 110592131.9, 108761161.7])

bzip2_alg = CompressionAlgorithm("bzip2",
    [9714152.69, 4761512.52, 4950135.672, 4752811.735, 4857091.939],
    [0.305588766, 1.003703696, 0.98621879, 0.99044826, 0.974886517],
    [13031893.78, 7964833.25, 14454.02827, 8457050.508, 8960229.348])

sevenz_alg = CompressionAlgorithm("7z",
    [804498.3094, 4427047.236, 3824895.503, 3819300.174, 3864384.773],
    [0.302648571, 1.009040826, 0.99245957, 0.990712745, 0.975147138],
    [39099319.53, 13809872.84, 13291898.01, 13718395.73, 13826212.51])

lzop_alg = CompressionAlgorithm("lzop",
    [133622036.1, 259502891.8, 217623789.8, 229771829, 233795128.9],
    [0.613333536, 1.000015532, 0.99447258, 0.99498836, 0.988155026],
    [268974410.2, 1089490417, 848173708.1, 791794805.8, 832463808.8])

snappy_alg = CompressionAlgorithm("snappy",
    [191299557.2, 608377338.1, 570671029, 592835681.5, 520625377.6],
    [0.684816788, 1.000110463, 0.995022754, 0.99184873, 0.993852803],
    [442635713.1, 966817800.6, 1096636902, 1011958109, 1016081001])

# Some hypothetical algorithms
faster1_alg = CompressionAlgorithm("faster1",
    map(lambda x: x*1.5, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*1.5, gzip_alg.decompression_speed))

faster2_alg = CompressionAlgorithm("faster2",
    map(lambda x: x*2, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*2, gzip_alg.decompression_speed))

faster3_alg = CompressionAlgorithm("faster3",
    map(lambda x: x*3, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*3, gzip_alg.decompression_speed))

faster4_alg = CompressionAlgorithm("faster4",
    map(lambda x: x*4, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*4, gzip_alg.decompression_speed))

faster5_alg = CompressionAlgorithm("faster5",
    map(lambda x: x*5, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*5, gzip_alg.decompression_speed))

faster6_alg = CompressionAlgorithm("faster6",
    map(lambda x: x*6, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*6, gzip_alg.decompression_speed))

faster7_alg = CompressionAlgorithm("faster7",
    map(lambda x: x*7, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*7, gzip_alg.decompression_speed))

faster8_alg = CompressionAlgorithm("faster8",
    map(lambda x: x*8, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*8, gzip_alg.decompression_speed))

faster9_alg = CompressionAlgorithm("faster9",
    map(lambda x: x*9, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*9, gzip_alg.decompression_speed))

faster10_alg = CompressionAlgorithm("faster10",
    map(lambda x: x*10, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*10, gzip_alg.decompression_speed))

faster11_alg = CompressionAlgorithm("faster11",
    map(lambda x: x*11, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*11, gzip_alg.decompression_speed))

faster12_alg = CompressionAlgorithm("faster12",
    map(lambda x: x*12, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*12, gzip_alg.decompression_speed))

faster13_alg = CompressionAlgorithm("faster13",
    map(lambda x: x*13, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*13, gzip_alg.decompression_speed))

faster14_alg = CompressionAlgorithm("faster14",
    map(lambda x: x*14, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*14, gzip_alg.decompression_speed))

faster15_alg = CompressionAlgorithm("faster15",
    map(lambda x: x*15, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*15, gzip_alg.decompression_speed))

faster16_alg = CompressionAlgorithm("faster16",
    map(lambda x: x*16, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*16, gzip_alg.decompression_speed))

faster17_alg = CompressionAlgorithm("faster17",
    map(lambda x: x*17, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*17, gzip_alg.decompression_speed))

faster18_alg = CompressionAlgorithm("faster18",
    map(lambda x: x*18, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*18, gzip_alg.decompression_speed))

faster19_alg = CompressionAlgorithm("faster19",
    map(lambda x: x*19, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*19, gzip_alg.decompression_speed))

faster20_alg = CompressionAlgorithm("faster20",
    map(lambda x: x*20, gzip_alg.compression_speed),
    gzip_alg.compression_ratio,
    map(lambda x: x*20, gzip_alg.decompression_speed))

greater1_alg = CompressionAlgorithm("greater1",
    gzip_alg.compression_speed,
    map(lambda x: x/1.5, gzip_alg.compression_ratio),
    gzip_alg.decompression_speed)

greater2_alg = CompressionAlgorithm("greater2",
    gzip_alg.compression_speed,
    map(lambda x: x/2, gzip_alg.compression_ratio),
    gzip_alg.decompression_speed)

greater3_alg = CompressionAlgorithm("greater3",
    gzip_alg.compression_speed,
    map(lambda x: x/3, gzip_alg.compression_ratio),
    gzip_alg.decompression_speed)

greater4_alg = CompressionAlgorithm("greater4",
    gzip_alg.compression_speed,
    map(lambda x: x/4, gzip_alg.compression_ratio),
    gzip_alg.decompression_speed)

greater5_alg = CompressionAlgorithm("greater5",
    gzip_alg.compression_speed,
    map(lambda x: x/5, gzip_alg.compression_ratio),
    gzip_alg.decompression_speed)
