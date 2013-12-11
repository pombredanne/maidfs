from __future__ import division


class FileInfo:
    '''
    Describes the basic attributes of a file.
    '''

    name = None
    path = None
    file_type = None
    size = None

    def __init__(self, name, path, file_type, size):
        self.name = name
        self.path = path
        self.file_type = file_type
        self.size = size

    def full_name(self):
        return self.path + self.name
