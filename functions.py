"""
This file stores the funcitons which are used to encrypt and decrypt 
data (so that they can be right next to each other), as well as functions
that are used within both encryption and decryption
"""

import random
import numpy
from constants import *

# will be filled later; stores what mods lead to what functions
ENCRYPT_FUNCS = {}
DECRYPT_FUNCS = {}

# adds to the dictionary of function mappers
def register_encryption(func, counter=[0]):        # default counter value of 0 so the variable stays
    ENCRYPT_FUNCS[counter[0]] = func
    counter[0] += 1
    return func

def register_decryption(func, counter=[0]):
    DECRYPT_FUNCS[counter[0]] = func
    counter [0] += 1
    return func

# shuffles a bit array: [1, 1, 1, 1, 0, 0, 0, 0] => [0, 1, 1, 0, 0, 1, 0, 1, 1]
@register_encryption
def shuf_bits(bit_arr, state):

    random.seed(state)

    # copies array as to not override arg
    new_arr = [bit for bit in bit_arr]

    # shuffle bits and return new
    random.shuffle(new_arr)
    return new_arr

# unshuffles a bit array by simulating what happened and reversing it
@register_decryption
def undo_shuf_bits(bit_arr, state):

    random.seed(state)

    # stores the shuffled indeces
    comparison_arr = [i for i in range(len(bit_arr))]
    random.shuffle(comparison_arr)

    # blank new array
    new_arr = [None for _ in range(len(bit_arr))]

    # maps values
    for old_index, shuffled_index in enumerate(comparison_arr):
        new_arr[shuffled_index] = bit_arr[old_index]

    # return unshuffled array
    return new_arr

# translates a bit array: [1, 0, 1, 1, 1, 1, 0] => [1, 1, 1, 1, 0, 1, 0]
@register_encryption
def shift_bits(bit_arr, state):

    random.seed(state)
    
    # determines random index to shift to
    shift_index = random.randint(0, len(bit_arr) - 1)

    # shifts the list
    new_arr = bit_arr[shift_index::] + bit_arr[0:shift_index]
    return new_arr

# translates a bit array in the opposite direction
@register_decryption
def undo_shift_bits(bit_arr, state):
    
    random.seed(state)

    # determines what the random index was
    shift_index = random.randint(0, len(bit_arr) - 1)

    # shifts the list in the opposite direction
    new_arr = bit_arr[-shift_index::] + bit_arr[0:-shift_index:]
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

# divides the array by the duplicated amount
@register_decryption
def undo_dupl_bits(bit_arr, state):

    random.seed(state)

    # determines how many duplications were done
    dupl = random.randint(DUPL_COUNT_BOUNDS["lower"], DUPL_COUNT_BOUNDS["upper"])

    # undos the duplication
    new_arr = bit_arr[:len(bit_arr) // dupl:]
    return new_arr

# for number formattings
def get_num(byte, adder):
    num = int("0b" + "".join(byte), 2)
    return (num + adder) % 2**CHAR_SIZE

# converts a byte_array of numbers to binary
def num_arr_to_bin(num_arr):
    # convert back to binary and return
    new_bit_str = ""
    for num in num_arr:
       new_bit_str += form_base(num, 2, CHAR_SIZE)

    return list(new_bit_str)

# adds to the hex values of each byte in the bit array: [00000000, ...] + n => [00000101, ...] when n = 5
@register_encryption
def add_hex(bit_arr, state):

    random.seed(state)

    # splits bit arr into groups of ___
    byte_arr = arr_split(bit_arr, CHAR_SIZE)

    # shifts by the random added amount
    num_arr = map(get_num, byte_arr, [random.randint(0, 2**CHAR_SIZE - 1) for _ in range(len(byte_arr))])

    # convert back to binary and return
    return num_arr_to_bin(num_arr)

@register_decryption
def undo_add_hex(bit_arr, state):

    random.seed(state)

    # splits into groups of ___
    byte_arr = arr_split(bit_arr, CHAR_SIZE)

    # shifts the opposite direction by the amount
    num_arr = map(get_num, byte_arr, [- random.randint(0, 2**CHAR_SIZE - 1) for _ in range(len(byte_arr))])

    return num_arr_to_bin(num_arr)

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

# formats a number to a base and to have a certain digit count
def form_base(num, base, digits):

    # converts number 
    converted_num = numpy.base_repr(num, base=base)

    # makes a series of zeroes in front of the base to meet the digit count
    out_str = "0" * digits
    return out_str[0:-len(converted_num)] + converted_num

# converts a string to bits
def str_to_bits(str):

    # convert string to byte array
    byte_array = str.encode(ENCODING)

    # get binary values 
    bin_str = ""
    for byte in byte_array:
        bin_str += form_base(byte, 2, CHAR_SIZE)       # [2::] slice removes the '0b' in front of the number

    return list(bin_str)

# converts a bit to strings
def bits_to_str(bit_arr):

    # converts to binary char 
    bin_char_arr = arr_split(bit_arr, CHAR_SIZE)

    # converts to byte array
    byte_array = bytes([int("0b" + "".join(bin_num), 2) for bin_num in bin_char_arr])

    # converts back to string
    return byte_array.decode(ENCODING) 