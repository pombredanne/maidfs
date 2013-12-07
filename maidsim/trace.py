from event import Event
from event import EventType
from fileinfo import FileInfo
from filetype import FileType

import units

import json

class Trace:
    '''
    Represents a file system trace containing read and write events to a large
    file system.  The trace file should be in json format.  Each entry
    contains the following:

    Time
    File name
    File path
    File type
    File size
    Access type (read or write)
    '''


    event_list = None
    current_event = 0
    first_event_timestamp = 0
    types = None


    def __init__(self, file_name):
        # Open the file
        trace_file = open(file_name)

        # Extract the json data
        self.event_list = json.load(trace_file)

        # Close the trace file
        trace_file.close()

        # Set the index to the first event
        self.current_event = 0

        # Remember the timestamp for the first event.  This will be used as
        # time zero, and all other timestamps will be adjusted to this time.
        self.first_event_timestamp = self.event_list[0]["timestamp"]

        # Set up a correspondence between mimetypes and file types
        self.types = dict()
        self.types["image/png"] = FileType.IMAGE


    def next_event(self):
        # Note that this function will throw an exception if there are no more
        # events to process.

        event = self.event_list[self.current_event]
        self.current_event += 1

        # Extract the data about the event
        time = event["timestamp"]

        # Update the timestamp so that the first event happens at time zero
        time -= self.first_event_timestamp
        time /= units.ns

        access_type_string = event["syscall"]
        if access_type_string == "read":
            access_type = EventType.READ
        else:
            access_type = EventType.WRITE

        # The entire path is used as the file name and the path is set to an
        # empty string
        file_name = event["path"]
        file_path = ""
        file_size = event["size_bytes"]

        # Convert mimetype to file type
	mimetype = event["mimetype"]

        # If a mimetype hasn't been assigned to a file type yet, print out
        # a message instead of throwing an exception.  This allows us to
        # discover more than one missing type in a single run.
        try:
            file_type = self.types[mimetype]
        except KeyError:
            print "Unknown mimetype: " + mimetype
            file_type = FileType.BINARY

        file_info = FileInfo(file_name, file_path, file_type, file_size)

        return Event(time, file_info, access_type)


    def more_events(self):
        return len(self.event_list) > self.current_event


    def reset(self):
        # Start the trace again at the beginning
        self.current_event = 0
