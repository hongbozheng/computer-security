#!/usr/bin/env python3
# CMD: python3 sol_3.1.2.py 3.1.2_sub_ciphertext.txt 3.1.2_sub_key.txt sol_3.1.2.txt

import sys

DEBUG=0

def main():
    if len(sys.argv) != 4:
        print('[USAGE]: python3 <your_script.py> <ciphertext_file> <key_file> <output_file>')
        exit()

    with open(sys.argv[1], 'r') as cipher, open(sys.argv[2], 'r') as key:
        key_str = key.read().strip()
        cipher_str = cipher.read().strip()

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    if DEBUG:
        print('[KEY]:     %s'%key_str)
        print('[ALPHA]:   %s'%alphabet)
        print('[CIPHER]:  %s'%cipher_str)
        print('[DECRYPT]: ', end='')

    with open(sys.argv[3], 'w') as out:
        for char in cipher_str:
            alpha_idx = key_str.find(char)
            if alpha_idx >= 0:
                out.write(alphabet[alpha_idx])
                if DEBUG: print(alphabet[alpha_idx], end='')
            else:
                out.write(char)
                if DEBUG: print(char, end='')

if __name__ == '__main__':
    main()