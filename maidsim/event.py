class EventType:
    '''
    Describes the type (read or write) of a file system event.
    '''

    READ = 0
    WRITE = 1
    


class Event:
    '''
    Represents an event in a file system trace.  This class should only contain
    public data members describing the event.
    '''

    time = None
    file_info = None
    access_type = None

