import sys

sys.path.append("..")

from disk import Disk
from diskmodel import DiskModel
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
    

def disk_test():

    timeout = 500

    # Set up a disk model, disk, and some files for testing purposes
    test_disk = DiskModel(
        2.5,    # spin up time
        30,     # spin up energy
        10,     # spin down energy
        3,      # idle power
        7,      # read power
        8,      # write power
        300*units.MiB,  # speed
        0.003)   # seek time
    disk = Disk(test_disk, timeout)

    file1 = FileInfo("file1", "/", FileType.TEXT, 1*units.GiB)
    file1_compressed_size = 300*units.MiB
    file2 = FileInfo("file2", "/", FileType.BINARY, 40*units.MiB)
    file2_compressed_size = 35*units.MiB

    # Tests
    passed = True

    # Write when the disk is on
    current_time = timeout / 2
    disk.update_time(current_time)
    time = disk.write(file1, file1_compressed_size)
    energy = disk.get_energy_usage()

    expected_time = test_disk.seek_time + (file1_compressed_size /
                                           test_disk.speed)
    expected_energy = (timeout / 2) * test_disk.idle_power + \
                      expected_time * test_disk.write_power;
    if not floateq(time, expected_time):
        passed = False
        print "Failed write test 1 for time"
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed write test 1 for energy"

    # Write when the disk is off
    current_time += timeout * 2
    disk.update_time(current_time)
    time = disk.write(file2, file2_compressed_size)
    energy = disk.get_energy_usage()

    expected_time = test_disk.spin_up_time + \
                    test_disk.seek_time + \
                    (file2_compressed_size / test_disk.speed)
    expected_energy += timeout * test_disk.idle_power + \
                       test_disk.spin_down_energy + \
                       test_disk.spin_up_energy + \
                       (expected_time - test_disk.spin_up_time) * \
                       test_disk.write_power;
    if not floateq(time, expected_time):
        passed = False
        print "Failed write test 2 for time"
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed write test 2 for energy"

    # Read when the disk is on
    current_time += timeout / 2
    disk.update_time(current_time)
    time = disk.read(file1)
    energy = disk.get_energy_usage()

    expected_time = test_disk.seek_time + (file1_compressed_size /
                                           test_disk.speed)
    expected_energy += (timeout / 2) * test_disk.idle_power + \
                       expected_time * test_disk.read_power;
    if not floateq(time, expected_time):
        passed = False
        print "Failed read test 1 for time"
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed read test 1 for energy"
        

    # Read when the disk is off
    current_time += timeout * 5
    disk.update_time(current_time)
    time = disk.read(file2)
    energy = disk.get_energy_usage()

    expected_time = test_disk.spin_up_time + \
                    test_disk.seek_time + \
                    (file2_compressed_size / test_disk.speed)
    expected_energy += timeout * test_disk.idle_power + \
                       test_disk.spin_down_energy + \
                       test_disk.spin_up_energy + \
                       (expected_time - test_disk.spin_up_time) * \
                       test_disk.read_power;
    if not floateq(time, expected_time):
        passed = False
        print "Failed read test 2 for time"
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed read test 2 for energy"


    # Try to read something that doesn't exist
    file3 = FileInfo("file1", "/newpath/", FileType.TEXT, 1*units.GiB)
    exception_occurred = False
    try:
        disk.read(file3)
    except:
        exception_occurred = True
    if not exception_occurred:
        passed = False
        print "Failed read test for non-existant file"

    if passed:
        print "All disk tests passed"
    else:
        print "Disk tests FAILED"


try:
    disk_test()
except:
    traceback.print_exc()
