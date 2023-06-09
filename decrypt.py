import getopt
import sys
import os
from colorama import Fore
from constants import HEX_DIGS, KEY_BASE, DECRYPT_LONG_OPTIONS, DECRYPT_SHORT_OPTIONS, POSSIBLE_CHAR_SIZE
from functions import DECRYPT_FUNCS, arr_split, bits_to_str, random_char_reference, form_base

def decrypt():

    # clears screen
    os.system(['clear', 'cls'][os.name == 'nt'])

    # get settings
    settings = get_args()
    key = settings['key']
    infile = settings['infile']

    # performs encryption operations
    key = arr_split(list(key), HEX_DIGS)
    
    # splits into the function mods and the random states
    func_nums = key[0:len(key) // 2:]
    state_nums = key[len(key) // 2::]
    
    # gets functions and states 
    funcs = [DECRYPT_FUNCS[int("".join(num), KEY_BASE) % len(DECRYPT_FUNCS)] for num in func_nums]
    states = [int("".join(num), KEY_BASE) for num in state_nums]

    # read input file
    bit_arr = read_cypher(infile, states[-1])

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
        args = getopt.getopt(arg_list, DECRYPT_SHORT_OPTIONS, DECRYPT_LONG_OPTIONS)[0]

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
def read_cypher(f_name, state):     # random state needed for conversion back to bit array
    with open(f_name) as f:
        crypt_str = list(f.read())

    # determines the index where leftover bits are
    if crypt_str[-1].isnumeric():
        split_index = len(crypt_str)
        while crypt_str[split_index - 1].isnumeric():
            split_index -= 1
        
        # splits into chars and leftovers
        chars = crypt_str[:split_index:]
        leftover_bits = crypt_str[split_index::]
    else:
        chars = crypt_str[::]
        leftover_bits = []

    # determines the refernece
    char_reference = random_char_reference(state)
    
    # flip the reference and get letters pointing to numbers
    flip_reference = {}
    for num, char in enumerate(char_reference):
        flip_reference[char] = num

    # gets numbers and adds to bit list
    bit_arr = []
    for char in chars:
        bit_arr += list(form_base(char_reference.index(char), 2, POSSIBLE_CHAR_SIZE))
    
    # add leftovers
    bit_arr += leftover_bits

    return bit_arr
    
# writes the decrypted result to a text file
def write_output(f_name, bit_arr):
    with open(f_name, "w") as f:
        f.write(bits_to_str(bit_arr))

if __name__ == "__main__":
    decrypt()