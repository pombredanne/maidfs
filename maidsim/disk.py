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

    # The starting state for all the disks.  Not really relevant as long as
    # it's consistent across runs.
    DEFAULT_STATE = State.ON


    model = None
    spin_down_timeout = None    # Seconds
    energy_used = None    # Joules
    state = None
    current_time = None    # Seconds
    last_activity_time = None    # The last time the disk was accessed

    # Dictionary to allow looking up compressed file sizes based on file names
    file_sizes = None


    def __init__(self, disk_model, timeout):
        self.model = disk_model
        self.spin_down_timeout = timeout
        self.energy_used = 0
        self.current_time = 0
        self.last_activity_time = 0
        self.file_sizes = dict()
        self.state = self.DEFAULT_STATE


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
        # Update the time
        time_since_activity = time - self.last_activity_time
        time_since_last_update = time - self.current_time
        self.current_time = time

        # Figure out how long the drive was active and spin down if necessary
        active_time = 0
        if self.state == State.ON:

            # Check to see if we spun down since the last update
            if time_since_activity >= self.spin_down_timeout:
                
                # We've already accounted for the energy used before the last
                # update.  We just need to consider the energy used between
                # the last update and the timeout.
                already_recorded = \
                    time_since_activity - time_since_last_update
                active_time = self.spin_down_timeout - already_recorded
                self.power_off()

            else:

                active_time = time_since_last_update

        # Update the energy used
        self.energy_used += active_time * self.model.idle_power


    def read(self, file_info):
        total_time = 0;

        # update_time must be called before any reads or writes to set the
        # current time    
        self.last_activity_time = self.current_time

        # Turn on the drive if necessary
        total_time += self.power_on()

        # Find the compressed size of the file
        compressed_size = self.file_sizes[file_info.full_name()]

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

        # update_time must be called before any reads or writes to set the
        # current time    
        self.last_activity_time = self.current_time

        # Turn on the drive if necessary
        total_time += self.power_on()

        # Store the size of the file
        self.file_sizes[file_info.full_name()] = compressed_size

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


    def reset_energy_usage(self):
        # Reset the energy usage, stored times, and disk state
        self.energy_used = 0
        self.current_time = 0
        self.last_activity_time = 0
        self.state = self.DEFAULT_STATE


    def get_capacity_usage(self):
        # Return the total amount of disk space used on this disk
        total_capacity = 0
        for size in self.file_sizes.itervalues():
            total_capacity += size
        return total_capacity
