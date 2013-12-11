from __future__ import division

import units


class DiskModel:
    '''
    Describes a disk (hard disk or SSD).  This class should only contain public
    data members.
    '''

    spin_up_time = None      # Seconds
    spin_up_energy = None    # Joules
    spin_down_energy = None  # Joules
    idle_power = None        # Watts
    read_power = None        # Watts
    write_power = None       # Watts
    speed = None             # bytes/sec
    seek_time = None         # Seconds
    capacity = None          # bytes

    def __init__(self, spin_up_time, spin_up_energy, spin_down_energy,
                 idle_power, read_power, write_power, speed, seek_time,
                 capacity):
        self.spin_up_time = spin_up_time
        self.spin_up_energy = spin_up_energy
        self.spin_down_energy = spin_down_energy
        self.idle_power = idle_power
        self.read_power = read_power
        self.write_power = write_power
        self.speed = speed
        self.seek_time = seek_time
        self.capacity = capacity


# Western Digital Savvio 10k.6 (hard drive)
# see http://www.seagate.com/files/www-content/product-content/savvio-fam/savvio-10k/savvio-10k-6/en-us/docs/savvio-10k-6-data-sheet-ds1768-1-1210us.pdf
savvio10k6hd = DiskModel(
    5,  # spin up time -  just a guess - couldn't find any hard data
    5 * 3.4,    # spin up energy - assuming this is negligible
    1 * 3.4,    # spin down energy - assuming this is negligible
    3.4,    # idle power - from spec sheet
    7.33 - 3.4,   # read power - from spec sheet (idle power is already accounted for)
    7.33 - 3.4,   # write power - from spec sheet (idle power is already accounted for)
    40 * units.MiB,    # speed - based on test results
    0.0,     # seek time (ignored because it's the same with and without compression)
    600 * units.GB)     # capacity


# Western Digital SiliconDrive A100 (solid state drive)
# see http://www.wdc.com/wdproducts/library/SpecSheet/ENG/2879-771419.pdf
siliconDriveA100ssd = DiskModel(
    0.1,    # spin up time - just a guess - couldn't find any hard data
    0.1 * 0.5,  # spin up energy - assuming this is negligible
    0,      # spin down energy - assuming this is negligible
    0.5,    # idle power - from spec sheet
    0.9 - 0.5,    # read power - from spec sheet (idle power is already accounted for)
    0.9 - 0.5,    # write power - from spec sheet (idle power is already accounted for)
    200 * units.MiB,    # speed - from spec sheet
    0,      # seek time - from spec sheet
    128 * units.GB)     # capacity
