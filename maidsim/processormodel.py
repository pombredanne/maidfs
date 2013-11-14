import units

class ProcessorModel:
    '''
    Describes the attributes of a processor.  This class should only have public
    data members.
    '''


    idle_power = None
    active_power = None
    speed = None

    def __init__(self, idle_power, active_power, speed):
        self.idle_power = idle_power
        self.active_power = active_power
        self.speed = speed


xeonE52658v2 = ProcessorModel(14.4, 66.1, 2.4*units.GHz)
