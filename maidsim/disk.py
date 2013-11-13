class State:
    '''
    Enum defining the state of a disk
    '''
    OFF = 0
    ON = 1


class Disk:
    '''
    Implements a disk (hard disk or solid state).  This handles reads and writes
    of files, calculates time required, and keeps track of energy used.
    '''


    model = None
    spin_down_timeout = None    # Seconds
    energy_used = None    # Joules
    state = None
    current_time = None    # Seconds

    # Dictionary to allow looking up compressed file sizes based on file names
    file_sizes = None


    def __init__(self, disk_model, timeout):
        self.model = disk_model
        self.spin_down_timeout = timeout
        self.energy_used = 0
        self.current_time = 0
        self.file_sizes = dict()

        # For now, assume all the disks are on at the start.  This setting
        # really doesn't matter as long as we are consistent across all tests.
        self.state = State.ON


    def power_on(self):
        # Turns on the drive if it is off and returns the amount of time it
        # takes to complete this operation.
        elapsed_time = 0
        if self.state == State.OFF:
            self.state = State.ON
            self.energy_used += self.model.spin_up_energy
            elapsed_time = self.model.spin_up_time
        return elapsed_time


    def power_off(self):
        # Turns off the drive if it is on.  We are neglecting the time cost
        # of powering down because it would be unnecessarily complicated to
        # consider cases where a request comes in at the exact time a drive
        # is spinning down.
        if self.state == State.ON:
            self.state = State.OFF
            self.energy_used += self.model.spin_down_energy
        

    def update_time(self, time):

        # TODO: should maybe check if time is going backwards

        # Update the time
        elapsed_time = time - self.current_time
        self.current_time = time

        # Figure out how long the drive was active and spin down if necessary
        active_time = 0
        if self.state == State.ON:

            # Check to see if we spun down since the last update
            if elapsed_time >= self.spin_down_timeout:
                
                # Note that we're ignoring cases were a request comes in while
                # the drive is spinning down.
                active_time = self.spin_down_timeout
                self.power_off()

            else:

                active_time = elapsed_time

        # Update the energy used
        self.energy_used += active_time * self.model.idle_power


    def get_file_name(self, file_info):
        # TODO: maybe should have some file path checking to detect different
        # character strings that are the same path.
        return file_info.path + file_info.name
        

    def read(self, file_info):
        total_time = 0;
    
        # Turn on the drive if necessary
        total_time += self.power_on()

        # Find the compressed size of the file
        file_name = self.get_file_name(file_info);
        compressed_size = self.file_sizes[file_name]

        # Calculate the time to read the file from disk
        read_time = self.model.seek_time + \
                    (compressed_size / self.model.speed);
        total_time += read_time

        # Calculate the energy used to read the file from disk
        self.energy_used += read_time * self.model.read_power

        # Return the read time to the caller so that performance metrics can
        # be tracked
        return total_time


    def write(self, file_info, compressed_size):
        total_time = 0;

        # Turn on the drive if necessary
        total_time += self.power_on()

        # Store the size of the file
        file_name = self.get_file_name(file_info);
        self.file_sizes[file_name] = compressed_size

        # Calculate the time to write the file to disk
        write_time = self.model.seek_time + \
                     (compressed_size / self.model.speed)
        total_time += write_time

        # Calculate the energy used to write the file to disk
        self.energy_used += write_time * self.model.write_power

        # Return the write time to the caller so that performance metrics can
        # be tracked
        return total_time


    def get_energy_usage(self):
        return self.energy_used
