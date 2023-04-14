import random
import time
import sys
import getopt
import os
from colorama import Fore

# determines random seed to make things consistent
FUNC_COUNT_BOUNDS = {"lower": 8, "upper": 16}
DUPL_COUNT_BOUNDS = {"lower": 1, "upper": 4}
FUNC_MODS = {}
CHAR_SIZE = 7
HEX_DIGS = 3
ENCODING = 'ascii'

# stores options
SHORT_OPTIONS = 'i:o:k:m:'
LONG_OPTIONS = ['infile=', 'outfile=', 'key=', 'message=']

# almost true randomness
random.seed(time.time_ns())

def encrypt():

    # clears screen
    os.system(['clear', 'cls'][os.name == 'nt'])

    # gets settings
    settings = get_args()  

    # obtains file for reading (optional) and writing (required)
    infile = settings["infile"]

    # gets the message
    if infile:
        bit_arr = get_bits(read_input(infile))
    else:
        bit_arr = get_bits(settings["message"])

    if len(bit_arr) == 0:
        print(f"{Fore.RED}Argument Error \n\n{Fore.RESET}Please do not enter empty messages or files.\n")
        sys.exit()

    # gets key
    if not settings["key"]:
        key = get_key()
        print(f"Your key is: {Fore.BLUE}{key}")
    else:
        key = settings["key"]
    
    # performs encryption operations
    key = arr_split(list(key), HEX_DIGS)[1::]
    
    # splits into the function mods and the random states
    func_nums = key[0:len(key) // 2:]
    state_nums = key[len(key) // 2::]
    
    # gets functions and states 
    funcs = [FUNC_MODS[int("0x" + "".join(num), 16) % len(FUNC_MODS)] for num in func_nums]
    states = [int("0x" + "".join(num), 16) for num in state_nums]

    # runs everything
    for func, state in zip(funcs, states):
        bit_arr = func(bit_arr, state)

    # writes to output
    outfile = settings["outfile"]
    write_output(outfile, bit_arr)

# gets arguments
def get_args():

    # stores arguments
    output = {
        "infile": None,
        "outfile": None,
        "key": None,
        "message": None
    }

    # remove the file name
    arg_list = sys.argv[1::]

    try:
        args = getopt.getopt(arg_list, SHORT_OPTIONS, LONG_OPTIONS)[0]

        # filters arguments
        for arg, val in args:
            if arg in ['-i', '--infile']:
                output["infile"] = val
            elif arg in ['-o', '--outfile']:
                output["outfile"] = val
            elif arg in ['-k', '--key']:
                output["key"] = val
            elif arg in ['-m', '--message']:
                output["message"] = val

        # checks if no message given or no output given
        if (not output['infile'] and not output['message']) or (output['infile'] and output['message']):
            sys.exit()

        if not output['outfile']:
            sys.exit()

        # returns dict with the options
        return output

    except: 
        print(f"{Fore.RED}Argument Error \n\n{Fore.RESET}Correct usage is: \n\n{Fore.BLUE}$ python3 encrypt.py -i INFILENAME -o OUTFILENAME -k KEY -m MESSAGE \n\n{Fore.RESET}You must either have a infile or a message, not both or neither. You also must include an outfile where the encrypted message is written. The rest of the arguments are optional, and the program will adapt depending on their presence.\n")
        sys.exit()

# adds to the dictionary of function mappers
def register(func, counter=[0]):        # default counter value of 0 so the variable stays
    FUNC_MODS[counter[0]] = func
    counter[0] += 1
    return func

# returns the decryption and encryption key - randomly generated
def get_key():

    # blank key
    key = ""

    # function count - determines how many encryption functions are done
    func_count = random.randint(FUNC_COUNT_BOUNDS["lower"], FUNC_COUNT_BOUNDS["upper"])

    key += form_hex(func_count, HEX_DIGS)

    # generates function ids
    for _ in range(func_count):         
        
        # get random hex number
        func_num = random.randint(0, 255)
        key += form_hex(func_num, HEX_DIGS)   # strip off the "0x"

    # generate random states
    for _ in range(func_count):
        random_state = random.randint(0, 4095)
        key += form_hex(random_state, HEX_DIGS)

    return key

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

# gets the user input in bit form
def get_bits(str):

    # convert string to byte array
    byte_array = str.encode(ENCODING)

    # get binary values 
    bin_str = ""
    for byte in byte_array:
        bin_str += form_bin(byte, CHAR_SIZE)       # [2::] slice removes the '0b' in front of the number

    return list(bin_str)

# shuffles a bit array: [1, 1, 1, 1, 0, 0, 0, 0] => [0, 1, 1, 0, 0, 1, 0, 1, 1]
@register
def shuf_bits(bit_arr, state):

    random.seed(state)

    # shuffle bits and return new string
    random.shuffle(bit_arr)
    return bit_arr

# translates a bit array: [1, 0, 1, 1, 1, 1, 0] => [1, 1, 1, 1, 0, 1, 0]
@register
def shift_bits(bit_arr, state):

    random.seed(state)
    
    # determines random index to shift to
    shift_index = random.randint(0, len(bit_arr) - 1)

    # shifts the list
    new_arr = bit_arr[shift_index::] + bit_arr[0:shift_index]

    return new_arr

# duplicate bit array: [1, 0, 1] * n => [1, 0, 1, 1, 0, 1, ..., 1, 0, 1]
@register
def dupl_bits(bit_arr, state):
    
    random.seed(state)

    # determines how many duplications to do
    dupl = random.randint(DUPL_COUNT_BOUNDS["lower"], DUPL_COUNT_BOUNDS["upper"])

    # performs duplication
    new_arr = bit_arr * dupl

    return new_arr

# adds to the hex values of each byte in the bit array: [00000000, ...] + n => [00000101, ...] when n = 5
@register
def add_hex(bit_arr, state):

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

def get_num(byte, adder):
    num = int("0b" + "".join(byte), 2)
    return (num + adder) % 2**CHAR_SIZE

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

def read_input(f_name):
    with open(f_name, "r") as f:
        return f.read()
    
def write_output(f_name, bit_arr):

    # converts to string and writes
    with open(f_name, "w") as f:
        f.write(bits_to_str(bit_arr))

def bits_to_str(bit_arr):

    # converts to binary char 
    bin_char_arr = arr_split(bit_arr, CHAR_SIZE)

    # converts to byte array
    byte_array = bytes([int("0b" + "".join(bin_num), 2) for bin_num in bin_char_arr])

    # converts back to string
    return byte_array.decode(ENCODING) 


if __name__ == "__main__":  
    encrypt()