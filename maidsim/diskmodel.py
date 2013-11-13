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


    def __init__(self, spin_up_time, spin_up_energy, spin_down_energy,
                 idle_power, read_power, write_power, speed, seek_time):
        self.spin_up_time = spin_up_time
        self.spin_up_energy = spin_up_energy
        self.spin_down_energy = spin_down_energy
        self.idle_power = idle_power
        self.read_power = read_power
        self.write_power = write_power
        self.speed = speed
        self.seek_time = seek_time


fake_disk = DiskModel(1.2, 5, 2, 0.1, 3, 5, 6, 0.0001)

