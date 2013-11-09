class SelectionAlgorithm:
    '''
    Implements a selective compression algorithm.  This algorithm determines
    whether a given file should be compressed or not.

    This class is designed as a base class; actual selection algorithms should
    be implemented as child classes.
    '''


    def should_compress(self, file_info):
        # Returns a boolean indicating if the file should be compressed or not.
        return false


# TODO: implement the real selective compression algorithm (and any others we
# want to use.  It probably needs to implement a threshold that determines
# whether we want to compress a file based on compression ratio.
