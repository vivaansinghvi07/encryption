import random
import time
import sys
import getopt
import os
from colorama import Fore   
from constants import HEX_DIGS, FUNC_COUNT_BOUNDS
from functions import str_to_bits, ENCRYPT_FUNCS, read_input, write_output, arr_split, form_hex

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
    funcs = [ENCRYPT_FUNCS[int("0x" + "".join(num), 16) % len(ENCRYPT_FUNCS)] for num in func_nums]
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

# returns the decryption and encryption key - randomly generated
def get_key():

    # blank key
    key = ""

    # function count - determines how many encryption functions are done
    func_count = random.randint(FUNC_COUNT_BOUNDS["lower"], FUNC_COUNT_BOUNDS["upper"])

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

if __name__ == "__main__":  
    encrypt()