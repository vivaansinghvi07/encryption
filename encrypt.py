import random
import time
import sys
import getopt
import os
from colorama import Fore   
from constants import HEX_DIGS, FUNC_COUNT_BOUNDS, KEY_BASE, ENCRYPT_LONG_OPTIONS, ENCRYPT_SHORT_OPTIONS, POSSIBLE_CHAR_SIZE
from functions import ENCRYPT_FUNCS, str_to_bits, arr_split, form_base, random_char_reference

# almost true randomness
random.seed(time.time_ns())

def encrypt():

    # gets settings
    settings = get_args()  

    # obtains file for reading (optional) and writing (required)
    infile = settings["infile"]

    # gets the message
    if infile:
        bit_arr = str_to_bits(read_input(infile))
    else:
        bit_arr = str_to_bits(settings["message"])

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
    key = arr_split(list(key), HEX_DIGS)
    
    # splits into the function mods and the random states
    func_nums = key[0:len(key) // 2:]
    state_nums = key[len(key) // 2::]
    
    # gets functions and states 
    funcs = [ENCRYPT_FUNCS[int("".join(num), KEY_BASE) % len(ENCRYPT_FUNCS)] for num in func_nums]
    states = [int("".join(num), KEY_BASE) for num in state_nums]

    # runs everything
    for func, state in zip(funcs, states):
        bit_arr = func(bit_arr, state)

    # writes to output
    outfile = settings["outfile"]
    write_cypher(outfile, bit_arr, states[-1])

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
        args = getopt.getopt(arg_list, ENCRYPT_SHORT_OPTIONS, ENCRYPT_LONG_OPTIONS)[0]

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

# returns the decryption and encryption key - randomly generated
def get_key():

    # blank key
    key = ""

    # function count - determines how many encryption functions are done
    func_count = random.randint(FUNC_COUNT_BOUNDS["lower"], FUNC_COUNT_BOUNDS["upper"])

    # generates function ids
    for _ in range(func_count):         
        
        # get random number in the base
        func_num = random.randint(0, KEY_BASE**HEX_DIGS-1)
        key += form_base(func_num, KEY_BASE, HEX_DIGS)   # strip off the "0x"

    # generate random states
    for _ in range(func_count):
        random_state = random.randint(0, KEY_BASE**HEX_DIGS-1)
        key += form_base(random_state, KEY_BASE, HEX_DIGS)

    return key.lower()

# read input from file, return string
def read_input(f_name):
    with open(f_name, "r") as f:
        return f.read()
    
# write the binary
def write_cypher(f_name, bit_arr, state):

    # rounds down to nearest 
    split_index = len(bit_arr) // POSSIBLE_CHAR_SIZE * POSSIBLE_CHAR_SIZE

    # splits bit array
    convertible_bits = arr_split(bit_arr[:split_index:], POSSIBLE_CHAR_SIZE)
    leftover_bits = bit_arr[split_index::]

    # converts bit array to ints
    char_nums = list(map(int, ["".join(bits) for bits in convertible_bits], [2 for _ in range(len(convertible_bits))]))

    # get int to char
    char_reference = random_char_reference(state)
    
    # finally, convert the char_nums to the chars
    output = "".join([char_reference[num] for num in char_nums]) + "".join(leftover_bits)

    with open(f_name, "w") as f:
        f.write(output)

if __name__ == "__main__":  

    # clears screen
    os.system(['clear', 'cls'][os.name == 'nt'])

    # performs encryption
    encrypt()