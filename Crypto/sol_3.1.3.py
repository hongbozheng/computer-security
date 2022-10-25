#!/usr/bin/env python3
# CMD: python3 sol_3.1.3.py 3.1.3_aes_ciphertext.hex 3.1.3_aes_key.hex 3.1.3_aes_iv.hex sol_3.1.3.txt

import sys
from Crypto.Cipher import AES

DEBUG=False

def main():
    if len(sys.argv) != 5:
        print('[USAGE] python3 <your_script.py> <ciphertext_file> <key_file> <iv_file> <output_file>')
        exit()

    with open(sys.argv[1], 'r') as cipher, open(sys.argv[2], 'r') as key, open(sys.argv[3], 'r') as iv:
        key_byte = bytes.fromhex(key.read().strip())
        iv_byte = bytes.fromhex(iv.read().strip())
        cipher_byte = bytes.fromhex(cipher.read().strip())

    if DEBUG:
        print('[KEY_BYTE]:    %s'%key_byte)
        print('[IV_BYTE]:     %s'%iv_byte)
        print('[CIPHER_BYTE]: %s'%cipher_byte)

    with open(sys.argv[4], 'w') as out:
        aes = AES.new(key=key_byte, mode=AES.MODE_CBC, iv=iv_byte)
        decrypt_byte = aes.decrypt(cipher_byte)
        out.write(decrypt_byte.decode(encoding='UTF-8', errors='strict'))
    if DEBUG: print('[DECRYPT_STR]: %s'%decrypt_byte.decode(encoding='UTF-8', errors='strict'))

if __name__ == '__main__':
    main()
