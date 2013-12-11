from __future__ import division

'''
Enum containing all the file types we are considering
'''
def enum(**enums):
    return type('Enum', (), enums)

FileType = enum(TEXT=0, BINARY=1, IMAGE=2, VIDEO=3, AUDIO=4)
