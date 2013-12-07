from disk import Disk


class DiskArray:
    '''
    Implements a disk array.  This class is responsible for managing an array
    of disks and dispatching file system accesses to specific disks.  This
    class will also manage cache disks if they are used.
    '''


    cache_disks = None
    passive_disks = None
    next_disk = None    # The passive disk to which the next new file will be
                        # written.  Files are currently written to disks in a
                        # round-robin fashion.
    file_locations = None    # A mapping of file names to the passive disks
                             # they are stored on.


    def __init__(self, num_cache_disks, cache_disk_model,
                 num_passive_disks, passive_disk_model, spin_down_timeout):

        # Create lists to hold the cache disks and passive disks
        if num_cache_disks > 0:
            # Cache disks are not implemented for now
            raise NotImplementedError(
                "Cache disks are currently not implemented.");
        self.cache_disks = []
        '''
        self.cache_disks = \
            [Disk(cache_disk_model, float("inf")) \
            for _ in range(num_cache_disks)]
        '''
        self.passive_disks = \
            [Disk(passive_disk_model, spin_down_timeout) \
            for _ in range(num_passive_disks)]

        # Set up metadata
        self.file_locations = dict()
        self.next_disk = 0


    def update_time_for_disks(self, disk_list, time):
        # Update the time for the given list of disks
        for the_disk in disk_list:
            the_disk.update_time(time)


    def update_time(self, time):
        # Update time for the cache disks and passive disks
        self.update_time_for_disks(self.cache_disks, time)
        self.update_time_for_disks(self.passive_disks, time)


    def read(self, file_info):
        # Find the correct disk in the passive array
        disk_num = self.file_locations[file_info.full_name()]

        # Read the file from that disk and return the amount of time it took
        # to read the file.
        return self.passive_disks[disk_num].read(file_info)


    def write(self, file_info, size):
        # See if the file already exists
        disk_num = 0
        try:
            disk_num = self.file_locations[file_info.full_name()]
        except KeyError:
            # The file does not exist, so assign it to a disk
            disk_num = self.next_disk
            self.next_disk = (self.next_disk + 1) % len(self.passive_disks)
            self.file_locations[file_info.full_name()] = disk_num

        # Write the file to the appropriate disk and return the amount of time
        # it took to write the file.
        return self.passive_disks[disk_num].write(file_info, size)


    def get_energy_usage_for_disks(self, disk_list):
        # Sum up the energy usage for the given list of disks
        total_energy = 0
        for the_disk in disk_list:
            total_energy += the_disk.get_energy_usage()
        return total_energy


    def get_energy_usage(self):
        # Sum up the energy used by the disks in this array during the entire
        # simulation
        return self.get_energy_usage_for_disks(self.cache_disks) + \
               self.get_energy_usage_for_disks(self.passive_disks)


    def reset_energy_usage_for_disks(self, disk_list):
        # Reset the energy usage for the given list of disks
        for the_disk in disk_list:
            the_disk.reset_energy_usage()


    def reset_energy_usage(self):
        # Reset the energy usage for all the disks
        self.reset_energy_usage_for_disks(self.cache_disks)
        self.reset_energy_usage_for_disks(self.passive_disks)

