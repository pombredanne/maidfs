

from diskmodel import DiskModel


class Disk:
    '''
    Implements a disk (hard disk or solid state).  This handles reads and writes
    of files, calculates time required, and keeps track of energy used.
    '''


    model = None
    spin_down_timeout = None


    def __init__(self, disk_model, timeout):
        self.model = disk_model
        self.spin_down_timeout = timeout


    def update_time(self, time):
        # TODO: update the disk to the current time.  This includes determining
        # if the disk spun down and the amount of energy used since the last
        # operation.
        pass


    def read(self, file_info):
        # TODO: reads a file from the disk.  Calculates time and energy usage.
        # TODO: the size of the file needs to be included in metadata somehow
        # since the compressed file size may be different from the nominal file
        # size
        # TODO: return the total amount of time required to do the read
        return None


    def write(self, file_info, compressed_size):
        # TODO: writes a file to the disk.  Calculates time and energy usage.
        # TODO: the compressed file size needs to be written to metadata
        # somehow so that the read knows how big the file is.
        # TODO: return the total amount of time required to do the write
        return None


    def get_energy_usage(self):
        # TODO: return the energy used by this disk during the entire simulation
        return None
