import sys

sys.path.append("..")

from diskarray import DiskArray
from diskmodel import DiskModel
from fileinfo import FileInfo
from filetype import FileType
import units

import pdb
import traceback

def floateq(float1, float2):
    if abs(float1 - float2) < 0.1:
        return True
    else:
        return False
    

def disk_array_test():

    timeout = 500
    disks = 10

    # Set up a disk model, disk array, and some files for testing purposes
    test_disk = DiskModel(
        2.5,    # spin up time
        30,     # spin up energy
        10,     # spin down energy
        3,      # idle power
        7,      # read power
        8,      # write power
        300*units.MiB,  # speed
        0.003,   # seek time
        500*units.GiB)  # capacity
    disk_array = DiskArray(0, test_disk, disks, test_disk, timeout)

    file1 = FileInfo("file1", "/", FileType.TEXT, 1*units.GiB)
    file1_compressed_size = 300*units.MiB
    file2 = FileInfo("file2", "/", FileType.BINARY, 40*units.MiB)
    file2_compressed_size = 35*units.MiB

    # Tests
    passed = True

    # Write before the disks turn off
    current_time = timeout / 2
    disk_array.update_time(current_time)
    time = disk_array.write(file1, file1_compressed_size)
    energy = disk_array.get_energy_usage()

    expected_time = test_disk.seek_time + (file1_compressed_size /
                                           test_disk.speed)
    expected_energy = (timeout / 2) * test_disk.idle_power * disks + \
                      expected_time * test_disk.write_power;
    if not floateq(time, expected_time):
        passed = False
        print "Failed write test 1 for time"
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed write test 1 for energy"

    # Update the time to when most of the disks turn off
    current_time += timeout / 2
    disk_array.update_time(current_time)
    energy = disk_array.get_energy_usage()
    expected_energy += disks * (timeout / 2) * test_disk.idle_power + \
                       (disks - 1) * test_disk.spin_down_energy
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed test 2"

    # Update the time so that the last disk turns off
    current_time += timeout / 2
    disk_array.update_time(current_time)
    energy = disk_array.get_energy_usage()
    expected_energy += (timeout / 2) * test_disk.idle_power + \
                       test_disk.spin_down_energy
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed test 3"

    # Turn a disk back on to read
    current_time += timeout * 10
    disk_array.update_time(current_time)
    time = disk_array.read(file1)
    energy = disk_array.get_energy_usage()

    read_time = file1_compressed_size / test_disk.speed
    expected_time = test_disk.spin_up_time + read_time
    expected_energy += test_disk.spin_up_energy + \
                       read_time * test_disk.read_power
    if not floateq(time, expected_time):
        passed = False
        print "Failed read test 4 for time"
    if not floateq(energy, expected_energy):
        passed = False
        print "Failed read test 4 for energy"

    # Try to read a file that's not there
    exception_occurred = False
    try:
        disk_array.read(file2)
    except:
        exception_occurred = True
    if not exception_occurred:
        passed = False
        print "Failed read test for non-existant file"

    # Try to allocate some cache disks
    exception_occurred = False
    try:
        disk_array = DiskArray(1, test_disk, disks, test_disk, timeout)
    except:
        exception_occurred = True
    if not exception_occurred:
        passed = False
        print "Failed read test for non-existant file"

    # TODO: add a test where multiple disks are involved (one disk is still on
    # from a previous operation while others are turned on for new operations)

    if passed:
        print "All disk array tests passed"
    else:
        print "Disk array tests FAILED"


try:
    disk_array_test()
except:
    traceback.print_exc()
