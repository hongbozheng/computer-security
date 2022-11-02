#!/usr/bin/env python3
# CMD: python3 sol_3.1.3.py 3.1.3_aes_ciphertext.hex 3.1.3_aes_key.hex 3.1.3_aes_iv.hex sol_3.1.3.txt

import sys
from Crypto.Cipher import AES

DEBUG=0

def main():
    if len(sys.argv) != 5:
        print('[USAGE] python3 <your_script.py> <ciphertext_file> <key_file> <iv_file> <output_file>')
        exit(1)

    with open(sys.argv[1], 'r') as ciphertxt_file, open(sys.argv[2], 'r') as key_file, open(sys.argv[3], 'r') as iv_file:
        key_byte = bytes.fromhex(key_file.read().strip())
        iv_byte = bytes.fromhex(iv_file.read().strip())
        ciphertxt_byte = bytes.fromhex(ciphertxt_file.read().strip())

    if DEBUG:
        print('[KEY_BYTE]:       %s'%key_byte)
        print('[IV_BYTE]:        %s'%iv_byte)
        print('[CIPHERTXT_BYTE]: %s'%ciphertxt_byte)

    aes = AES.new(key=key_byte, mode=AES.MODE_CBC, iv=iv_byte)
    decrypted_byte = aes.decrypt(ciphertxt_byte)
    if DEBUG: print('[DECRYPT_STR]: %s'%decrypted_byte.decode(encoding='UTF-8', errors='strict'))

    with open(sys.argv[4], 'w') as decrypted_msg_file:
        decrypted_msg_file.write(decrypted_byte.decode(encoding='UTF-8', errors='strict'))

if __name__ == '__main__':
    main()