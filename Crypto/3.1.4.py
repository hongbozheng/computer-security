#!/usr/bin/env python3
# CMD: ./3.1.4.py 3.1.4_aes_weak_ciphertext.hex

import sys
from Crypto.Cipher import AES

KEY_BIT=256
BITS=KEY_BIT-251

def main():
    if len(sys.argv) != 2:
        print('[USAGE]: ./3.1.4.py <ase_weak_ciphertext.hex_file>')

    iv_byte = bytes.fromhex('%032X'%0)
    with open(sys.argv[1], 'r') as ciphertxt_hex_file:
        ciphertxt_byte = bytes.fromhex(ciphertxt_hex_file.read().strip())

    for i in range(2**BITS):
        key = '%064X'%i
        key_byte = bytes.fromhex(key)
        print('[KEY]:            %s'%key)
        print('[KEY_BYTE]:       %s'%key_byte)
        print('[IV_BYTE]:        %s'%iv_byte)
        print('[CIPHERTXT_BYTE]: %s'%ciphertxt_byte)
        aes = AES.new(key=key_byte, mode=AES.MODE_CBC, iv=iv_byte)
        try:
            print('[DECRYPT]:     %s'%aes.decrypt(ciphertxt_byte).decode(encoding='UTF-8', errors='strict'))
        except:
            pass
        print('--------------------------------------------------------------------------------------------------------'
              '------------------------------------------')
if __name__ == '__main__':
    main()