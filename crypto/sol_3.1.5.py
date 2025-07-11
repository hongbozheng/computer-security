#!/usr/bin/env python3
# CMD: python3 sol_3.1.5.py 3.1.5_RSA_ciphertext.hex 3.1.5_RSA_private_key.hex 3.1.5_RSA_modulo.hex sol_3.1.5.hex

import sys

DEBUG=0

def main():
    if len(sys.argv) != 5:
        print('[USAGE]: python3 <your_script.py> <ciphertext_file> <key_file> <modulo_file> <output_file>')
        exit(1)

    with open(sys.argv[1], 'r') as ciphertxt_file, open(sys.argv[2], 'r') as key_file, open(sys.argv[3], 'r') as modulo_file:
        key_int = int(key_file.read().strip(), 16)
        modulo_int = int(modulo_file.read().strip(), 16)
        ciphertxt_int = int(ciphertxt_file.read().strip(), 16)
    ciphertxt_file.close()
    key_file.close()
    modulo_file.close()

    if DEBUG:
        print('[KEY_INT]:            %d'%key_int)
        print('[MOD_INT]:            %d'%modulo_int)
        print('[CIPHERTXT_INT]:      %d'%ciphertxt_int)

    decrypted_int = pow(ciphertxt_int, key_int, modulo_int)
    if DEBUG: print('[DECRYPT_HEX_STR]: %s'%str(hex(decrypted_int)[2:]))

    with open(sys.argv[4], 'w') as decrypted_hex_file:
        decrypted_hex_file.write(str(hex(decrypted_int)[2:]))
    decrypted_hex_file.close()

if __name__ == '__main__':
    main()