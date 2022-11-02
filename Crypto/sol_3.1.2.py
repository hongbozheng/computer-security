#!/usr/bin/env python3
# CMD: python3 sol_3.1.2.py 3.1.2_sub_ciphertext.txt 3.1.2_sub_key.txt sol_3.1.2.txt

import sys

DEBUG=0

def main():
    if len(sys.argv) != 4:
        print('[USAGE]: python3 <your_script.py> <ciphertext_file> <key_file> <output_file>')
        exit(1)

    with open(sys.argv[1], 'r') as ciphertxt_file, open(sys.argv[2], 'r') as key_file:
        key = key_file.read().strip()
        ciphertxt = ciphertxt_file.read().strip()

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    if DEBUG:
        print('[KEY]:     %s'%key)
        print('[ALPHA]:   %s'%alphabet)
        print('[CIPHER]:  %s'%ciphertxt)
        print('[DECRYPT]: ', end='')

    with open(sys.argv[3], 'w') as output_file:
        for char in ciphertxt:
            alpha_idx = key.find(char)
            if alpha_idx >= 0:
                output_file.write(alphabet[alpha_idx])
                if DEBUG: print(alphabet[alpha_idx], end='')
            else:
                output_file.write(char)
                if DEBUG: print(char, end='')

if __name__ == '__main__':
    main()