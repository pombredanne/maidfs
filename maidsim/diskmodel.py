class DiskModel:
    '''
    Describes a hard disk.  This class should only contain public data members.
    '''


    # TODO: this parameter list is not final
    spin_up_time = None
    spin_up_energy = None
    spin_down_time = None
    spin_down_energy = None
    idle_power = None
    read_power = None
    write_power = None
    speek = None


    def __init__(self, spin_up_time, spin_up_energy, spin_down_time,
                 spin_down_energy, idle_power, read_power, write_power, speed):
        self.spin_up_time = spin_up_time
        self.spin_up_energy = spin_up_energy
        self.spin_down_time = spin_down_time
        self.spin_down_energy = spin_down_energy
        self.idle_power = idle_power
        self.read_power = read_power
        self.write_power = write_power
        self.speed = speed


fake_disk = DiskModel(1.2, 5, 0.5, 2, 0.1, 3, 5, 6)

