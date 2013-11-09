

from disk import Disk


class DiskArray:
    '''
    Implements a MAID array.  This class is responsible for managing an array
    of disks and dispatching file system accesses to specific disks.  This
    class will also manage cache disks if they are used.
    '''


    def __init__(self):
        # TODO: fill this in
        pass


    def update_time(self, time):
        # TODO: update the current time for all disks in the array
        # TODO: perform any other time related calculations (may be nothing
        # at this level).
        pass


    def read(self, file_info):
        # TODO: read the given file from the correct disk
        # TODO: need to update this to handle the fact that the compressed size
        # is different from the file size
        # TODO: return the total amount of time it took to do the read
        return None


    def write(self, file_info):
        # TODO: write the given file to the correct disk
        # TODO: need to update this to handle the fact that the compressed size
        # is different from the file size
        # TODO: return the total amount of time it took to do the write
        return None


    def get_energy_usage(self):
        # TODO: sum up the energy used by the disks in this array during the
        # entire simulation
        return None

