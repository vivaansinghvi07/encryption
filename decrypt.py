import getopt
import sys
import os
from colorama import Fore
from constants import HEX_DIGS, KEY_BASE
from functions import DECRYPT_FUNCS, arr_split, bits_to_str

SHORT_OPTIONS = "i:k:o:"
LONG_OPTIONS = ['infile=', 'key=', 'outfile=']

def decrypt():

    # clears screen
    os.system(['clear', 'cls'][os.name == 'nt'])

    # get settings
    settings = get_args()
    key = settings['key']
    infile = settings['infile']

    # read input file
    bit_arr = read_binary(infile)

    # performs encryption operations
    key = arr_split(list(key), HEX_DIGS)
    
    # splits into the function mods and the random states
    func_nums = key[0:len(key) // 2:]
    state_nums = key[len(key) // 2::]
    
    # gets functions and states 
    funcs = [DECRYPT_FUNCS[int("".join(num), KEY_BASE) % len(DECRYPT_FUNCS)] for num in func_nums]
    states = [int("".join(num), KEY_BASE) for num in state_nums]

    # execute all the reserve functions in reverse order
    funcs = funcs[::-1]
    states = states[::-1]

    # reverse the functions and states
    for func, state in zip(funcs, states):
        bit_arr = func(bit_arr, state)

    # writes the bits to output
    if not settings["outfile"]:
        print(f"Your decrypted message is:\n\n{bits_to_str(bit_arr)}\n")
    else:
        write_output(settings["outfile"], bit_arr)

def get_args():

    # stores arguments
    output = {
        "infile": None,
        "outfile": None,
        "key": None
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

        # checks if no message given or no output given
        if not output["infile"] or not output["key"]:
            sys.exit()

        # returns dict with the options
        return output

    except: 
        print(f"{Fore.RED}Argument Error \n\n{Fore.RESET}Correct usage is: \n\n{Fore.BLUE}$ python3 decrypt.py -i INFILENAME -o OUTFILENAME -k KEY \n\n{Fore.RESET}You must have an infile and a key. You may include an outfile to which your output will be written.\n")
        sys.exit()

# reads bits from the text file and returns an array of characters
def read_binary(f_name):
    with open(f_name) as f:
        return list(f.read())

# writes the decrypted result to a text file
def write_output(f_name, bit_arr):
    with open(f_name, "w") as f:
        f.write(bits_to_str(bit_arr))

if __name__ == "__main__":
    decrypt()