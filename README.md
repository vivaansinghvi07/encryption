# Encryption
Uses various techniques to encrypt a string of text.

## Usage

Download all the python files of the repository to a folder. See [here](https://www.gitkraken.com/learn/git/github-download#how-to-downlaod-a-file-from-github) on how to download files from GitHub. Then, follow the instructions below to encrypt and decrypt files.

- First, you will need to install the necessary libaries. Do this by running the following onto your terminal:

    ```
    $ pip3 install colorama
    $ pip3 install numpy
    ```
- ### `encrypt.py`
    - To use, run the following command:

        ```
        $ python3 encrypt.py -o OUTFILE -i INFILE -m MESSAGE -k KEY
        ```
    - You must include an out-file where output will be written.
    - For input, you must have <u>either</u> an in-file <u>or</u> a message. However, it seems to work more consistently with a file.
    - Additionally, you can include a predetermined key to encrypt messages using that key.
    
- ### `decrypt.py`
    - To use, run the following command:

        ```
        $ python3 decrypt.py -i INFILE -o OUTFILE -k KEY
        ```

    - You must include an in-file; it is the only way for a cypher to be read.
    - You must also include a key, as it is necessary for decryption. The key is given to you by the encryption algorithm.


## Methods

Input is read and converted to a list of bits to maximize randomization. There are several functions defined which add some element of randomization to the function. Each function is given a specific random state, which is stored in the key for decryption. Here is a list of them:
- **Shuffle**: Simply shuffles the list of bits.
- **Shift**: Shifts the bits left by a random amount.
- **Add to Char**: Given the char size, this function adds a random number to each char saved in the bit array. To be able to do this, the bit array is first converted into a 2d array of chars.
- **Duplicate**: Simply duplicates the list of bits present by a random amount.

All decryption methods essentially perform these operations but in reverse. Additionally, after all operations are done, there is another form of randomization in which each set of 6 bits is converted to a character. The conversion from bit-set to character and back is randomly generated for more security.