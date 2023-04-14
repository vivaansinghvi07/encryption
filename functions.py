"""
This file stores the funcitons which are used to encrypt and decrypt 
data (so that they can be right next to each other), as well as functions
that are used within both encryption and decryption
"""

import random
from constants import *

# will be filled later; stores what mods lead to what functions
ENCRYPT_FUNCS = {}
DECRYPT_FUNCS = {}

# adds to the dictionary of function mappers
def register_encryption(func, counter=[0]):        # default counter value of 0 so the variable stays
    ENCRYPT_FUNCS[counter[0]] = func
    counter[0] += 1

def register_decryption(func, counter=[0]):
    DECRYPT_FUNCS[counter[0]] = func
    counter [0] += 1

# shuffles a bit array: [1, 1, 1, 1, 0, 0, 0, 0] => [0, 1, 1, 0, 0, 1, 0, 1, 1]
@register_encryption
def shuf_bits(bit_arr, state):

    random.seed(state)

    # shuffle bits and return new string
    random.shuffle(bit_arr)
    return bit_arr

# translates a bit array: [1, 0, 1, 1, 1, 1, 0] => [1, 1, 1, 1, 0, 1, 0]
@register_encryption
def shift_bits(bit_arr, state):

    random.seed(state)
    
    # determines random index to shift to
    shift_index = random.randint(0, len(bit_arr) - 1)

    # shifts the list
    new_arr = bit_arr[shift_index::] + bit_arr[0:shift_index]

    return new_arr

# duplicate bit array: [1, 0, 1] * n => [1, 0, 1, 1, 0, 1, ..., 1, 0, 1]
@register_encryption
def dupl_bits(bit_arr, state):
    
    random.seed(state)

    # determines how many duplications to do
    dupl = random.randint(DUPL_COUNT_BOUNDS["lower"], DUPL_COUNT_BOUNDS["upper"])

    # performs duplication
    new_arr = bit_arr * dupl

    return new_arr

# adds to the hex values of each byte in the bit array: [00000000, ...] + n => [00000101, ...] when n = 5
@register_encryption
def add_hex(bit_arr, state):

    # for number formattings
    def get_num(byte, adder):
        num = int("0b" + "".join(byte), 2)
        return (num + adder) % 2**CHAR_SIZE

    random.seed(state)

    # splits bit arr into groups of ___
    byte_arr = arr_split(bit_arr, CHAR_SIZE)

    # shifts by the random added amount
    num_arr = map(get_num, byte_arr, [random.randint(0, 2**CHAR_SIZE - 1) for _ in range(len(byte_arr))])

    # convert back to binary and return
    new_bit_arr = ""
    for num in num_arr:
       new_bit_arr += form_bin(num, CHAR_SIZE)

    return list(new_bit_arr)

# splits an array into chunks of size <size>
def arr_split(arr, size):

    arr_length = len(arr)

    # assures the split can happens
    assert(arr_length % size == 0)

    # create new array
    new_arr = [[] for _ in range(arr_length // size)]

    # fill the new arrays with each value in order
    for i in range(arr_length):
        new_arr[i // size].append(arr[i])
    return new_arr

# formats a hex to have a certain digit count
def form_hex(num, digits):

    # converts number to hex
    hex_num = hex(num)[2::]

    # series of zeros
    out_str = "0" * digits

    # puts the hex onto the output
    out_str = out_str[0:-len(hex_num)] + hex_num

    return out_str

# formats a binary in teh same way
def form_bin(num, digits):
    
    # converts to binary\
    bin_num = bin(num)[2::]

    # series of zeroes
    out_str = "0" * digits

    return out_str[0:-len(bin_num)] + bin_num

# read input from file, return string
def read_input(f_name):
    with open(f_name, "r") as f:
        return f.read()
    
# write bit-array input to file
def write_output(f_name, bit_arr):
    # converts to string and writes
    with open(f_name, "w") as f:
        f.write(bits_to_str(bit_arr))

# converts a string to bits
def str_to_bits(str):

    # convert string to byte array
    byte_array = str.encode(ENCODING)

    # get binary values 
    bin_str = ""
    for byte in byte_array:
        bin_str += form_bin(byte, CHAR_SIZE)       # [2::] slice removes the '0b' in front of the number

    return list(bin_str)

# converts a bit to strings
def bits_to_str(bit_arr):

    # converts to binary char 
    bin_char_arr = arr_split(bit_arr, CHAR_SIZE)

    # converts to byte array
    byte_array = bytes([int("0b" + "".join(bin_num), 2) for bin_num in bin_char_arr])

    # converts back to string
    return byte_array.decode(ENCODING) 