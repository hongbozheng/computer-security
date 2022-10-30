#!/usr/bin/env python3
# CMD: python3 sol_3.1.5.py 3.1.5_RSA_ciphertext.hex 3.1.5_RSA_private_key.hex 3.1.5_RSA_modulo.hex sol_3.1.5.hex

import sys

DEBUG=0

def main():
    if len(sys.argv) != 5:
        print('[USAGE]: python3 <your_script.py> <ciphertext_file> <key_file> <modulo_file> <output_file>')
        exit()

    with open(sys.argv[1], 'r') as cipher, open(sys.argv[2], 'r') as key, open(sys.argv[3], 'r') as modulo:
        key_int = int(key.read().strip(), 16)
        modulo_int = int(modulo.read().strip(), 16)
        cipher_int = int(cipher.read().strip(), 16)

    if DEBUG:
        print('[KEY_INT]:         %d'%key_int)
        print('[MOD_INT]:         %d'%modulo_int)
        print('[CIPHER_INT]:      %d'%cipher_int)

    decrypt = pow(cipher_int, key_int, modulo_int)
    if DEBUG: print('[DECRYPT_HEX_STR]: %s' % str(hex(decrypt)[2:]))

    with open(sys.argv[4], 'w') as out:
        out.write(str(hex(decrypt)[2:]))

if __name__ == '__main__':
    main()