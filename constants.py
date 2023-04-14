# constants to keep things consistent
FUNC_COUNT_BOUNDS = {"lower": 8, "upper": 16}   # number of functions to be exectued in encryption
DUPL_COUNT_BOUNDS = {"lower": 1, "upper": 4}    # bounds for duplication count
CHAR_SIZE = 7                                   # the size of a character in bits
HEX_DIGS = 3                                    # the number of hex digits for each function in the key
ENCODING = 'ascii'                              # type of text encoding used
KEY_BASE = 29                                   # base in which the key is defined

# stores options for getting args
ENCRYPT_SHORT_OPTIONS = 'i:o:k:m:'
ENCRYPT_LONG_OPTIONS = ['infile=', 'outfile=', 'key=', 'message=']
DECRYPT_SHORT_OPTIONS = "i:k:o:"
DECRYPT_LONG_OPTIONS = ['infile=', 'key=', 'outfile=']