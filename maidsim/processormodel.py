from __future__ import division

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

# Intel Xeon E5-2658 v2 Processor
# see http://www.intel.com/content/www/us/en/intelligent-systems/romley/xeon-e5-2600-v2-series-appl-power-guide-addendum.html
# Active power is based on CINT400, and integer performance benchmark, with
# the expectation that compression algorithms use mostly integer operations.
xeonE52658v2 = ProcessorModel(
    14.4,   # idle power
    66.1,   # active power
    2.4*units.GHz)  # speed
