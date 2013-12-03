import sys

sys.path.append("..")

from compressionalgorithm import CompressionAlgorithm
from processor import Processor
from processormodel import ProcessorModel
from fileinfo import FileInfo
from filetype import FileType
import units

import pdb
import traceback

def floateq(float1, float2):
    if abs(float1 - float2) < 0.000001:
        return True
    else:
        return False


def processor_test():

    # Set up some objects for testing
    model = ProcessorModel(
        13,     # idle power
        27.1,   # active power
        3.0*units.GHz)  # speed
    processor = Processor(model)
    compression_alg = CompressionAlgorithm(
        11*units.MiB,   # compression speed
        [0.1,   # text compression ratio
         1.2,   # binary compression ratio
         0.9,   # image compression ratio
         1.0,   # video compression ratio
         0.8],  # audio compression ratio
        17*units.MiB)   # decompression speed
    file1 = FileInfo("file1", "/", FileType.TEXT, 1*units.GiB)
    file2 = FileInfo("file2", "/", FileType.BINARY, 40*units.MiB)

    # Tests
    passed = True

    # Run the processor idle
    current_time = 1000
    processor.update_time(current_time)
    energy = processor.get_energy_usage()

    expected_energy = current_time * model.idle_power
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed idle power test"

    # Compress a file
    results = processor.compress(file1, compression_alg)
    energy = processor.get_energy_usage()

    expected_size = file1.size * compression_alg.compression_ratio[file1.file_type]
    expected_time = file1.size / compression_alg.compression_speed
    expected_energy += expected_time * model.active_power

    if not floateq(results.compressed_size, expected_size):
        passed = False
        print "Failed compression test for size"
    if not floateq(results.execution_time, expected_time):
        passed = False
        print "Failed compression test for time"
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed compression test for energy"
    
    # Decompress a file
    time = processor.decompress(file2, compression_alg)
    energy = processor.get_energy_usage()

    expected_time = file2.size / compression_alg.decompression_speed
    expected_energy += expected_time * model.active_power

    if not floateq(time, expected_time):
        passed = False
        print "Failed decompression test for time"
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed decompression test for energy"

    if passed:
        print "All processor tests passed"
    else:
        print "Processor tests FAILED"

try:
    processor_test()
except:
    traceback.print_exc()
