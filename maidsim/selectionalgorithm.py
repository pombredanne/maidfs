class SelectionAlgorithm:
    '''
    Implements a selective compression algorithm.  This algorithm determines
    whether a given file should be compressed or not.

    This class is designed as a base class; actual selection algorithms should
    be implemented as child classes.
    '''


    def should_compress(self, file_info):
        # Returns a boolean indicating if the file should be compressed or not.
        return False


class NoCompressionSelectionAlgorithm(SelectionAlgorithm):
    '''
    Most basic selection algorithm: don't compress anything.  This is actually
    the same as the base SelectionAlgorithm.
    '''

class CompressEverythingSelectionAlgorithm(SelectionAlgorithm):
    '''
    The other most basic selection algorithm: compress everything.
    '''


    def should_compress(self, file_info):
        return True


class ThresholdCompressionAlgorithm(SelectionAlgorithm):
    '''
    Makes compression decisions based on a threshold and information about the
    compression algorithm used.  If the compression ratio for a given file
    (based on the file type) is expected to be below the threshold, then the
    file is compressed.
    '''


    threshold = None
    compression_alg = None


    def __init__(self, threshold, compression_alg):
        self.threshold = threshold
        self.compression_alg = compression_alg


    def should_compress(self, file_info):
        compression_ratio = self.compression_alg.compression_ratio[ \
            file_info.file_type]
        return (compression_ratio <= self.threshold)

