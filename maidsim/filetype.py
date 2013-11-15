# class FileType:
#     '''
#     Enum containing all the file types we are considering.
#     '''


#     TEXT = 0
#     BINARY = 1
#     IMAGE = 2
#     VIDEO = 3

#     # TODO: add more types as necessary

#
# How about this?
#
def enum(**enums):
    return type('Enum', (), enums)

FileType = enum(TEXT=0, BINARY=1, IMAGE=2, VIDEO=3, AUDIO=4)
