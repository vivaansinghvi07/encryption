import math

# constants to keep things consistent - changeable for more security, etc
FUNC_COUNT_BOUNDS = {"lower": 8, "upper": 16}   # number of functions to be exectued in encryption
DUPL_COUNT_BOUNDS = {"lower": 1, "upper": 3}    # bounds for duplication count
HEX_DIGS = 3                                    # the number of hex digits for each function in the key
KEY_BASE = 29                                   # base in which the key is defined

# risky to change
ENCODING = 'ascii'                              # type of text encoding used
CHAR_SIZE = 7                                   # the size of a character in bits

# stores options for getting args
ENCRYPT_SHORT_OPTIONS = 'i:o:k:m:'
ENCRYPT_LONG_OPTIONS = ['infile=', 'outfile=', 'key=', 'message=']
DECRYPT_SHORT_OPTIONS = "i:k:o:"
DECRYPT_LONG_OPTIONS = ['infile=', 'key=', 'outfile=']

# characters that can be entered into the encryption
POSSIBLE_CHARS = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*?\n/ ')       # 64 TOTAL
POSSIBLE_CHAR_SIZE = round(math.log2(len(POSSIBLE_CHARS)))   # 6 for now

# assures the length of the possible chars is good (power of 2)
assert len(POSSIBLE_CHARS) == 2**POSSIBLE_CHAR_SIZE